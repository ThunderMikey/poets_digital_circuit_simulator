#!/usr/bin/env python3

import sexpdata
import argparse
import inspect
import sys
from typing import NewType
from Cell import Cell
sys.path.append('graph_schema/tools')
from graph.core import DeviceInstance, GraphInstance, EdgeInstance
from graph.load_xml import load_graph_types_and_instances
from graph.save_xml_stream import save_graph
from collections import namedtuple
from common import Terminal, sanitise, gateMappings


###########################
# arguments
###########################

argParser = argparse.ArgumentParser(description="EDIF to XML converter")
argParser.add_argument('-i', '--input-file',
    dest='input_file',
    default="netlists/c17.edif",
    help="EDIF input file")
argParser.add_argument('-o', '--output-file',
    dest='output_file',
    default="STDOUT",
    help="POETS graph XML file")

args = argParser.parse_args()

with open(args.input_file, 'r') as edif:
    # true=None, prevent t being intepreted as True
    e = sexpdata.load(
            edif,
            true=None
        )

#s = sexpdata.car(e)
#print(type(s))
#print(s.__dict__)
#print(inspect.getmembers(s, predicate=inspect.ismethod))

AVAILABLE_CELLS = list(gateMappings.keys())

def get_op(lst):
    return lst[0].value()

def is_op(lst, op):
    return lst[0] == sexpdata.Symbol(op)


def get_sexp_name(item, orig=False):
    """
        orig: original name. (rename id00001 "$_NAND_")
            True returns second field
    """
    nameField = item[1]
    if type(nameField) is sexpdata.Symbol:
        return nameField.value()
    elif type(nameField) is list:
        if is_op(nameField, "rename"):
            return sanitise(nameField[2]) if orig else nameField[1].value()
        else:
            raise(KeyError("The list does not start with rename: {}".format(nameField)))
    else:
        raise(KeyError("{}, {} Not a Symbol or a list".format(
            nameField,
            type(nameField)
            )))

def get_sexp_list(inList, op):
    """
        get list with operator matching `op`
    """
    return [ l for l in inList if is_op(l, op) ]

def get_sexp_unique_op(inList, op):
    """
        get list with operator matching `op`
    """
    lists = get_sexp_list(inList, op)
    return lists[0] if lists else []

def get_sexp_list_contents(lst):
    """
        get content of an sexp list
            e.g. (instance GND (...) (...) )
    """
    return lst[2:]

def get_sexp_list_content(lst):
    """
        get content of an sexp list
            e.g. (instance GND (...) )
    """
    return lst[2]

def convert_cells(rawCells: list):
    """
        {"cellName": Cell class}
    """

    def process_cell(c):
        cellName = get_sexp_name(c)
        cellOrigName = get_sexp_name(c, orig=True)
        cellContents = get_sexp_list_contents(c)
        thisCell = Cell(cellName, cellOrigName)
        view = get_sexp_list(
            cellContents,
            "view"
            )
        # assume the first is netlist view
        netlistView = view[0]
        interface = get_sexp_unique_op(
            get_sexp_list_contents(netlistView),
            "interface"
            )
        ports = get_sexp_list(
            interface[1:],
            "port")
        contents = get_sexp_unique_op(
            get_sexp_list_contents(netlistView),
            "contents")
        if contents:
            instances = get_sexp_list(contents[1:], "instance")
            nets = get_sexp_list(contents[1:], "net")
        else:
            instances = []
            nets =[]
        # add ports, from interface
        for port in ports:
            portName = get_sexp_name(port)
            portContent = get_sexp_list_contents(port)
            d = get_sexp_unique_op(portContent, "direction")
            portDirection = get_sexp_name(d)
            thisCell.add_port(
                name=portName,
                direction=portDirection)
        # add contents if any
        for inst in instances:
            instName = get_sexp_name(inst)
            # assume the fist is VIEW_NETLIST
            instView = get_sexp_list_content(inst)
            instCell = get_sexp_list_content(instView)
            instLib = get_sexp_list_content(instCell)

            viewRef = get_sexp_name(instView)
            cellRef = get_sexp_name(instCell)
            libRef = get_sexp_name(instLib)
            thisCell.add_instance(
                name=instName,
                libRef=libRef,
                cellRef=cellRef,
                viewRef=viewRef
                )
        # add nets if any
        for net in nets:
            netName = get_sexp_name(net)
            netConns = get_sexp_list_content(net)
            netTerminals = get_sexp_list(netConns[1:], "portRef")

            terms = [
                Terminal(
                    get_sexp_name(t),
                    get_sexp_name(get_sexp_list_content(t)) if len(t)>2 else None
                )
                for t in netTerminals
            ]
            thisCell.add_net(
                name=netName,
                terminals=terms
            )

        return thisCell

    # map to dictionay
    cells = dict([
        (get_sexp_name(c), process_cell(c)) for c in rawCells
        ])
    return cells

def process_cells(libName: str, content: list, checkCellAvailability=True):
    """
        external libs need to be checked for availability
        return dict(libRef) of dict(cellRef) of Cells
    """
    rawCells = get_sexp_list(content, "cell")
    # verify availability
    if checkCellAvailability:
        for cell in rawCells:
            cellOrigName = get_sexp_name(cell, orig=True)
            if cellOrigName not in AVAILABLE_CELLS:
                raise(
                    NotImplementedError(
                        "Cell: {0} not implemented".format(cellOrigName)
                        )
                    )
    # map to dictionay
    cells = convert_cells(rawCells)
    return {libName: cells}


#externalLibs_sexp = [c for c in e[2:] if is_op(c, "external")]
edifContent = get_sexp_list_contents(e)
externalLibs_sexp = get_sexp_list(edifContent, "external")
libs_sexp = get_sexp_list(edifContent, "library")
designs_sexp = get_sexp_list(edifContent, "design")


extLibs = {}
intLibs = {}
for el in externalLibs_sexp:
    extLibs.update(
        process_cells(
            libName=get_sexp_name(el),
            content=get_sexp_list_contents(el)
            )
        )


for lib in libs_sexp:
    intLibs.update(
        process_cells(
            libName=get_sexp_name(lib),
            content=get_sexp_list_contents(lib),
            checkCellAvailability=False
            )
        )


##########################
# instantiate graph instance

src = "graph_type/digital_circuit_simulator_graph_type.xml"
(graphTypes,graphInstances)=load_graph_types_and_instances(src,src)

maxTicks=100
# if len(sys.argv)>1:
#     d=int(sys.argv[1])
# if len(sys.argv)>2:
#     b=int(sys.argv[2])
# if len(sys.argv)>3:
#     maxTicks=int(sys.argv[3])

graphType = graphTypes["circuit_gates"]


properties={"max_ticks":maxTicks}


for d in designs_sexp:
    designName = get_sexp_name(d)
    designContents = get_sexp_list_contents(d)
    cellRefs = get_sexp_list(designContents, "cellRef")
    res=GraphInstance(designName, graphType, None)
    for cellRef in cellRefs:
        cellRefName = get_sexp_name(cellRef)
        libRef = get_sexp_list_content(cellRef)
        libRefName = get_sexp_name(libRef)
        cell = intLibs[libRefName][cellRefName]
        cell.instantiate(
            res=res,
            graphTypes=graphTypes,
            externalLibs=extLibs)

if args.output_file == "STDOUT":
    save_dst = sys.stdout
else:
    save_dst=args.output_file

save_graph(res, save_dst)
#print(extLibs)

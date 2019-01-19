#!/usr/bin/env python3

import sexpdata
import argparse
import inspect
from typing import NewType


with open("netlist/c17.edif", 'r') as edif:
    e = sexpdata.load(edif)

#s = sexpdata.car(e)
#print(type(s))
#print(s.__dict__)
#print(inspect.getmembers(s, predicate=inspect.ismethod))

AVAILABLE_CELLS = [
        "$_NAND_",
        "$_NOT_",
        "VCC",
        "GND"
        ]

extLibs = {}

def get_op(lst):
    return lst[0].value()

def is_op(lst, op):
    return lst[0] == sexpdata.Symbol(op)




def process_external_libs(libName: str, content: list):
    """
    cells: {
        "VCC": {
            "interface": {
                "Y": "OUTPUT",
                "A": "INPUT"
            }
        },
        "GND": {...}
    }
    """
    def get_symbol_name(item) -> str:
        if type(item) is sexpdata.Symbol:
            return item.value()
        elif type(item) is list:
            if is_op(item, "rename"):
                return item[1].value()
            else:
                raise(KeyError("The list does not start with rename"))
        else:
            raise(KeyError("Not a Symbol or a list"))
    def get_instance_name(item) -> str:
        if type(item) is sexpdata.Symbol:
            return item.value()
        elif type(item) is list:
            if is_op(item, "rename"):
                return item[2]
            else:
                raise(KeyError("The list does not start with rename"))
        else:
            raise(KeyError("Not a Symbol or a list"))
    def gen_if(cView):
        # generate interface in dictionary
        if not is_op(cView, "view"):
            raise(KeyError("Not a cell view: {0}".format(cView)))

        interface = cView[3]
        if not is_op(interface, "interface"):
            raise(KeyError("Not a cell interface: {0}".format(interface)))

        ports = dict([
            (get_symbol_name(p[1]), get_symbol_name(p[2][1]))
            for p in interface[1:]])

        return {"interface": ports}


    rawCells = [c for c in content if is_op(c, "cell")]
    # verify availability
    for cell in rawCells:
        cellName = get_instance_name(cell[1])
        if cellName not in AVAILABLE_CELLS:
            raise(NotImplementedError("Cell: {0} not implemented".format(cellName)))
    # map to dictionay
    cells = dict([(get_symbol_name(c[1]), gen_if(c[3])) for c in rawCells])
    return {libName: cells}


def process_libs(libName, content):
    pass

def process_design(name, content):
    pass


# start from the third Symbol
for i in e[2:]:
    iop = lambda op: is_op(i, op)
    if iop("external"):
        extLib = process_external_libs(
                libName=i[1].value(),
                content=i[2:]
                )
        extLibs.update(extLib)
    elif iop("library"):
        process_libs(
                libName=i[1].value(),
                content=i[2:]
                )
    elif iop("design"):
        process_design(
                name=i[1].value(),
                content=i[2:]
                )
    else:
        pass

print(extLibs)

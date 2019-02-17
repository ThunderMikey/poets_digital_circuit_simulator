import json
import sys
sys.path.append('graph_schema/tools')
from graph.core import DeviceInstance, GraphInstance, EdgeInstance
from common import Terminal, Instance

class Cell:
    def __init__(self, name, orignal_name):
        self.name = name
        self.orignal_name = orignal_name
        self.ports = {}
        self.instances = {}
        self.nets = {}

    def add_port(self, name, direction):
        self.ports.update({name: direction})

    def add_instance(self, name, libRef, cellRef, viewRef):
        self.instances.update(
                {
                    name: Instance(libRef, cellRef, viewRef)
                    }
                )

    def add_net(self, name, terminals):
        """
            [
                {"portRef": string,
                    "instanceRef": string
                }
            ]
        """
        self.nets.update(
                {
                    name: terminals
                    }
                )

    def instantiate(self, res: GraphInstance, graphTypes, externalLibs):
        """
            externalLibs={
                "libname": {
                    "name": Cell1,
                    "name2": Cell2
                }
                
            }
        """
        # gates
        graphType = graphTypes["circuit_gates"]
        inputTerminalGate = graphType.device_types["input_terminal"]
        outputTerminalGate = graphType.device_types["output_terminal"]
        # TODO: do not currently have exit node
        # exit is controlled by global `max_ticks`
        #exitNode = graphType.device_types["exit_node"]
        graphInstDict = {}
        def get_gate_type(libRef, cellRef):
            cell = externalLibs[libRef][cellRef]
            return cell.orignal_name

        def find_gt_gate(gateType, device_types=graphType.device_types):
            gateMappings = {
                "AND": 0,
                "OR": 1,
                "GND": "gnd",
                "VCC": "vcc",
                "$_NAND_": "nand"
                }
            return device_types[gateMappings[gateType]]
        
        def get_input_ports(cell):
            return [ p for (p, dirc) in cell.ports.items() if dirc == "INPUT" ]

        def get_output_ports(cell):
            return [ p for (p, dirc) in cell.ports.items() if dirc == "OUTPUT" ]
        
        def get_net_terminals(cell, direction: str, nets, eLibs, graphInstDict):
            """
                return terminal device(s) and its port
                    port must match port definition in graph schema
                INPUT for a Cell is drain, but it is src for a port
            """
            srcTerms = []
            for term in nets:
                if term.instanceRef:
                    inst = cell.instances[term.instanceRef]
                    # the base gate
                    gate = eLibs[inst.libRef][inst.cellRef]
                    if gate.ports[term.portRef] != direction:
                        srcTerms.append(
                            (graphInstDict[term.instanceRef],
                            term.portRef)
                        )
                else:
                    if cell.ports[term.portRef] == direction:
                        # input terminal has only one output pin
                        # output terminal has only one receive pin
                        pinName = "out" if direction == "INPUT" else "receive"
                        srcTerms.append(
                            (graphInstDict[term.portRef],
                            pinName)
                        )
            if direction == "INPUT":
                assert(len(srcTerms) == 1,
                    "There can only be one source terminal in the net", 
                    srcTerms)
                return srcTerms[0]
            else:
                return srcTerms


            


        # construct device instance
        for (instId, inst) in self.instances.items():
            gType = get_gate_type(inst.libRef, inst.cellRef)
            node = DeviceInstance(
                parent=res,
                id="{0}_{1}".format(gType, instId),
                device_type=find_gt_gate(gType),
                )
            res.add_device_instance(node)
            graphInstDict[instId] = node
        
        # construct input terminals
        inTerms = get_input_ports(self)
        for inPin in inTerms:
            gid = inPin
            node = DeviceInstance(
                parent=res,
                id="{0}_{1}_{2}".format(self.name, "it", gid),
                device_type=inputTerminalGate,
                properties={"flip_interval": 200}
            )
            res.add_device_instance(node)
            graphInstDict[gid] = node
        
        # construct output terminals
        outTerms = get_output_ports(self)
        for outPin in outTerms:
            gid = outPin
            node = DeviceInstance(
                parent=res,
                id="{0}_{1}_{2}".format(self.name, "ot", gid),
                device_type=outputTerminalGate,
            )
            res.add_device_instance(node)
            graphInstDict[gid] = node

        # construct edge instances
        for (_, edges) in self.nets.items():
            # find the only source
            (srcDev, srcPin) = get_net_terminals(
                self,
                "INPUT", edges,
                externalLibs, graphInstDict)
            # find drains
            drains = get_net_terminals(
                self,
                "OUTPUT", edges,
                externalLibs, graphInstDict)
            
            for (dstDev, dstPin) in drains:
                # except KeyError:
                #     srcDev = None
                #     srcPin = None
                edgeInst = EdgeInstance(
                    parent=res,
                    dst_device=dstDev,
                    dst_pin=dstPin,
                    src_device=srcDev,
                    src_pin=srcPin)
                res.add_edge_instance(edgeInst)

    def __str__(self):
        return json.dumps(
            {
            "name": self.name,
            "orignal_name": self.orignal_name,
            "ports": self.ports,
            "instances": self.instances,
            "nets": self.nets
            },
            indent=2, sort_keys=True
        )
    def __repr__(self):
        return self.__str__()

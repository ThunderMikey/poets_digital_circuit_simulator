import json
import sys
sys.path.append('graph_schema/tools')
from graph.core import DeviceInstance, GraphInstance, EdgeInstance

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
                    name:{
                        "libRef": libRef,
                        "cellRef": cellRef,
                        "viewRef": viewRef
                        }
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
        exitNode = graphType.device_types["exit_node"]
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
        
        def get_net_src(cell, nets):
            for net in nets:
                instRef = net["instanceRef"]
                inst = cell.instances[instRef]

            


        # construct device instance
        for (gid, gate) in self.instances.items():
            gType = get_gate_type(gate["libRef"], gate["cellRef"])
            node = DeviceInstance(
                parent=res,
                id="{0}_{1}".format(gType, gid),
                device_type=find_gt_gate(gType),
                )
            res.add_device_instance(node)
            graphInstDict[gid] = node
        
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
                id="{0}_{1}_{2}".format(self.name, "it", gid),
                device_type=outputTerminalGate,
            )
            res.add_device_instance(node)
            graphInstDict[gid] = node

        # construct edge instances
        for (netName, nets) in self.nets.items():
            print(netName, nets)
            gType = get_gate_type(gate["libRef"], gate["cellRef"])
            print(gate)
            (srcDev, srcPin) = get_net_src()
            drains = get_net_drains()
            for idx, inPin in enumerate(gate):
                print(inPin)
                srcDev = graphInstDict[inPin]
                srcPin = "out"
                # except KeyError:
                #     srcDev = None
                #     srcPin = None
                edgeInst = EdgeInstance(
                    parent=res,
                    dst_device=graphInstDict[gid],
                    dst_pin="in{}".format(idx),
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

#!/usr/bin/env python3
import sys
import os
import math

sys.path.append('../../tools')

from graph.core import DeviceInstance, GraphInstance, EdgeInstance

from graph.load_xml import load_graph_types_and_instances
from graph.save_xml_stream import save_graph

appBase=os.path.dirname(os.path.realpath(__file__))

src=appBase+"/digital_circuit_simulator_graph_type.xml"
(graphTypes,graphInstances)=load_graph_types_and_instances(src,src)

maxTicks=100
# if len(sys.argv)>1:
#     d=int(sys.argv[1])
# if len(sys.argv)>2:
#     b=int(sys.argv[2])
# if len(sys.argv)>3:
#     maxTicks=int(sys.argv[3])

graphType = graphTypes["circuit_gates"]
universal2Gate = graphType.device_types["universal2"]
inputTerminalGate = graphType.device_types["input_terminal"]
outputTerminalGate = graphType.device_types["output_terminal"]
exitNode = graphType.device_types["exit_node"]

instName = "full_adder_1bit"

properties={"max_ticks":maxTicks}
res=GraphInstance(instName, graphType, None)

usingCircuit = {
    "name": "1-bit full adder Cin, A, B -> Sum, Cout",
    "in": [1, 2, 3],
    "out":   [5, 11],
    "gates": [ 
      { "id":4,  "type":"XOR", "in": [2, 3] },
      { "id":5,  "type":"XOR", "in": [1, 4] }, 
      { "id":6,  "type":"AND", "in": [2, 3] },
      { "id":7,  "type":"AND", "in": [1, 4] },
      { "id":11, "type":"OR",  "in": [6, 7] }
    ]
}

gateTypes = {
    "AND": 0,
    "OR": 1,
    "XOR": 2
}

graphInstDict = {}

# construct DeviceInstance
for gate in usingCircuit["gates"]:
    gid = gate["id"]
    gType = gate["type"]
    node = DeviceInstance(
        parent=res,
        id="{0}_{1}".format(gType, gid),
        device_type=universal2Gate,
        properties={"gate_type": gateTypes[gType]}
        )
    res.add_device_instance(node)
    graphInstDict[gid] = node

# construct input terminals
for inPin in usingCircuit["in"]:
    gid = inPin
    node = DeviceInstance(
        parent=res,
        id="{0}_{1}".format("input_terminal", gid),
        device_type=inputTerminalGate,
        properties={"flip_interval": inPin}
    )
    res.add_device_instance(node)
    graphInstDict[gid] = node

# contruct output terminals
for outPin in usingCircuit["out"]:
    gid = str(outPin) + "ot"
    node = DeviceInstance(
        parent=res,
        id="{0}_{1}".format("output_terminal", gid),
        device_type=outputTerminalGate
    )
    res.add_device_instance(node)
    graphInstDict[gid] = node

# construct edge instances
for gate in usingCircuit["gates"]:
    gid = gate["id"]
    gType = gate["type"]
    for idx, inPin in enumerate(gate["in"]):
        # try:
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

# connect output terminals
for srcGate in usingCircuit["out"]:
    destGate = str(srcGate) + "ot"
    # try:
    destDev = graphInstDict[destGate]
    destPin = "receive"
    srcDev = graphInstDict[srcGate]
    srcPin = "out"
    # except KeyError:
    #     srcDev = None
    #     srcPin = None
    edgeInst = EdgeInstance(
        parent=res,
        dst_device=destDev,
        dst_pin=destPin,
        src_device=srcDev,
        src_pin=srcPin)
    res.add_edge_instance(edgeInst)

save_graph(res,sys.stdout)

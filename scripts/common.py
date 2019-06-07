from collections import namedtuple

Terminal = namedtuple('Terminal', 'portRef, instanceRef')

Instance = namedtuple('Instance', 'libRef, cellRef, viewRef')
gateMappings = {
    "GND": "gnd",
    "VCC": "vcc",
    "__NAND_": "nand",
    "__NOT_": "not",
    "__XOR_": "xor"
}

def sanitise(string):
    """
        remove `$` char from string
        make it good for graph id and path
    """
    return string.replace('$', '_')

def flatten_array(baseName, idx):
    """
        flatten array into form "in__1"
    """
    return baseName+"__"+str(idx)


from collections import namedtuple

Terminal = namedtuple('Terminal', 'portRef, instanceRef')

Instance = namedtuple('Instance', 'libRef, cellRef, viewRef')
import ctypes as C

import sys

sys.path.insert(0, "/home/vsriv/Git/pymake/Test/Node")
from Node import Node
sys.path.pop(0)

lib = C.CDLL("/home/vsriv/Git/pymake/Test/Face/libFace.so")

class Face(C.Structure):

    _fields_ = [
        ("nNodes", C.c_int),
        ("nodes", C.POINTER(Node)),
    ]

    _init = lib.Face__init
    _init.restype = None
    _init.argtypes = [
        C.c_void_p,
    ]

    _delete = lib.Face__delete
    _delete.restype = None
    _delete.argtypes = [
        C.c_void_p,
    ]

    def __init__(
        self,
    ):
        return self._init(
            C.addressof(self),
        )

    def delete(
        self,
    ):
        return self._delete(
            C.addressof(self),
        )


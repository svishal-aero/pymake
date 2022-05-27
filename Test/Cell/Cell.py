import ctypes as C

import sys

sys.path.insert(0, "/home/svishal/Git/pymake/Test/Face")
from Face import Face
sys.path.pop(0)

lib = C.CDLL("/home/svishal/Git/pymake/Test/Cell/libCell.so")

class Cell(C.Structure):

    _pack_ = 2
    _fields_ = [
        ("nFaces", C.c_int),
        ("faces", C.POINTER(Face)),
    ]

    _init = lib.Cell__init
    _init.restype = None
    _init.argtypes = [
        C.c_void_p,
    ]

    _delete = lib.Cell__delete
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


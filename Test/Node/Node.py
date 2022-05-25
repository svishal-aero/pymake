import ctypes as C

lib = C.CDLL("/home/vsriv/Git/pymake/Test/Node/libNode.so")

class Node(C.Structure):

    _pack_ = 1
    _fields_ = [
        ("x", (C.c_double)*3),
    ]

    _init = lib.Node__init
    _init.restype = None
    _init.argtypes = [
        C.c_void_p,
    ]

    _delete = lib.Node__delete
    _delete.restype = None
    _delete.argtypes = [
        C.c_void_p,
    ]

    _getDistanceFromNode = lib.Node__getDistanceFromNode
    _getDistanceFromNode.restype = C.c_double
    _getDistanceFromNode.argtypes = [
        C.c_void_p,
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

    def getDistanceFromNode(
        self,
        other,
    ):
        return self._getDistanceFromNode(
            C.addressof(self),
            C.addressof(other),
        )


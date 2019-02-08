import os
from _ctypes import Structure, POINTER, byref
from ctypes import cdll, c_int32, c_double

import numpy as np

ljig = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),"libjigsaw64r.so"))
indx_t = c_int32
real_t = c_double


class DStruct(Structure):
    def dict(self):
        return {f[0]: getattr(self, f[0]) for f in self._fields_}


def tuplize(i):
    try:
        return tuple(i)
    except Exception:
        return i


class IStruct(DStruct):
    def allocate(self, size):
        self.data = (self.data._type_ * size)()
        self.size = size

    def unsafe_store(self, data):
        self.size = len(data[0])
        # from numpy to recarray
        data = np.rec.fromarrays(data, dtype=self.data._type_)
        # from recarray to ctypes
        self.data = data.ctypes.data_as(POINTER(self.data._type_))

    def old_store(self, data):
        self.size = len(data[0])
        data = [tuple(i.tolist()) for i in data]
        # data = np.rec.fromarrays(data, dtype=self.data._type_)
        self.data = (self.data._type_ * self.size)(*[tuple(tuplize(j) for j in i) for i in zip(*data)])

    def store(self, data, tags=None):
        self.size = len(data)
        data = map(tuplize, data)
        if tags is not None:
            assert len(tags) == self.size, "tags should be %s scalars (not %s)" % (self.size, tags.shape)
            data = [tuple(tuplize(j) for j in i) for i in zip(data, tags)]
        self.data = (self.data._type_ * self.size)(*data)

    def __iter__(self):
        for i in range(self.size):
            yield self.data[i]


JIGSAW_UNKNOWN_ERROR = -1
JIGSAW_NO_ERROR = +0
JIGSAW_FILE_NOT_LOCATED = +2
JIGSAW_FILE_NOT_CREATED = +3
JIGSAW_INVALID_ARGUMENT = +4
JIGSAW_NULL_FLAG = -100
JIGSAW_EUCLIDEAN_MESH = +100
JIGSAW_EUCLIDEAN_GRID = +101
JIGSAW_EUCLIDEAN_DUAL = +102
JIGSAW_ELLIPSOID_MESH = +200
JIGSAW_ELLIPSOID_GRID = +201
JIGSAW_ELLIPSOID_DUAL = +202
JIGSAW_HFUN_RELATIVE = +300
JIGSAW_HFUN_ABSOLUTE = +301
JIGSAW_KERN_DELFRONT = +400
JIGSAW_KERN_DELAUNAY = +401
JIGSAW_BNDS_TRIACELL = +402
JIGSAW_BNDS_DUALCELL = +403


class jigsaw_jig_t(DStruct):
    _fields_ = [
        ('verbosity', indx_t),
        ('geom_seed', indx_t),
        ('geom_feat', indx_t),
        ('geom_eta1', real_t),
        ('geom_eta2', real_t),
        ('hfun_scal', indx_t),
        ('hfun_hmax', real_t),
        ('hfun_hmin', real_t),
        ('bnds_kern', indx_t),
        ('mesh_dims', indx_t),
        ('mesh_kern', indx_t),
        ('mesh_iter', indx_t),
        ('mesh_top1', indx_t),
        ('mesh_top2', indx_t),
        ('mesh_rad2', real_t),
        ('mesh_rad3', real_t),
        ('mesh_siz1', real_t),
        ('mesh_siz2', real_t),
        ('mesh_siz3', real_t),
        ('mesh_off2', real_t),
        ('mesh_off3', real_t),
        ('mesh_snk2', real_t),
        ('mesh_snk3', real_t),
        ('mesh_eps1', real_t),
        ('mesh_eps2', real_t),
        ('mesh_vol3', real_t),
        ('optm_iter', indx_t),
        ('optm_qtol', real_t),
        ('optm_qlim', real_t),
        ('optm_tria', indx_t),
        ('optm_dual', indx_t),
        ('optm_zip_', indx_t),
        ('optm_div_', indx_t)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ljig.jigsaw_init_jig_t(byref(self))


class jigsaw_VERT2_t(DStruct):
    _fields_ = [
        ("ppos", real_t * 2),
        ("itag", indx_t)]


class jigsaw_VERT3_t(DStruct):
    _fields_ = [
        ("ppos", real_t * 3),
        ("itag", indx_t)]


class jigsaw_EDGE2_t(DStruct):
    _fields_ = [
        ("ppos", indx_t * 2),
        ("itag", indx_t)]


class jigsaw_TRIA3_t(DStruct):
    _fields_ = [
        ("ppos", indx_t * 3),
        ("itag", indx_t)]


class jigsaw_TRIA4_t(DStruct):
    _fields_ = [
        ("ppos", indx_t * 3),
        ("itag", indx_t)]


class jigsaw_VERT2_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(jigsaw_VERT2_t))]


class jigsaw_VERT3_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(jigsaw_VERT3_t))]


class jigsaw_EDGE2_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(jigsaw_EDGE2_t))]


class jigsaw_TRIA3_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(jigsaw_TRIA3_t))]


class jigsaw_TRIA4_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(jigsaw_TRIA4_t))]


class jigsaw_REALS_array_t(IStruct):
    _fields_ = [
        ("size", indx_t),
        ("data", POINTER(real_t))]


class jigsaw_msh_t(DStruct):
    _fields_ = [('flags', indx_t),
                ('vert2', jigsaw_VERT2_array_t),
                ('vert3', jigsaw_VERT3_array_t),
                ('power', jigsaw_REALS_array_t),
                ('edge2', jigsaw_EDGE2_array_t),
                ('tria3', jigsaw_TRIA3_array_t),
                ('tria4', jigsaw_TRIA4_array_t),
                ('radii', jigsaw_REALS_array_t),
                ('xgrid', jigsaw_REALS_array_t),
                ('ygrid', jigsaw_REALS_array_t),
                ('zgrid', jigsaw_REALS_array_t),
                ('value', jigsaw_REALS_array_t)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ljig.jigsaw_init_msh_t(byref(self))


def makeMesh(jjig, geom, init=None,hfun=None):
    mesh = jigsaw_msh_t()
    init = byref(init) if init is not None else 0
    hfun = byref(hfun) if hfun is not None else 0
    retv = ljig.jigsaw_make_mesh(byref(jjig), byref(geom), init, hfun, byref(mesh))
    return retv, mesh

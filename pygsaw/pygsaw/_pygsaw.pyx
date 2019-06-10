__package__="pygsaw._pygsaw"
cimport jigsaw as pygsaw

import numpy as np
cimport numpy as np

UNKNOWN_ERROR = pygsaw.JIGSAW_UNKNOWN_ERROR
NO_ERROR = pygsaw.JIGSAW_NO_ERROR
FILE_NOT_LOCATED = pygsaw.JIGSAW_FILE_NOT_LOCATED
FILE_NOT_CREATED = pygsaw.JIGSAW_FILE_NOT_CREATED
INVALID_ARGUMENT = pygsaw.JIGSAW_INVALID_ARGUMENT
NULL_FLAG = pygsaw.JIGSAW_NULL_FLAG
EUCLIDEAN_MESH = pygsaw.JIGSAW_EUCLIDEAN_MESH
EUCLIDEAN_GRID = pygsaw.JIGSAW_EUCLIDEAN_GRID
EUCLIDEAN_DUAL = pygsaw.JIGSAW_EUCLIDEAN_DUAL
ELLIPSOID_MESH = pygsaw.JIGSAW_ELLIPSOID_MESH
ELLIPSOID_GRID = pygsaw.JIGSAW_ELLIPSOID_GRID
ELLIPSOID_DUAL = pygsaw.JIGSAW_ELLIPSOID_DUAL
HFUN_RELATIVE = pygsaw.JIGSAW_HFUN_RELATIVE
HFUN_ABSOLUTE = pygsaw.JIGSAW_HFUN_ABSOLUTE
KERN_DELFRONT = pygsaw.JIGSAW_KERN_DELFRONT
KERN_DELAUNAY = pygsaw.JIGSAW_KERN_DELAUNAY
BNDS_TRIACELL = pygsaw.JIGSAW_BNDS_TRIACELL
BNDS_DUALCELL = pygsaw.JIGSAW_BNDS_DUALCELL

cdef class Mesh:
    cdef pygsaw.jigsaw_msh_t msh
    cdef np.ndarray _verts2D
    cdef np.ndarray _verts3D
    cdef np.ndarray _powers
    cdef np.ndarray _edges
    cdef np.ndarray _trias
    cdef np.ndarray _quads
    cdef np.ndarray _radii
    cdef np.ndarray _xgrid
    cdef np.ndarray _ygrid
    cdef np.ndarray _zgrid
    cdef np.ndarray _values

    def __init__(self, pygsaw.indx_t flags=EUCLIDEAN_MESH, verts2D=0, verts3D=0, powers=0, edges=0, trias=0, quads=0,
                 radii=0, xgrid=0, ygrid=0, zgrid=0, values=0):
        pygsaw.jigsaw_init_msh_t(&self.msh)
        self.msh._flags = flags

        self._verts2D = self.setupVerts2D(verts2D) if verts2D > 0 else np.ndarray(0, dtype=np.void)
        self._verts3D = self.setupVerts3D(verts3D) if verts3D > 0 else np.ndarray(0, dtype=np.void)
        self._powers = self.setupPowers(powers) if powers > 0 else np.ndarray(0, dtype=np.void)
        self._edges = self.setupEdges(edges) if edges > 0 else np.ndarray(0, dtype=np.void)
        self._trias = self.setupTrias(trias) if trias > 0 else np.ndarray(0, dtype=np.void)
        self._quads = self.setupQuads(quads) if quads > 0 else np.ndarray(0, dtype=np.void)
        self._radii = self.setupRadii(radii) if radii > 0 else np.ndarray(0, dtype=np.void)
        self._xgrid = self.setupXgrid(xgrid) if xgrid > 0 else np.ndarray(0, dtype=np.void)
        self._ygrid = self.setupYgrid(ygrid) if ygrid > 0 else np.ndarray(0, dtype=np.void)
        self._zgrid = self.setupZgrid(zgrid) if zgrid > 0 else np.ndarray(0, dtype=np.void)
        self._values = self.setupValues(values) if values > 0 else np.ndarray(0, dtype=np.void)

    cdef np.ndarray setupVerts2D(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('pos', ('f8', 2)), ('tag', 'i4')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.jigsaw_VERT2_t, cast=True] res = container
        self.msh._vert2._data = &res[0]
        self.msh._vert2._size = size
        return container

    cdef np.ndarray setupVerts3D(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('pos', ('f8', 3)), ('tag', 'i4')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.jigsaw_VERT3_t, cast=True] res = container
        self.msh._vert3._data = &res[0]
        self.msh._vert3._size = size
        return container

    cdef np.ndarray setupPowers(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._power._data = &res[0]
        self.msh._power._size = size
        return container

    cdef np.ndarray setupEdges(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('node', ('i4', 2)), ('tag', 'i4')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.jigsaw_EDGE2_t, cast=True] res = container
        self.msh._edge2._data = &res[0]
        self.msh._edge2._size = size
        return container

    cdef np.ndarray setupTrias(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('node', ('i4', 3)), ('tag', 'i4')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.jigsaw_TRIA3_t, cast=True] res = container
        self.msh._tria3._data = &res[0]
        self.msh._tria3._size = size
        return container

    cdef np.ndarray setupQuads(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('node', ('i4', 4)), ('tag', 'i4')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.jigsaw_TRIA4_t, cast=True] res = container
        self.msh._tria4._data = &res[0]
        self.msh._tria4._size = size
        return container

    cdef np.ndarray setupRadii(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._radii._data = &res[0]
        self.msh._radii._size = size
        return container

    cdef np.ndarray setupXgrid(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._xgrid._data = &res[0]
        self.msh._xgrid._size = size
        return container

    cdef np.ndarray setupYgrid(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._ygrid._data = &res[0]
        self.msh._ygrid._size = size
        return container

    cdef np.ndarray setupZgrid(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._zgrid._data = &res[0]
        self.msh._zgrid._size = size
        return container

    cdef np.ndarray setupValues(self, size):
        cdef container = np.ndarray(size, dtype=np.dtype([('data', 'f8')], align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.real_t, cast=True] res = container
        self.msh._value._data = &res[0]
        self.msh._value._size = size
        return container

    cpdef sync(self):
        cdef np.ndarray verts2D_res
        if self.msh._vert2._size > 0:
            verts2D_res = np.ndarray(
                shape=self.msh._vert2._size,
                dtype=np.dtype([('pos', ('f8', 2)), ('tag', 'i4')], align=True))
            verts2D_res.data =  <char *> self.msh._vert2._data
            self._verts2D = verts2D_res
        cdef np.ndarray verts3D_res
        if self.msh._vert3._size > 0:
            verts3D_res = np.ndarray(
                shape=self.msh._vert3._size,
                dtype=np.dtype([('pos', ('f8', 3)), ('tag', 'i4')], align=True))
            verts3D_res.data =  <char *> self.msh._vert3._data
            self._verts3D = verts3D_res
        cdef np.ndarray powers_res
        if self.msh._power._size > 0:
            powers_res = np.ndarray(
                shape=self.msh._power._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            powers_res.data =  <char *> self.msh._power._data
            self._powers = powers_res
        cdef np.ndarray edges_res
        if self.msh._edge2._size > 0:
            edges_res = np.ndarray(
                shape=self.msh._edge2._size,
                dtype=np.dtype([('node', ('i4', 2)), ('tag', 'i4')], align=True))
            edges_res.data =  <char *> self.msh._edge2._data
            self._edges = edges_res
        cdef np.ndarray trias_res
        if self.msh._tria3._size > 0:
            trias_res = np.ndarray(
                shape=self.msh._tria3._size,
                dtype=np.dtype([('node', ('i4', 3)), ('tag', 'i4')], align=True))
            trias_res.data =  <char *> self.msh._tria3._data
            self._trias = trias_res
        cdef np.ndarray quads_res
        if self.msh._tria4._size > 0:
            quads_res = np.ndarray(
                shape=self.msh._tria4._size,
                dtype=np.dtype([('node', ('i4', 4)), ('tag', 'i4')], align=True))
            quads_res.data =  <char *> self.msh._tria4._data
            self._quads = quads_res
        cdef np.ndarray radii_res
        if self.msh._radii._size > 0:
            radii_res = np.ndarray(
                shape=self.msh._radii._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            radii_res.data =  <char *> self.msh._radii._data
            self._radii = radii_res
        cdef np.ndarray xgrid_res
        if self.msh._xgrid._size > 0:
            xgrid_res = np.ndarray(
                shape=self.msh._xgrid._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            xgrid_res.data =  <char *> self.msh._xgrid._data
            self._xgrid = xgrid_res
        cdef np.ndarray ygrid_res
        if self.msh._ygrid._size > 0:
            ygrid_res = np.ndarray(
                shape=self.msh._ygrid._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            ygrid_res.data =  <char *> self.msh._ygrid._data
            self._ygrid = ygrid_res
        cdef np.ndarray zgrid_res
        if self.msh._zgrid._size > 0:
            zgrid_res = np.ndarray(
                shape=self.msh._zgrid._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            zgrid_res.data =  <char *> self.msh._zgrid._data
            self._zgrid = zgrid_res
        cdef np.ndarray values_res
        if self.msh._value._size > 0:
            values_res = np.ndarray(
                shape=self.msh._value._size,
                dtype=np.dtype([('data', 'f8')], align=True))
            values_res.data =  <char *> self.msh._value._data
            self._values = values_res

    @property
    def verts2D(self):
        return self._verts2D

    @property
    def verts3D(self):
        return self._verts3D

    @property
    def powers(self):
        return self._powers

    @property
    def edges(self):
        return self._edges

    @property
    def trias(self):
        return self._trias

    @property
    def quads(self):
        return self._quads

    @property
    def radii(self):
        return self._radii

    @property
    def xgrid(self):
        return self._xgrid

    @property
    def ygrid(self):
        return self._ygrid

    @property
    def zgrid(self):
        return self._zgrid

    @property
    def values(self):
        return self._values

cdef class Conf:
    cdef pygsaw.jigsaw_jig_t jjig

    def __cinit__(self):
        pygsaw.jigsaw_init_jig_t(&self.jjig)

        self.jjig._verbosity = 1
        self.jjig._hfun_scal = pygsaw.JIGSAW_HFUN_ABSOLUTE
        self.jjig._hfun_hmax = 0.01
        self.jjig._hfun_hmin = 0.01

    def toDict(self):
        return self.jjig

    @property
    def optm_zip_(self):
        return self.jjig._optm_zip_

    @optm_zip_.setter
    def optm_zip_(self, value):
        self.jjig._optm_zip_ = value

    @property
    def mesh_top1(self):
        return self.jjig._mesh_top1

    @mesh_top1.setter
    def mesh_top1(self, value):
        self.jjig._mesh_top1 = value

    @property
    def optm_tria(self):
        return self.jjig._optm_tria

    @optm_tria.setter
    def optm_tria(self, value):
        self.jjig._optm_tria = value

    @property
    def mesh_rad2(self):
        return self.jjig._mesh_rad2

    @mesh_rad2.setter
    def mesh_rad2(self, value):
        self.jjig._mesh_rad2 = value

    @property
    def mesh_rad3(self):
        return self.jjig._mesh_rad3

    @mesh_rad3.setter
    def mesh_rad3(self, value):
        self.jjig._mesh_rad3 = value

    @property
    def optm_dual(self):
        return self.jjig._optm_dual

    @optm_dual.setter
    def optm_dual(self, value):
        self.jjig._optm_dual = value

    @property
    def optm_qlim(self):
        return self.jjig._optm_qlim

    @optm_qlim.setter
    def optm_qlim(self, value):
        self.jjig._optm_qlim = value

    @property
    def optm_qtol(self):
        return self.jjig._optm_qtol

    @optm_qtol.setter
    def optm_qtol(self, value):
        self.jjig._optm_qtol = value

    @property
    def hfun_hmax(self):
        return self.jjig._hfun_hmax

    @hfun_hmax.setter
    def hfun_hmax(self, value):
        self.jjig._hfun_hmax = value

    @property
    def mesh_dims(self):
        return self.jjig._mesh_dims

    @mesh_dims.setter
    def mesh_dims(self, value):
        self.jjig._mesh_dims = value

    @property
    def optm_iter(self):
        return self.jjig._optm_iter

    @optm_iter.setter
    def optm_iter(self, value):
        self.jjig._optm_iter = value

    @property
    def mesh_eps2(self):
        return self.jjig._mesh_eps2

    @mesh_eps2.setter
    def mesh_eps2(self, value):
        self.jjig._mesh_eps2 = value

    @property
    def verbosity(self):
        return self.jjig._verbosity

    @verbosity.setter
    def verbosity(self, value):
        self.jjig._verbosity = value

    @property
    def mesh_kern(self):
        return self.jjig._mesh_kern

    @mesh_kern.setter
    def mesh_kern(self, value):
        self.jjig._mesh_kern = value

    @property
    def mesh_eps1(self):
        return self.jjig._mesh_eps1

    @mesh_eps1.setter
    def mesh_eps1(self, value):
        self.jjig._mesh_eps1 = value

    @property
    def mesh_vol3(self):
        return self.jjig._mesh_vol3

    @mesh_vol3.setter
    def mesh_vol3(self, value):
        self.jjig._mesh_vol3 = value

    @property
    def mesh_snk3(self):
        return self.jjig._mesh_snk3

    @mesh_snk3.setter
    def mesh_snk3(self, value):
        self.jjig._mesh_snk3 = value

    @property
    def mesh_snk2(self):
        return self.jjig._mesh_snk2

    @mesh_snk2.setter
    def mesh_snk2(self, value):
        self.jjig._mesh_snk2 = value

    @property
    def optm_div_(self):
        return self.jjig._optm_div_

    @optm_div_.setter
    def optm_div_(self, value):
        self.jjig._optm_div_ = value

    @property
    def bnds_kern(self):
        return self.jjig._bnds_kern

    @bnds_kern.setter
    def bnds_kern(self, value):
        self.jjig._bnds_kern = value

    @property
    def geom_seed(self):
        return self.jjig._geom_seed

    @geom_seed.setter
    def geom_seed(self, value):
        self.jjig._geom_seed = value

    @property
    def mesh_top2(self):
        return self.jjig._mesh_top2

    @mesh_top2.setter
    def mesh_top2(self, value):
        self.jjig._mesh_top2 = value

    @property
    def mesh_iter(self):
        return self.jjig._mesh_iter

    @mesh_iter.setter
    def mesh_iter(self, value):
        self.jjig._mesh_iter = value

    @property
    def geom_feat(self):
        return self.jjig._geom_feat

    @geom_feat.setter
    def geom_feat(self, value):
        self.jjig._geom_feat = value

    @property
    def hfun_hmin(self):
        return self.jjig._hfun_hmin

    @hfun_hmin.setter
    def hfun_hmin(self, value):
        self.jjig._hfun_hmin = value

    @property
    def mesh_off2(self):
        return self.jjig._mesh_off2

    @mesh_off2.setter
    def mesh_off2(self, value):
        self.jjig._mesh_off2 = value

    @property
    def mesh_off3(self):
        return self.jjig._mesh_off3

    @mesh_off3.setter
    def mesh_off3(self, value):
        self.jjig._mesh_off3 = value

    @property
    def geom_eta1(self):
        return self.jjig._geom_eta1

    @geom_eta1.setter
    def geom_eta1(self, value):
        self.jjig._geom_eta1 = value

    @property
    def geom_eta2(self):
        return self.jjig._geom_eta2

    @geom_eta2.setter
    def geom_eta2(self, value):
        self.jjig._geom_eta2 = value

    @property
    def hfun_scal(self):
        return self.jjig._hfun_scal

    @hfun_scal.setter
    def hfun_scal(self, value):
        self.jjig._hfun_scal = value

    @property
    def mesh_siz3(self):
        return self.jjig._mesh_siz3

    @mesh_siz3.setter
    def mesh_siz3(self, value):
        self.jjig._mesh_siz3 = value

    @property
    def mesh_siz2(self):
        return self.jjig._mesh_siz2

    @mesh_siz2.setter
    def mesh_siz2(self, value):
        self.jjig._mesh_siz2 = value

    @property
    def mesh_siz1(self):
        return self.jjig._mesh_siz1

    @mesh_siz1.setter
    def mesh_siz1(self, value):
        self.jjig._mesh_siz1 = value

cpdef pygsaw.indx_t make_mesh(Conf jcfg, Mesh geom, Mesh init, Mesh hfun, Mesh mesh):
    cdef pygsaw.indx_t ret = pygsaw.jigsaw_make_mesh(&jcfg.jjig, &geom.msh, &init.msh, &hfun.msh, &mesh.msh)
    mesh.sync()
    return ret

cimport numpy as np
cdef extern from "../src/jigsaw.cpp":
    ctypedef np.int32_t  indx_t
    ctypedef double      real_t

    cdef indx_t JIGSAW_UNKNOWN_ERROR = -1
    cdef indx_t JIGSAW_NO_ERROR = +0
    cdef indx_t JIGSAW_FILE_NOT_LOCATED = +2
    cdef indx_t JIGSAW_FILE_NOT_CREATED = +3
    cdef indx_t JIGSAW_INVALID_ARGUMENT = +4
    cdef indx_t JIGSAW_NULL_FLAG = -100
    cdef indx_t JIGSAW_EUCLIDEAN_MESH = +100
    cdef indx_t JIGSAW_EUCLIDEAN_GRID = +101
    cdef indx_t JIGSAW_EUCLIDEAN_DUAL = +102
    cdef indx_t JIGSAW_ELLIPSOID_MESH = +200
    cdef indx_t JIGSAW_ELLIPSOID_GRID = +201
    cdef indx_t JIGSAW_ELLIPSOID_DUAL = +202
    cdef indx_t JIGSAW_HFUN_RELATIVE = +300
    cdef indx_t JIGSAW_HFUN_ABSOLUTE = +301
    cdef indx_t JIGSAW_KERN_DELFRONT = +400
    cdef indx_t JIGSAW_KERN_DELAUNAY = +401
    cdef indx_t JIGSAW_BNDS_TRIACELL = +402
    cdef indx_t JIGSAW_BNDS_DUALCELL = +403


    ctypedef struct jigsaw_jig_t:
        indx_t _verbosity
        indx_t _geom_seed
        indx_t _geom_feat
        real_t _geom_eta1
        real_t _geom_eta2
        indx_t _hfun_scal
        real_t _hfun_hmax
        real_t _hfun_hmin
        indx_t _bnds_kern
        indx_t _mesh_dims
        indx_t _mesh_kern
        indx_t _mesh_iter
        indx_t _mesh_top1
        indx_t _mesh_top2
        real_t _mesh_rad2
        real_t _mesh_rad3
        real_t _mesh_siz1
        real_t _mesh_siz2
        real_t _mesh_siz3
        real_t _mesh_off2
        real_t _mesh_off3
        real_t _mesh_snk2
        real_t _mesh_snk3
        real_t _mesh_eps1
        real_t _mesh_eps2
        real_t _mesh_vol3
        indx_t _optm_iter
        real_t _optm_qtol
        real_t _optm_qlim
        indx_t _optm_tria
        indx_t _optm_dual
        indx_t _optm_zip_
        indx_t _optm_div_

    ctypedef  struct  jigsaw_VERT2_t:
        real_t _ppos [2]
        indx_t _itag

    ctypedef struct jigsaw_VERT3_t:
        real_t _ppos [3]
        indx_t _itag

    ctypedef struct jigsaw_EDGE2_t:
        indx_t _node [2]
        indx_t _itag

    ctypedef struct jigsaw_TRIA3_t:
        indx_t _node [3]
        indx_t _itag

    ctypedef struct jigsaw_TRIA4_t:
        indx_t _node [4]
        indx_t _itag

    ctypedef struct jigsaw_VERT2_array_t:
        indx_t _size;
        jigsaw_VERT2_t * _data;

    ctypedef struct jigsaw_VERT3_array_t:
        indx_t _size;
        jigsaw_VERT3_t * _data;

    ctypedef struct jigsaw_EDGE2_array_t:
        indx_t _size
        jigsaw_EDGE2_t * _data

    ctypedef struct jigsaw_TRIA3_array_t:
        indx_t _size;
        jigsaw_TRIA3_t * _data;

    ctypedef struct jigsaw_TRIA4_array_t:
        indx_t _size;
        jigsaw_TRIA4_t * _data;

    ctypedef struct jigsaw_REALS_array_t:
        indx_t _size;
        real_t * _data;

    ctypedef struct jigsaw_msh_t:
        indx_t               _flags;
        jigsaw_VERT2_array_t _vert2;
        jigsaw_VERT3_array_t _vert3;
        jigsaw_REALS_array_t _power;
        jigsaw_EDGE2_array_t _edge2;
        jigsaw_TRIA3_array_t _tria3;
        jigsaw_TRIA4_array_t _tria4;
        jigsaw_REALS_array_t _radii;
        jigsaw_REALS_array_t _xgrid;
        jigsaw_REALS_array_t _ygrid;
        jigsaw_REALS_array_t _zgrid;
        jigsaw_REALS_array_t _value;

    extern indx_t jigsaw_make_mesh(
            jigsaw_jig_t * jcfg,
            jigsaw_msh_t * geom,
            jigsaw_msh_t * init,
            jigsaw_msh_t * hfun,
            jigsaw_msh_t * mesh
    )

    extern void   jigsaw_init_msh_t(
            jigsaw_msh_t   *_mesh
    );

    extern void   jigsaw_init_jig_t(
            jigsaw_jig_t   *_jjig
    );

    extern void  jigsaw_alloc_vert2(
            jigsaw_VERT2_array_t *_xsrc,
            indx_t _size
    );

    extern void  jigsaw_alloc_vert3(
            jigsaw_VERT3_array_t *_xsrc,
            indx_t _size
    );

    extern void  jigsaw_alloc_edge2(
            jigsaw_EDGE2_array_t *_xsrc,
            indx_t _size
    );

    extern void  jigsaw_alloc_tria3(
            jigsaw_TRIA3_array_t *_xsrc,
            indx_t _size
    );

    extern void  jigsaw_alloc_tria4(
            jigsaw_TRIA4_array_t *_xsrc,
            indx_t _size
    );

    extern void  jigsaw_alloc_reals(
            jigsaw_REALS_array_t *_xsrc,
            indx_t _size
    );

    extern void   jigsaw_free_msh_t(
            jigsaw_msh_t   *_mesh
    );

    extern indx_t jigsaw_save_jig_t(
            char *_file,
            jigsaw_jig_t   *_jjig
    );

    extern indx_t jigsaw_load_msh_t(
            char *_file,
            jigsaw_msh_t   *_mesh
    );

    extern indx_t jigsaw_load_jig_t(
            char *_file,
            jigsaw_jig_t   *_jjig
    );

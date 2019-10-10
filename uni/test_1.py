import matplotlib as mpl

mpl.use("tkagg")

import numpy as np
from matplotlib import pyplot as plt

from ctypes import *

ljig = cdll.LoadLibrary("/Users/fmontagna/PycharmProjects/jigsaw/src/libjigsaw64r.so")
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

    def store(self, data):
        self.size = len(data[0])
        data = [tuple(i.tolist()) for i in data]
        # data = np.rec.fromarrays(data, dtype=self.data._type_)
        self.data = (self.data._type_ * self.size)(*[tuple(tuplize(j) for j in i) for i in zip(*data)])

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


jjig = jigsaw_jig_t()
geom = jigsaw_msh_t()
init = jigsaw_msh_t()
mesh = jigsaw_msh_t()

strip = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.046, 0.77], [0.0, 0.77], [0.1, 0.5]])
strip = np.array([[-80.47845458984375, 32.13664245605469], [-80.48204803466797, 32.12731170654297],
                  [-80.48564910888672, 32.11798095703125], [-80.49552917480469, 32.11642837524414],
                  [-80.4991226196289, 32.10709762573242], [-80.50271606445312, 32.0977668762207],
                  [-80.50631713867188, 32.088436126708984], [-80.51618957519531, 32.086883544921875],
                  [-80.51979064941406, 32.077552795410156], [-80.52338409423828, 32.06822204589844],
                  [-80.5269775390625, 32.05889129638672], [-80.53685760498047, 32.05733871459961],
                  [-80.54045104980469, 32.04800796508789], [-80.54405212402344, 32.03867721557617],
                  [-80.5539321899414, 32.03712463378906], [-80.55752563476562, 32.027793884277344],
                  [-80.56111907958984, 32.018463134765625], [-80.56471252441406, 32.009132385253906],
                  [-80.57459259033203, 32.0075798034668], [-80.57819366455078, 31.998249053955078],
                  [-80.581787109375, 31.98891830444336], [-80.58538055419922, 31.97958755493164],
                  [-80.59526062011719, 31.97803497314453], [-80.5988540649414, 31.968704223632812],
                  [-80.60245513916016, 31.959373474121094], [-80.60604858398438, 31.950042724609375],
                  [-80.61592864990234, 31.948490142822266], [-80.61952209472656, 31.939159393310547],
                  [-80.62311553955078, 31.929828643798828], [-80.62671661376953, 31.92049789428711],
                  [-80.6365966796875, 31.9189453125], [-80.64019012451172, 31.90961456298828],
                  [-80.64378356933594, 31.900283813476562], [-80.64737701416016, 31.89095115661621],
                  [-80.65725708007812, 31.889400482177734], [-80.66085815429688, 31.880069732666016],
                  [-80.6644515991211, 31.870738983154297], [-80.67433166503906, 31.869186401367188],
                  [-80.67792510986328, 31.85985565185547], [-80.6815185546875, 31.85052490234375],
                  [-80.68511962890625, 31.8411922454834], [-80.69499206542969, 31.839641571044922],
                  [-80.69859313964844, 31.830310821533203], [-80.70218658447266, 31.820980072021484],
                  [-80.70578002929688, 31.811647415161133], [-80.71566009521484, 31.810096740722656],
                  [-80.7192611694336, 31.800765991210938], [-80.72285461425781, 31.791433334350586],
                  [-80.72644805908203, 31.782102584838867], [-80.736328125, 31.78055191040039],
                  [-80.73992156982422, 31.77121925354004], [-80.74352264404297, 31.76188850402832],
                  [-80.74711608886719, 31.7525577545166], [-80.75699615478516, 31.751007080078125],
                  [-80.76058959960938, 31.741674423217773], [-80.7641830444336, 31.732343673706055],
                  [-80.76778411865234, 31.723012924194336], [-80.77765655517578, 31.721460342407227],
                  [-80.78125762939453, 31.712129592895508], [-80.78485107421875, 31.70279884338379],
                  [-80.79473114013672, 31.70124626159668], [-80.79832458496094, 31.69191551208496],
                  [-80.80191802978516, 31.682584762573242], [-80.8055191040039, 31.673254013061523],
                  [-80.81539916992188, 31.671701431274414], [-80.8189926147461, 31.662370681762695],
                  [-80.82258605957031, 31.653039932250977], [-80.82618713378906, 31.643709182739258],
                  [-80.8360595703125, 31.64215660095215], [-80.83966064453125, 31.63282585144043],
                  [-80.84325408935547, 31.62349510192871], [-80.84684753417969, 31.614164352416992],
                  [-80.85672760009766, 31.612611770629883], [-80.86032104492188, 31.603281021118164],
                  [-80.86392211914062, 31.593950271606445], [-80.86751556396484, 31.584617614746094],
                  [-80.87739562988281, 31.583066940307617], [-80.88098907470703, 31.573734283447266],
                  [-80.88458251953125, 31.564403533935547], [-80.88817596435547, 31.555072784423828],
                  [-80.89803314208984, 31.553510665893555], [-80.90164947509766, 31.544187545776367],
                  [-80.9052505493164, 31.53485870361328], [-80.91507720947266, 31.53328514099121],
                  [-80.91870880126953, 31.523969650268555], [-80.92231750488281, 31.5146427154541],
                  [-80.92591857910156, 31.505313873291016], [-80.93579864501953, 31.50376319885254],
                  [-80.93939208984375, 31.494430541992188], [-80.94298553466797, 31.48509979248047],
                  [-80.94658660888672, 31.47576904296875], [-80.95646667480469, 31.474218368530273],
                  [-80.9600601196289, 31.464885711669922], [-80.96365356445312, 31.455554962158203],
                  [-80.96724700927734, 31.446224212646484], [-80.97712707519531, 31.444671630859375],
                  [-80.98072814941406, 31.435340881347656], [-80.98432159423828, 31.426010131835938],
                  [-80.9879150390625, 31.41667938232422], [-80.99779510498047, 31.41512680053711],
                  [-81.00138854980469, 31.40579605102539], [-81.00498962402344, 31.396465301513672],
                  [-81.00858306884766, 31.387134552001953], [-81.01846313476562, 31.385581970214844],
                  [-81.02205657958984, 31.376251220703125], [-81.02565002441406, 31.366920471191406],
                  [-81.03553009033203, 31.365367889404297], [-81.03913116455078, 31.356037139892578],
                  [-81.042724609375, 31.34670639038086], [-81.04631805419922, 31.33737564086914],
                  [-81.05619812011719, 31.33582305908203], [-81.0597915649414, 31.326492309570312],
                  [-81.06339263916016, 31.317161560058594], [-81.06698608398438, 31.307828903198242],
                  [-81.07686614990234, 31.306278228759766], [-81.08045959472656, 31.296947479248047],
                  [-81.08405303955078, 31.287616729736328], [-81.08765411376953, 31.278284072875977],
                  [-81.09752655029297, 31.2767333984375], [-81.10112762451172, 31.26740264892578],
                  [-81.10472106933594, 31.25806999206543], [-81.10831451416016, 31.24873924255371],
                  [-81.11823272705078, 31.247400283813477], [-81.12123107910156, 31.238399505615234],
                  [-81.12393951416016, 31.230548858642578], [-81.13267517089844, 31.226062774658203],
                  [-81.138671875, 31.21756362915039], [-81.08049774169922, 31.201377868652344],
                  [-80.34441375732422, 32.11109161376953], [-80.44110107421875, 32.18610382080078],
                  [-80.44432067871094, 32.177066802978516], [-80.45419311523438, 32.17551803588867],
                  [-80.4577865600586, 32.16618728637695], [-80.46138763427734, 32.156856536865234],
                  [-80.46498107910156, 32.147525787353516], [-80.47486114501953, 32.14597702026367]])

loop = np.tile(np.arange(len(strip)), 2)
loop = np.array([loop[:len(strip)], loop[1:len(strip) + 1]]).T

geom.vert2.store([
    strip,
    np.zeros(len(strip), dtype=int)])
geom.edge2.store([
    loop,
    np.zeros(len(loop), dtype=int)])

geom.flags = JIGSAW_EUCLIDEAN_MESH

jjig.verbosity = +1

jjig.hfun_scal = JIGSAW_HFUN_ABSOLUTE
jjig.hfun_hmax = 0.01
jjig.hfun_hmin = 0.01

retv = ljig.jigsaw_make_mesh(byref(jjig), byref(geom), 0, 0, byref(mesh))

points = np.array([list(point.ppos) for point in mesh.vert2])
tris = np.array([list(tri.ppos) for tri in mesh.tria3])
print(points)
print(tris)
plt.triplot(points[:, 0], points[:, 1], tris)
plt.scatter(strip[:, 0], strip[:, 1], c="k", marker="x")
ring = np.tile(strip.T, 2).T
plt.plot(ring[:, 0], ring[:, 1])
plt.show()

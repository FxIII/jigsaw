class Mesh:
    def __init__(self):
        self.attributes = [
            ("verts2D", [("pos", ("f8", 2)), ("tag", "i4")], "jigsaw_VERT2_t", "vert2"),
            ("verts3D", [("pos", ("f8", 3)), ("tag", "i4")], "jigsaw_VERT3_t", "vert3"),
            ("powers", [("data", "f8")], "real_t", "power"),
            ("edges", [("node", ("i4", 2)), ("tag", "i4")], "jigsaw_EDGE2_t", "edge2"),
            ("trias", [("node", ("i4", 3)), ("tag", "i4")], "jigsaw_TRIA3_t", "tria3"),
            ("quads", [("node", ("i4", 4)), ("tag", "i4")], "jigsaw_TRIA4_t", "tria4"),
            ("radii", [("data", "f8")], "real_t", "radii"),
            ("xgrid", [("data", "f8")], "real_t", "xgrid"),
            ("ygrid", [("data", "f8")], "real_t", "ygrid"),
            ("zgrid", [("data", "f8")], "real_t", "zgrid"),
            ("values", [("data", "f8")], "real_t", "value")]

    def mkHead(self):
        tmpl = """
    cdef np.ndarray _%s"""
        attrs = "".join(tmpl % i[0] for i in self.attributes)
        return """
cdef class Mesh:
    cdef pygsaw.jigsaw_msh_t msh""" + attrs

    def mkintArgs(self):
        args = ", ".join("%s=0" % i[0] for i in self.attributes)
        return """    
    def __init__(self, pygsaw.indx_t flags, %s):
        pygsaw.jigsaw_init_msh_t(&self.msh)
        self.msh._flags = flags""" % args

    def mkInit(self):
        tmpl = """
        self._{attr} = self.setup{Attr}({attr}) if {attr} > 0 else np.ndarray(0,dtype=np.void)"""

        return "".join(tmpl.format(attr=attr, Attr=attr[0].upper() + attr[1:])
                       for attr, dtype, struct, field in self.attributes)

    def mkProperties(self):
        tmpl = """
    @property
    def {attr}(self):
        return self._{attr}
        """
        return "".join(tmpl.format(attr=i[0]) for i in self.attributes)

    def mkSyncWithBuffers(self):
        tmpl = """
        cdef pygsaw.{struct} [:] {attr}View
        if self.msh._{field}._size > 0:
            {attr}View = <pygsaw.{struct}[:self.msh._{field}._size]> self.msh._{field}._data
            self._{attr} = np.asarray({attr}View, dtype=np.dtype({dtype}, align=True))"""
        attrs = "".join(
            tmpl.format(attr=attr, Attr=attr[0].upper() + attr[1:], dtype="%r" % dtype, struct=struct, field=field)
            for attr, dtype, struct, field in self.attributes)
        return """
    cpdef sync(self):""" + attrs

    def mkSync(self):
        tmpl = """
        cdef np.ndarray {attr}_res
        if self.msh._{field}._size > 0:
            {attr}_res = np.ndarray(
                shape=self.msh._{field}._size,
                dtype=np.dtype({dtype}, align=True))
            {attr}_res.data =  <char *> self.msh._{field}._data
            self._{attr} = {attr}_res"""
        attrs = "".join(
            tmpl.format(attr=attr, Attr=attr[0].upper() + attr[1:], dtype="%r" % dtype, struct=struct, field=field)
            for attr, dtype, struct, field in self.attributes)
        return """
    cpdef sync(self):""" + attrs

    def mkSetup(self):
        tmpl = """
    cdef np.ndarray setup{Attr}(self,size):
        cdef container = np.ndarray(size,dtype=np.dtype({dtype},align=True))
        container[:] = 0
        cdef np.ndarray[pygsaw.{struct}, cast=True] res = container
        self.msh._{field}._data = &res[0]
        self.msh._{field}._size = size
        return container
        """
        return "".join(
            tmpl.format(attr=attr, Attr=attr[0].upper() + attr[1:], dtype="%r" % dtype, struct=struct, field=field)
            for attr, dtype, struct, field in self.attributes)

    def __repr__(self):
        return "\n".join([
            self.mkHead(),
            self.mkintArgs(),
            self.mkInit(),
            self.mkSetup(),
            self.mkSync(),
            self.mkProperties()])


if __name__ == '__main__':
    print Mesh()

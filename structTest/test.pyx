import numpy as np

ctypedef struct test_pass_t:
        double nodes[2]
        int tag

cdef container_pass = np.ndarray(1,dtype=np.dtype([('nodes', ('f8', 2)), ('tag', ('i4',1))],align=True))

cdef test_pass_t [:] res_pass = container_pass
print (res_pass[0])

ctypedef struct test_fail_t:
        int nodes[2]
        int tag

cdef container_fail = np.ndarray(1,dtype=np.dtype([('nodes', ('i4', 2)), ('tag', ('i4',1))],align=True))

cdef test_fail_t [:] res_fail = container_fail
print (res_fail[0])
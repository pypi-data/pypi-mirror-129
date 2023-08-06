cimport cython
import numpy as np
cimport numpy as cnp

cdef cnp.ndarray[cnp.int64_t, ndim=2] create(int n):
    cdef cnp.ndarray[cnp.int64_t, ndim=1] a = np.empty([n**2], dtype=np.int64)
    cdef int i
    for i in range(n**2):
        a[i] = int((i-i/2)**2)
    return a.reshape([n,n])

cpdef cnp.ndarray get_100m_array(int n):
    return create(n)
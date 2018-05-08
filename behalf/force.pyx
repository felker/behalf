cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport sqrt

cpdef accel_cython(tree, double theta, int particle_id, double G, double eps):
    cdef np.ndarray[np.float64_t, ndim=1] grad
    grad = traverse(tree.root, tree.particle_dict[particle_id], theta, particle_id, np.zeros(3), G, eps)
    return grad

cdef traverse(n0, n1, double theta, int idx, np.ndarray[np.float64_t, ndim=1] ret, G, eps):
    if(n0 == n1):
        return
    cdef np.ndarray[np.float64_t, ndim=1] dr
    cdef double size_of_node, r
    
    dr = n0.com - n1.com 
    r = sqrt(dr[0]**2 + dr[1]**2 + dr[2]**2)
    size_of_node = n0.box.xhigh - n0.box.xlow
    
    if(size_of_node/r < theta or n0.leaf):
        ret[0] = ret[0] + G*n0.M*dr[0]/(r**2 + eps**2)**(3./2)
        ret[1] = ret[1] + G*n0.M*dr[1]/(r**2 + eps**2)**(3./2)
        ret[2] = ret[2] + G*n0.M*dr[2]/(r**2 + eps**2)**(3./2)
    else:
        for c in n0.children:
            traverse(c, n1, theta, idx, ret, G, eps)
    return ret


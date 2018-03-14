from __future__ import print_function
import numpy as np
import random
import sqaod
from sqaod.common import checkers
import cuda_dg_annealer as cext
import device

class DenseGraphAnnealer :

    _active_device = device.active_device
    _cext = cext
    
    def __init__(self, W, optimize, dtype, prefdict) :
        self.dtype = dtype
        self._cobj = cext.new(dtype)
	self.assign_device(device.active_device)
        if not W is None :
            self.set_qubo(W, optimize)
        self.set_preferences(prefdict)

    def __del__(self) :
        cext.delete(self._cobj, self.dtype)
        
    def assign_device(self, device) :
        cext.assign_device(self._cobj, device._cobj, self.dtype)

    def seed(self, seed) :
        cext.seed(self._cobj, seed, self.dtype)
        
    def set_qubo(self, W, optimize = sqaod.minimize) :
        checkers.dense_graph.qubo(W)
        W = sqaod.clone_as_ndarray(W, self.dtype)
        cext.set_qubo(self._cobj, W, optimize, self.dtype)
        self._optimize = optimize

    def set_hamiltonian(self, h, J, c) :
        checkers.dense_graph.hJc(W)
        h = sqaod.clone_as_ndarray(h, self.dtype)
        J = sqaod.clone_as_ndarray(J, self.dtype)
        c = sqaod.clone_as_ndarray(c, self.dtype)
        cext.set_hamiltonian(self._cobj, h, J, c, self.dtype)
        self._optimize = sqaod.minimize

    def get_problem_size(self) :
        return cext.get_problem_size(self._cobj, self.dtype)

    def set_preferences(self, prefdict = None, **prefs) :
        if not prefdict is None:
            cext.set_preferences(self._cobj, prefdict, self.dtype)
        cext.set_preferences(self._cobj, prefs, self.dtype)

    def get_preferences(self) :
	return cext.get_preferences(self._cobj, self.dtype)

    def get_optimize_dir(self) :
        return self._optimize

    def get_E(self) :
        return cext.get_E(self._cobj, self.dtype)

    def get_x(self) :
        return cext.get_x(self._cobj, self.dtype)

    def set_x(self, x0, x1) :
        cext.set_x(self._cobj, x0, x1, self.dtype)

    def get_hamiltonian(self) :
        N = self.get_problem_size()
        h = np.empty((N), self.dtype)
        J = np.empty((N, N), self.dtype)
        c = np.empty((1), self.dtype)
        cext.get_hamiltonian(self._cobj, h, J, c, self.dtype)
        return h, J, c[0]

    def get_q(self) :
        return cext.get_q(self._cobj, self.dtype)

    def randomize_spin(self) :
        cext.randomize_spin(self._cobj, self.dtype)

    def calculate_E(self) :
        cext.calculate_E(self._cobj, self.dtype)

    def prepare(self) :
        cext.prepare(self._cobj, self.dtype)

    def make_solution(self) :
        cext.make_solution(self._cobj, self.dtype)

    def anneal_one_step(self, G, kT) :
        cext.anneal_one_step(self._cobj, G, kT, self.dtype)
        

def dense_graph_annealer(W = None, optimize=sqaod.minimize, dtype=np.float64, **prefs) :
    ann = DenseGraphAnnealer(W, optimize, dtype, prefs)
    return ann


if __name__ == '__main__' :

    W = np.array([[-32,4,4,4,4,4,4,4],
                  [4,-32,4,4,4,4,4,4],
                  [4,4,-32,4,4,4,4,4],
                  [4,4,4,-32,4,4,4,4],
                  [4,4,4,4,-32,4,4,4],
                  [4,4,4,4,4,-32,4,4],
                  [4,4,4,4,4,4,-32,4],
                  [4,4,4,4,4,4,4,-32]])
    np.random.seed(0)

    N = 8
    m = 4

    N = 100
    m = 5
    W = sqaod.generate_random_symmetric_W(N, -0.5, 0.5, np.float64)

    ann = dense_graph_annealer(W, dtype=np.float64, n_trotters = m)
    import sqaod.py as py
    #ann = py.dense_graph_annealer(W, n_trotters = m)
    ann.set_qubo(W, sqaod.minimize)
    h, J, c = ann.get_hamiltonian()
    print(h)
    print(J)
    print(c)

    
    Ginit = 5.
    Gfin = 0.001
    
    nRepeat = 2
    kT = 0.02
    tau = 0.995
    
    for loop in range(0, nRepeat) :
        G = Ginit
        ann.prepare()
        ann.randomize_spin()
        while Gfin < G :
            ann.anneal_one_step(G, kT)
            G = G * tau
        ann.make_solution()
        E = ann.get_E()
        q = ann.get_q() 
        print(E)
        print(q)

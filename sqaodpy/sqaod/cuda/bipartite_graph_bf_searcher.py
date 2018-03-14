from __future__ import print_function
import numpy as np
import random
import sys
import sqaod
from sqaod.common import checkers
import cuda_bg_bf_searcher as cext
import device

class BipartiteGraphBFSearcher :

    _cext = cext
    _active_device = device.active_device
    
    def __init__(self, b0, b1, W, optimize, dtype, prefdict) :
        self.dtype = dtype
        self._cobj = cext.new(dtype)
        self.assign_device(device.active_device)
        if not W is None :
            self.set_qubo(b0, b1, W, optimize)
        self.set_preferences(prefdict)
            
    def __del__(self) :
        cext.delete(self._cobj, self.dtype)

    def assign_device(self, dev) :
        cext.assign_device(self._cobj, dev._cobj, self.dtype)

    def set_qubo(self, b0, b1, W, optimize = sqaod.minimize) :
        checkers.bipartite_graph.qubo(b0, b1, W)
        b0, b1, W = sqaod.clone_as_ndarray_from_vars([b0, b1, W], self.dtype)
        self._dim = (b0.shape[0], b1.shape[0])
        cext.set_qubo(self._cobj, b0, b1, W, optimize, self.dtype)
        self._optimize = optimize

    def get_problem_size(self) :
        return cext.get_problem_size(self._cobj, self.dtype)

    def set_preferences(self, prefdict = None, **prefs) :
        if not prefdict is None :
            cext.set_preferences(self._cobj, prefdict, self.dtype)
        cext.set_preferences(self._cobj, prefs, self.dtype)

    def get_preferences(self) :
        return cext.get_preferences(self._cobj, self.dtype);

    def get_optimize_dir(self) :
        return self._optimize

    def get_E(self) :
        return cext.get_E(self._cobj, self.dtype);

    def get_x(self) :
        return cext.get_x(self._cobj, self.dtype);
    
    def prepare(self) :
        cext.prepare(self._cobj, self.dtype);
        
    def make_solution(self) :
        cext.make_solution(self._cobj, self.dtype);
        
    def search_range(self) :
        return cext.search_range(self._cobj, self.dtype)
        
    def search(self) :
        # one liner.  does not accept ctrl+c.
        cext.search(self._cobj, self.dtype);

    def _search(self) :
        self.prepare()
        while True :
            comp, curx0, curx1 = cext.search_range(self._cobj, self.dtype)
            if comp :
                break;
        self.make_solution()
        

def bipartite_graph_bf_searcher(b0 = None, b1 = None, W = None,
                                optimize = sqaod.minimize, dtype = np.float64,
                                **prefs) :
    searcher = BipartiteGraphBFSearcher(b0, b1, W, optimize, dtype, prefs)
    return searcher


if __name__ == '__main__' :
    N0 = 14
    N1 = 5
    
    np.random.seed(0)

    W = np.random.random((N1, N0)) - 0.5
    b0 = np.random.random((N0)) - 0.5
    b1 = np.random.random((N1)) - 0.5
    
    bf = bipartite_graph_bf_searcher(b0, b1, W)
    bf.search()
    E = bf.get_E()
    x = bf.get_x() 
    print(E.shape, E)
    print(x)

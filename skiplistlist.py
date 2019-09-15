"""A skiplist implementation of the List interface

W. Pugh. Skip Lists: A probabilistic alternative to balanced trees. 
  In Communications of the ACM, 33(6), pp. 668-676, June 1990.

W. Pugh. A skip list cookbook. CS-TR-2286.1, University of Maryland, 
  College Park, 1990.
"""
import random
import numpy
from utils import new_array
from base import BaseList

        
class SkiplistList(BaseList):
    class Node(object):
        """A node in a skip list"""
        def __init__(self, x, h):
            self.x = x
            self.next = new_array(h+1)
            self.length = numpy.ones(h+1, dtype=int)

        def height(self):
            return len(self.next) - 1

    def _new_node(self, x, h):
        return SkiplistList.Node(x, h)
        
    def __init__(self, iterable=[]):
        self._initialize()
        self.add_all(iterable)
        
    def _initialize(self):
        self.h = 0
        self.n = 0
        self.sentinel = self._new_node(None, 32)
        self.stack = new_array(self.sentinel.height()+1)
    
    def find_pred(self, i):
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]  # go right in list r
            r -= 1  # go down into list r-1
        return u

    def get(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        return self.find_pred(i).next[0].x

    def set(self, i, x):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.find_pred(i).next[0]
        y = u.x
        u.x = x
        return y
        
    def _add(self, i, w):
        u = self.sentinel
        k = w.height()
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j+u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] += 1
            if r <= k:
                w.next[r] = u.next[r]
                u.next[r] = w
                w.length[r] = u.length[r] - (i-j)
                u.length[r] = i - j
            r -= 1
        self.n += 1
        return u
        
    def add(self, i, x):
        if i < 0 or i > self.n: raise IndexError()
        w = self._new_node(x, self.pick_height())
        if w.height() > self.h:
            self.h = w.height()
        self._add(i, w)
        
    def remove(self, i):
        if i < 0 or i > self.n-1: raise IndexError()
        u = self.sentinel
        r = self.h
        j = -1
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]
            u.length[r] -= 1
            if j + u.length[r] + 1 == i and u.next[r] is not None:
                x = u.next[r].x
                u.length[r] += u.next[r].length[r]
                u.next[r] = u.next[r].next[r]
                if u == self.sentinel and u.next[r] is None:
                    self.h -= 1
            r -= 1
        self.n -= 1
        return x    

    def __iter__(self):
        u = self.sentinel.next[0]
        while u is not None:
            yield u.x
            u = u.next[0]

    def pick_height(self):
        z = random.getrandbits(32)
        k = 0
        while z & 1:
            k += 1
            z = z // 2
        return k

    def truncate(self, i):
        lista = SkiplistList() #para criar um novo nó sentinela
        lista.n = self.n - i # tamanho da nova lista
        lista.h = self.h # a principio de mesma altura da antiga
        
        #percorreremos a lista da mesma forma que remove() porém ajustando o next[r] do nó anterior ao truncamento (novo ultimo nó)
        u = self.sentinel
        r = self.h
        j = -1
        
        while r >= 0:
            while u.next[r] is not None and j + u.length[r] < i:
                j += u.length[r]
                u = u.next[r]  # go right in list r
            if j + u.length[r] >= i:
                lista.sentinel.next[r] = u.next[r] # o novo sentinela aponta para onde o nó u apontava
                u.next[r] = None #o nó u na altura r passa a ser o ultimo, logo aponta para None

            # como não sabemos se o nó com maior altura ficara na lista nova ou antiga, precisamos ajustar o tamanho
            if self.sentinel.next[r] == None: # caso o maior esteja na Nova lista
                self.h -= 1
            if lista.sentinel.next[r] == None: # caso o maior esteja na Antiga lista
                lista.h -= 1
            r -= 1 # go down into list r-1
        
        self.n = i # tamanho da lista antiga atualizado
        
        # por fim retornamos a lista Nova, criada a partir da Antiga
        return lista


        




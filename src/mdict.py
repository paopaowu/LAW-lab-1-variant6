import unittest
from hypothesis import given
import hypothesis.strategies as st
from immutable import *


class node:

    def __init__(self,key,value,rightChild=None,leftChild=None):
        self.k=key
        self.v=value
        self.rc=rightChild
        self.lc=leftChild
        self.count=0

class treeIterator:

    def __init__(self,data):
        self.index=-1
        self.len=len(data)
        self.data=data
    def next(self):
        self.index+=1
        if self.len>self.index:
            return self.data[self.index]
        else:
            raise StopIteration
    def has_next(self):
        if self.len > self.index+1:
            return True
        else:
            return False


class mydict():
    count=0
    root=None
    def getting(self,key):
        if self.count==0:
            return None
        else:
            return self.myfind(key)
    def setting(self,key,value):
        if self.count==0:
            self.root=node(key,value)
            self.count+=1
        else:
            self.myadd(key,value)

    def myiterator(self):
        list = self.mytolist()
        list2 = []
        for i in list:
            list2.append(i)
        return treeIterator(list2)

    def myadd(self, key, value):
        if self.root==None:
            self.root=node(key,value)
            self.count+=1
            return True
        return self.myaddt(self.root,key,value)
    def myaddt(self,n,key,value):
        if key == n.k:
            n.v = value
            return True
        if key < n.k:
            if n.lc == None:
                n.lc = node(key, value)
                self.count+=1
                return True
            else:
                return self.myaddt(n.lc, key, value)
        if key > n.k:
            if n.rc == None:
                n.rc = node(key, value)
                self.count += 1
                return True
            else:
                return self.myaddt(n.rc,key, value)

    def mysize(self):
            return self.count

    def myfromlist(self, list):

        if len(list) == 0:
            return None
        while len(list) != 0:

            temp = list.pop()
            self.myadd(temp[0], temp[1])

    def mytolist(self):
        list = []

        def func(node, list):
            if node != None:
                func(node.lc, list)
                temp = []
                temp.append(node.k)
                temp.append(node.v)
                list.append(temp)

                func(node.rc, list)

        func(self.root, list)
        return list

    def myfind(self, key):
        return self.myfindt(self.root,key)
    def myfindt(self,n,key):
        if n.k == key:
            return n.v
        if key < n.k:
            if n.lc == None:
                return None
            return self.myfindt(n.lc, key)
        if key > n.k:
            if n.lc == None:
                return None
            return self.myfindt(n.rc, key)

    def myfilter(self, func):
        list = self.mytolist()
        list2 = []
        for i in list:
            if func(i[0]):
                list2.append(i)
        return treeIterator(list2)

    def mymap(self, func):
        list = self.mytolist()
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)
        return treeIterator(list2)

    def myreduce(self,func):
        treeitor=self.myiterator()
        if treeitor.has_next():
            res = treeitor.next()[1]
        while treeitor.has_next():
            res = func(res, treeitor.next()[1])
        return res

    def myremove(self, key):
        list = self.mytolist()
        for i in range(len(list)):
            if key == list[i][0]:
                list.pop(i)
                break

        self.root=None
        self.count=0
        self.myfromlist(list)

class TestImmutableList(unittest.TestCase):


    def test_add(self):
        dict = mydict()
        dict.myadd( 1, 2)
        dict.myadd( 2, 2)
        dict.myadd( 0, 2)
        self.assertEqual(dict.mytolist(), [[0,2],[1,2],[2,2]])

    def test_remove(self):
        dict = mydict()
        dict.myadd( 1, 2)
        dict.myadd( 2, 2)
        dict.myadd( 0, 2)

        dict.myremove(1)
        self.assertEqual(dict.mytolist(), [[0,2],[2,2]])

    def test_size(self):
        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        self.assertEqual(dict.mysize(), 3)

    def test_Conversion(self):
        dict=mydict()
        dict.myfromlist([[0,1],[2,1],[3,1]])
        self.assertEqual(dict.mytolist(), [[0, 1], [2, 1], [3, 1]])

    def test_find(self):
        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        self.assertEqual(dict.myfind(2), 2)

    def test_iterator(self) :
        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        list=dict.mytolist()
        itor=dict.myiterator()
        test=[]
        while itor.has_next():
            test.append(itor.next())
        self.assertEqual(test, list)
        self.assertRaises(StopIteration, lambda : itor.next())

    def test_filter(self):
        def func(k):
            if k%2==0:
                return True
            return False

        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        list=dict.mytolist()
        list2 = []
        for i in range(len(list)):
            if func(list[i][0]):
                list2.append(list[i])

        itor=dict.myfilter( func)
        test=[]
        while itor.has_next():
            test.append(itor.next())
        self.assertEqual(test, list2)

    def test_map(self):
        def func(k):
            k+1

        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        list = dict.mytolist()
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)

        itor=dict.mymap(func)
        test=[]
        while itor.has_next():
            test.append(itor.next())
        self.assertEqual(test, list2)

    def test_reduce(self):
        def func(k,j):
            return k+j

        dict = mydict()
        dict.myadd(1, 2)
        dict.myadd(2, 2)
        dict.myadd(0, 2)
        sum=dict.myreduce( func)
        self.assertEqual(sum, 6)

    def test_dict(self):
        d=mydict()
        self.assertEqual(d.getting(1), None)
        d.setting(0,1)
        self.assertEqual(d.getting(0), 1)
        d.setting(0, 2)
        self.assertEqual(d.getting(0), 2)
        d.setting(1, None)
        self.assertEqual(d.getting(1), None)



unittest.main()
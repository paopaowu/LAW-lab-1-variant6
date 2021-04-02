import unittest
from hypothesis import given
import hypothesis.strategies as st
from imdict import *



class TestImmutableList(unittest.TestCase):
    def test_add(self):
        root=node(1,1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        self.assertEqual(mytolist(root), [[0,2],[1,2],[2,2]])
    def test_remove(self):
        root=node(1,1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        root=myremove(root,1)
        self.assertEqual(mytolist(root), [[0,2],[2,2]])

    def test_size(self):
        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        self.assertEqual(mysize(root), 3)

    def test_Conversion(self):
        root=myfromlist([[0,1],[2,1],[3,1]])
        self.assertEqual(mytolist(root), [[0, 1], [2, 1], [3, 1]])
    def test_find(self):
        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        self.assertEqual(myfind(root,2), 2)
    def test_iterator(self) :

        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        list=mytolist(root)
        itor=myiterator(root)
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
        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        list=mytolist(root)
        list2 = []
        for i in range(len(list)):
            if func(list[i][0]):
                list2.append(list[i])

        itor=myfilter(root, func)
        test=[]
        while itor.has_next():
            test.append(itor.next())
        self.assertEqual(test, list2)
    def test_map(self):
        def func(k):
            k+1
        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        list=mytolist(root)
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)

        itor=mymap(root, func)
        test=[]
        while itor.has_next():
            test.append(itor.next())
        self.assertEqual(test, list2)
    def test_reduce(self):
        def func(k,j):
            return k+j
        root = node(1, 1)
        myadd(root, 1, 2)
        myadd(root, 2, 2)
        myadd(root, 0, 2)
        sum=myreduce(myiterator(root), func)
        self.assertEqual(sum, 6)
    def test_dict(self):
        d=dict()
        self.assertEqual(d.getting(1), None)
        d.setting(0,1)
        self.assertEqual(d.getting(0), 1)
        d.setting(0, 2)
        self.assertEqual(d.getting(0), 2)
        d.setting(1, None)
        self.assertEqual(d.getting(1), None)
    def test_concat(self):
        t1=node(1,1)
        myadd(t1, 1, 2)
        myadd(t1, 2, 2)
        myadd(t1, 0, 2)
        t2 = node(-1, 1)
        myadd(t2, -1, 2)
        myadd(t2, 3, 2)
        myadd(t2, 1, 3)
        t3=myconact(t1,t2)
        self.assertEqual(mytolist(t3), [[-1,2],[0,2],[1,2],[2,2],[3,2]])
        t3=myconact(t2,t1)
        self.assertEqual(mytolist(t3), [[-1,2],[0,2],[1,2],[2,2],[3,2]])

unittest.main()
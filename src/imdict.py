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

def myiterator(tree):
    list=mytolist(tree)
    list2=[]
    for i in list:
        list2.append(i)
    return treeIterator(list2)

def myadd(tree,key, value):
    if key == tree.k:
        tree.v=value
        return True
    if key < tree.k:
        if tree.lc == None:
            tree.lc = node(key, value)
            return True
        else:
            return myadd(tree.lc,key,value)
    if key > tree.k:
        if tree.rc == None:
            tree.rc = node(key, value)
            return True
        else:
            return myadd(tree.rc,key, value)

def mysize(tree):
    if tree != None:
        tree.count=0
        tree.count+=1
        tree.count+=mysize(tree.rc)+mysize(tree.lc)
        return tree.count
    else:
        return 0

def myfromlist(list):
    if len(list)==0:
        return None
    temp = list.pop()
    root = node(temp[0], temp[1])
    while len(list)!=0:
        temp=list.pop()
        myadd(root,temp[0],temp[1])
    return root

def mytolist(tree):
    list=[]
    def  func(node,list):
        if node!=None:
            func(node.lc,list)
            temp=[]
            temp.append(node.k)
            temp.append(node.v)
            list.append(temp)
            func(node.rc,list)
    func(tree,list)
    return list

def myfind(tree,key):
    if tree.k==key:
        return tree.v
    if key < tree.k:
        if tree.lc == None:
            return None
        return myfind(tree.lc,key)
    if key > tree.k:
        if tree.lc == None:
            return None
        return myfind(tree.rc, key)

def myfilter(tree, func):
    list=mytolist(tree)
    list2=[]
    for i in list:
        if func(i[0]):
             list2.append(i)
    return treeIterator(list2)

def mymap(tree, func):
    list=mytolist(tree)
    list2=[]
    for i in list:
        i[1]=func(i[1])
        list2.append(i)
    return treeIterator(list2)

def myreduce(treeitor,func):
    if treeitor.has_next():
        res=treeitor.next()[1]
    while treeitor.has_next():
        res=func(res,treeitor.next()[1])
    return res

def myremove(tree, key):
    list=mytolist(tree)
    for i in range(len(list)):
        if key==list[i][0]:
            list.pop(i)
            break
    return myfromlist(list)

def myconact(t1,t2):
    l1=mytolist(t1)
    l2=mytolist(t2)
    l3=[]
    while (0<len(l1) and 0<len(l2)):
        if l1[0][0]<l2[0][0]:
            l3.append(l1.pop(0))
        elif l1[0][0]>l2[0][0]:
            l3.append(l2.pop(0))
        elif l1[0][0]==l2[0][0]:
            if l1[0][1]>l2[0][1]:
                l3.append(l2.pop(0))
                l1.pop(0)
            else:
                l3.append(l1.pop(0))
                l2.pop(0)
    while len(l1)>0:
        l3.append(l1.pop(0))
    while len(l2)>0:
        l3.append(l2.pop(0))
    return myfromlist(l3)
class dict():
    count=0
    root=None
    def getting(self,key):
        if self.count==0:
            return None
        else:
            return myfind(self.root,key)
    def setting(self,key,value):
        if self.count==0:
            self.root=node(key,value)
            self.count+=1
        else:
            myadd(self.root,key,value)


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
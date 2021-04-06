import unittest
import imdict



class TestImmutableList(unittest.TestCase):
    def test_add(self):
        root=imdict.node(1,1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        self.assertEqual(imdict.mytolist(root), [[0,2],[1,2],[2,2]])
    def test_remove(self):
        root=imdict.node(1,1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        root=imdict.myremove(root,1)
        self.assertEqual(imdict.mytolist(root), [[0,2],[2,2]])

    def test_size(self):
        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        self.assertEqual(imdict.mysize(root), 3)

    def test_Conversion(self):
        root=imdict.myfromlist([[0,1],[2,1],[3,1]])
        self.assertEqual(imdict.mytolist(root), [[0, 1], [2, 1], [3, 1]])
    def test_find(self):
        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        self.assertEqual(imdict.myfind(root,2), 2)

    def test_iterator(self) :

        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        list=imdict.mytolist(root)
        itor=iter(root)
        test=[]
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list)

        self.assertRaises(StopIteration, lambda : next(itor))
    def test_filter(self):
        def func(k):
            if k%2==0:
                return True
            return False
        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        list=imdict.mytolist(root)
        list2 = []
        for i in range(len(list)):
            if func(list[i][0]):
                list2.append(list[i])

        itor=imdict.myfilter(root, func)
        test=[]
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list2)
    def test_map(self):
        def func(k):
            k+1
        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        list=imdict.mytolist(root)
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)

        itor=imdict.mymap(root, func)
        test=[]
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list2)
    def test_reduce(self):
        def func(k,j):
            return k+j
        root = imdict.node(1, 1)
        imdict.myadd(root, 1, 2)
        imdict.myadd(root, 2, 2)
        imdict.myadd(root, 0, 2)
        sum=imdict.myreduce(iter(root), func)
        self.assertEqual(sum, 6)
    def test_dict(self):
        d=imdict.dict()
        self.assertEqual(d.getting(1), None)
        d.setting(0,1)
        self.assertEqual(d.getting(0), 1)
        d.setting(0, 2)
        self.assertEqual(d.getting(0), 2)
        d.setting(1, None)
        self.assertEqual(d.getting(1), None)
    def test_concat(self):
        t1=imdict.node(1,1)
        imdict.myadd(t1, 1, 2)
        imdict.myadd(t1, 2, 2)
        imdict.myadd(t1, 0, 2)
        t2 = imdict.node(-1, 1)
        imdict.myadd(t2, -1, 2)
        imdict.myadd(t2, 3, 2)
        imdict.myadd(t2, 1, 3)
        t3=imdict.myconact(t1,t2)
        self.assertEqual(imdict.mytolist(t3), [[-1,2],[0,2],[1,2],[2,2],[3,2]])
        t3=imdict.myconact(t2,t1)
        self.assertEqual(imdict.mytolist(t3), [[-1,2],[0,2],[1,2],[2,2],[3,2]])

unittest.main()
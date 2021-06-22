import unittest
from mdict import *
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):

    def test_add(self):
        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 'cat')
        dict.add(0, 'dog')
        self.assertEqual(dict.to_list(), [[0, 'dog'], [1, 2], [2, 'cat']])

    def test_remove(self):
        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 'cat')
        dict.add(0, 'dog')

        dict.remove(1)
        self.assertEqual(dict.to_list(), [[0, 'dog'], [2, 'cat']])

    def test_size(self):
        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 'cat')
        dict.add(0, 'dog')
        self.assertEqual(dict.size(), 3)

    def test_find(self):
        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 'cat')
        dict.add(0, 'dog')
        self.assertEqual(dict.find(2), 'cat')

    def test_iterator(self):
        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 'cat')
        dict.add(0, 'dog')
        dicList = []
        for dic in dict:
            dicList.append(dic)
        self.assertEqual(dicList, [[0, 'dog'], [1, 2], [2, 'cat']])
        itrate1 = iter(dict)
        itrate2 = iter(dict)
        leng = len(dicList)
        while(leng):
            self.assertEqual(next(itrate1),next(itrate2))
            leng-=1


    def test_filter(self):
        def func(k):
            if k % 2 == 0:
                return True
            return False

        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 2)
        dict.add(0, 2)
        list = dict.to_list()
        list2 = []
        for i in range(len(list)):
            if func(list[i][0]):
                list2.append(list[i])

        itor = dict.filter(func)
        test = []
        while itor.has_next():
            test.append(itor.__next__())
        self.assertEqual(test, list2)

    def test_map(self):
        def func(k):
            k + 1

        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 2)
        dict.add(0, 2)
        list = dict.to_list()
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)

        itor = dict.map(func)
        test = []
        while itor.has_next():
            test.append(itor.__next__())
        self.assertEqual(test, list2)

    def test_reduce(self):
        def func(k, j):
            return k + j

        dict = mydict()
        dict.add(1, 2)
        dict.add(2, 2)
        dict.add(0, 2)
        sum = dict.reduce(func)
        self.assertEqual(sum, 6)

    def test_dict(self):
        d = mydict()
        self.assertEqual(d.find(1), None)
        d.add(0, 1)
        self.assertEqual(d.find(0), 1)
        d.add(0, 'dog')
        self.assertEqual(d.find(0), 'dog')
        d.add(1, None)
        self.assertEqual(d.find(1), None)

    def test_from_List(self):
        list = [[2, 3], [0, 1], [1, 2]]
        dict = mydict()
        dict.from_list(list)
        self.assertEqual([dict.root.k, dict.root.v], [1, 2])
        self.assertEqual([dict.root.lc.k, dict.root.lc.v], [0, 1])
        self.assertEqual([dict.root.rc.k, dict.root.rc.v], [2, 3])

    def test_to_List(self):
        dict = mydict()
        dict.add(0, 2)
        dict.add(1, 3)
        dict.add(2, 4)
        self.assertEqual(dict.to_list(), [[0, 2], [1, 3], [2, 4]])

    def test_mconcat(self):
        dict1 = mydict()
        dict2 = mydict()
        dict1.add(4, 1)
        dict1.add(1, 2)
        dict1.add(2, 2)
        dict1.add(0, 2)
        dict2.add(-1, 1)
        dict2.add(-1, 2)
        dict2.add(3, 2)
        dict2.add(1, 3)
        dict3 = mydict.mconcat(dict1, dict2)
        self.assertEqual(dict3.to_list(), [[-1, 2], [0, 2], [1, 2], [2, 2], [3, 2], [4, 1]])
        dict3 = mydict.mconcat(dict2, dict1)
        self.assertEqual(dict3.to_list(), [[-1, 2], [0, 2], [1, 2], [2, 2], [3, 2], [4, 1]])

    @given(st.lists(st.lists(st.integers(), min_size=2, max_size=2)))
    def test_from_list_to_list_equality(self, a):
        # The generated test data is processed
        dict = mydict()
        d = {}
        for i in a:
            d[i[0]] = i[1]
        key_value = list(d.keys())
        key_value.sort()
        value_list = list(d.values())
        c = []
        for i in range(len(key_value)):
            c.append([key_value[i], value_list[i]])
        dict.from_list(c)
        b = dict.to_list()
        self.assertEqual(b, c)

    @given(st.lists(st.lists(st.integers(), min_size=2, max_size=2)))
    def test_monoid_identity(self, a):
        # The generated test data is processed
        dict1 = mydict()
        dict2 = mydict()
        d = {}
        for i in a:
            d[i[0]] = i[1]
        key_value = list(d.keys())
        key_value.sort()
        value_list = list(d.values())
        c = []
        for i in range(len(key_value)):
            c.append([key_value[i], value_list[i]])
        dict2.from_list(c)
        dict2 = mydict.mconcat(dict1.mempty(), dict2)
        self.assertEqual(dict2.to_list(), c)

        dict1.from_list(c)
        dict1 = mydict.mconcat(dict1, dict2.mempty())
        self.assertEqual(dict1.to_list(), c)


if __name__ == '__main__':
    unittest.main()

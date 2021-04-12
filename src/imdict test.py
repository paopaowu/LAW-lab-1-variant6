import unittest
import imdict
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):
    def test_add(self):
        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        self.assertEqual(imdict.to_list(root), [[0, 2], [1, 2], [2, 2]])

    def test_remove(self):
        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        root = imdict.remove(root, 1)
        self.assertEqual(imdict.to_list(root), [[0, 2], [2, 2]])

    def test_size(self):
        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        self.assertEqual(imdict.size(root), 3)

    def test_to_list(self):
        root = imdict.node(0, 1)
        root = imdict.add(root, 2, 1)
        root = imdict.add(root, 3, 1)
        self.assertEqual(imdict.to_list(root), [[0, 1], [2, 1], [3, 1]])

    def test_from_list(self):
        root = imdict.from_list([[0, 1], [2, 1], [3, 1]])
        self.assertEqual(imdict.to_list(root), [[0, 1], [2, 1], [3, 1]])

    @given(st.lists(st.lists(st.integers(), min_size=2, max_size=2)))
    def test_from_list_to_list_equality(self, a):
        # The generated test data is processed
        d = {}
        for i in a:
            d[i[0]] = i[1]
        key_value = list(d.keys())
        key_value.sort()
        value_list = list(d.values())
        c = []
        for i in range(len(key_value)):
            c.append([key_value[i], value_list[i]])

        root = imdict.from_list(c)
        b = imdict.to_list(root)
        self.assertEqual(b, c)

    @given(st.lists(st.lists(st.integers(), min_size=2, max_size=2)))
    def test_monoid_identity(self, a):
        # The generated test data is processed
        d = {}
        for i in a:
            d[i[0]] = i[1]
        key_value = list(d.keys())
        key_value.sort()
        value_list = list(d.values())
        c = []
        for i in range(len(key_value)):
            c.append([key_value[i], value_list[i]])

        self.assertEqual(imdict.to_list(imdict.mconcat(imdict.mempty(), imdict.from_list(c))), c)
        self.assertEqual(imdict.to_list(imdict.mconcat(imdict.from_list(c), imdict.mempty())), c)

    def test_find(self):
        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        self.assertEqual(imdict.find(root, 2), 2)

    def test_iterator(self):

        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        list = imdict.to_list(root)
        itor = iter(root)
        test = []
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list)

        self.assertRaises(StopIteration, lambda: next(itor))

    def test_filter(self):
        def func(k):
            if k % 2 == 0:
                return True
            return False

        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        list = imdict.to_list(root)
        list2 = []
        for i in range(len(list)):
            if func(list[i][0]):
                list2.append(list[i])

        itor = imdict.filter(root, func)
        test = []
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list2)

    def test_map(self):
        def func(k):
            k + 1

        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        list = imdict.to_list(root)
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)

        itor = imdict.map(root, func)
        test = []
        while itor.has_next():
            test.append(next(itor))
        self.assertEqual(test, list2)

    def test_reduce(self):
        def func(k, j):
            return k + j

        root = imdict.node(1, 1)
        root = imdict.add(root, 1, 2)
        root = imdict.add(root, 2, 2)
        root = imdict.add(root, 0, 2)
        sum = imdict.reduce(iter(root), func)
        self.assertEqual(sum, 6)

    def test_dict(self):
        d = imdict.dict()
        self.assertEqual(d.getting(1), None)
        d.setting(0, 1)
        self.assertEqual(d.getting(0), 1)
        d.setting(0, 2)
        self.assertEqual(d.getting(0), 2)
        d.setting(1, None)
        self.assertEqual(d.getting(1), None)

    def test_mconcat(self):
        t1 = imdict.node(1, 1)
        t1 = imdict.add(t1, 1, 2)
        t1 = imdict.add(t1, 2, 2)
        t1 = imdict.add(t1, 0, 2)
        t2 = imdict.node(-1, 1)
        t2 = imdict.add(t2, -1, 2)
        t2 = imdict.add(t2, 3, 2)
        t2 = imdict.add(t2, 1, 3)
        t3 = imdict.mconcat(t1, t2)
        self.assertEqual(imdict.to_list(t3), [[-1, 2], [0, 2], [1, 2], [2, 2], [3, 2]])
        t3 = imdict.mconcat(t2, t1)
        self.assertEqual(imdict.to_list(t3), [[-1, 2], [0, 2], [1, 2], [2, 2], [3, 2]])


unittest.main()

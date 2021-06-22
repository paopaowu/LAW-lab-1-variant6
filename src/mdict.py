class node:
    def __init__(self, key, value, rightChild=None, leftChild=None):
        self.k = key
        self.v = value
        self.rc = rightChild
        self.lc = leftChild
        self.count = 0


class treeIterator:

    def __init__(self, data):
        self.iter_count = -1
        self.len = len(data)
        self.data = data

    def __iter__(self):
        return self

    def __next__(self):
        self.iter_count += 1
        if self.len > self.iter_count:
            return self.data[self.iter_count]
        else:
            raise StopIteration

    def has_next(self):
        if self.len > self.iter_count + 1:
            return True
        else:
            return False


class mydict():
    count = 0
    root = None

    def __iter__(self):
        list = self.to_list()
        list2 = []
        for i in list:
            list2.append(i)
        return treeIterator(list2)

    def add(self, key, value):
        if self.root == None:
            self.root = node(key, value)
            self.count += 1
            return True

        def func(n, key, value):
            if key == n.k:
                n.v = value
                return True
            if key < n.k:
                if n.lc == None:
                    n.lc = node(key, value)
                    self.count += 1
                    return True
                else:
                    return func(n.lc, key, value)
            if key > n.k:
                if n.rc == None:
                    n.rc = node(key, value)
                    self.count += 1
                    return True
                else:
                    return func(n.rc, key, value)

        return func(self.root, key, value)

    def size(self):
        return self.count

    def from_list(self, list):
        list_copy = list[:]
        if len(list_copy) == 0:
            return None
        while len(list_copy) != 0:
            temp = list_copy.pop()
            self.add(temp[0], temp[1])

    def to_list(self):
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

    def find(self, key):
        if self.count == 0:
            return None
        def myfindt(n, key):
            if n.k == key:
                return n.v
            if key < n.k:
                if n.lc == None:
                    return None
                return myfindt(n.lc, key)
            if key > n.k:
                if n.lc == None:
                    return None
                return myfindt(n.rc, key)

        return myfindt(self.root, key)

    def filter(self, func):
        list = self.to_list()
        list2 = []
        for i in list:
            if func(i[0]):
                list2.append(i)
        return treeIterator(list2)

    def map(self, func):
        list = self.to_list()
        list2 = []
        for i in list:
            i[1] = func(i[1])
            list2.append(i)
        return treeIterator(list2)

    def reduce(self, func):
        treeitor = self.__iter__()
        if treeitor.has_next():
            res = treeitor.__next__()[1]
        while treeitor.has_next():
            res = func(res, treeitor.__next__()[1])
        return res

    def remove(self, key):
        list = self.to_list()
        for i in range(len(list)):
            if key == list[i][0]:
                list.pop(i)
                break

        self.root = None
        self.count = 0
        self.from_list(list)

    def mconcat(dict1, dict2):
        if (dict1 != None and dict2 != None):
            l1 = dict1.to_list()
            l2 = dict2.to_list()
        else:
            if (dict1 == None and dict2 != None):
                l1 = []
                l2 = dict2.to_list()
            if (dict2 == None and dict1 != None):
                l2 = []
                l1 = dict1.to_list()
            if (dict1 == None and dict2 == None):
                l1 = []
                l2 = []

        l3 = []
        while (0 < len(l1) and 0 < len(l2)):
            if l1[0][0] != l2[0][0]:
                l3.append(l1.pop(0) if l1[0][0] < l2[0][0] else l2.pop(0))
            else:
                if l1[0][1] > l2[0][1]:
                    l3.append(l2.pop(0))
                    l1.pop(0)
                else:
                    l3.append(l1.pop(0))
                    l2.pop(0)
        while len(l1) > 0:
            l3.append(l1.pop(0))
        while len(l2) > 0:
            l3.append(l2.pop(0))
        dic = mydict()
        dic.from_list(l3)
        return dic

    def mempty(self):
        return None

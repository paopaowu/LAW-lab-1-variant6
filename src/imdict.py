class node:
    def __init__(self, key, value, rightChild=None, leftChild=None):
        self.k = key
        self.v = value
        self.rc = rightChild
        self.lc = leftChild
        self.count = 0

    def __iter__(self):
        self.list = to_list(self)
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1
        if len(self.list) <= self.iter_count:
            raise StopIteration
        return self.list[self.iter_count]

    def has_next(self):
        if len(self.list) <= self.iter_count + 1:
            return False
        return True


def add(tree, key, value):
    copy_tree = copy(tree)

    def func(tree, key, value):
        if key == tree.k:
            tree.v = value
            return True
        if key < tree.k:
            if tree.lc == None:
                tree.lc = node(key, value)
                return True
            else:
                return func(tree.lc, key, value)
        if key > tree.k:
            if tree.rc == None:
                tree.rc = node(key, value)
                return True
            else:
                return func(tree.rc, key, value)

    func(copy_tree, key, value)
    return copy_tree


def copy(tree):
    if tree == None:
        return None
    copy_tree = node(tree.k, tree.v)
    copy_tree.rc = copy(tree.rc)
    copy_tree.lc = copy(tree.lc)
    return copy_tree


def size(tree):
    if tree != None:
        tree.count = 0
        tree.count += 1
        tree.count += size(tree.rc) + size(tree.lc)
        return tree.count
    else:
        return 0


def from_list(list):
    if len(list) == 0:
        return None
    temp = list[0]
    root = node(temp[0], temp[1])
    i = 1
    while i < len(list):
        temp = list[i]
        root = add(root, temp[0], temp[1])
        i += 1
    return root


def to_list(tree):
    list = []

    def func(node, list):
        if node != None:
            func(node.lc, list)
            temp = []
            temp.append(node.k)
            temp.append(node.v)
            list.append(temp)
            func(node.rc, list)

    func(tree, list)
    return list


def find(tree, key):
    if tree.k == key:
        return tree.v
    if key < tree.k:
        if tree.lc == None:
            return None
        return find(tree.lc, key)
    if key > tree.k:
        if tree.lc == None:
            return None
        return find(tree.rc, key)


def filter(tree, func):
    list = to_list(tree)
    list2 = []
    for i in list:
        if func(i[0]):
            list2.append(i)
    root = from_list(list2)
    return iter(root)


def map(tree, func):
    list = to_list(tree)
    list2 = []
    for i in list:
        i[1] = func(i[1])
        list2.append(i)
    root = from_list(list2)
    return iter(root)


def reduce(treeitor, func):
    if treeitor.has_next():
        res = next(treeitor)[1]
    while treeitor.has_next():
        res = func(res, next(treeitor)[1])
    return res


def remove(tree, key):
    list = to_list(tree)
    for i in range(len(list)):
        if key == list[i][0]:
            list.pop(i)
            break
    return from_list(list)


def mconcat(t1, t2):
    l1 = to_list(t1)
    l2 = to_list(t2)
    l3 = []
    while (0 < len(l1) and 0 < len(l2)):
        if l1[0][0] < l2[0][0]:
            l3.append(l1.pop(0))
        elif l1[0][0] > l2[0][0]:
            l3.append(l2.pop(0))
        elif l1[0][0] == l2[0][0]:
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
    return from_list(l3)


def mempty():
    return None


class dict():
    count = 0
    root = None

    def getting(self, key):
        if self.count == 0:
            return None
        else:
            return find(self.root, key)

    def setting(self, key, value):
        if self.count == 0:
            self.root = node(key, value)
            self.count += 1
        else:
            self.root = add(self.root, key, value)

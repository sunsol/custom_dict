# coding:utf-8

# 设置所使用的dict文件列表，默认使用dicts目录中所有python.*.dict
dicts = ['python.pyparsing.dict',
         'python.stdlib.zh_CN.dict', 'python.bs4.zh_CN.dict']

# 设置补全方式，free表示由指定按键来补全，default表示使用Ctrl-x Ctrl-u来补全
# complete_method = 'default'

# 设置按键
# first用于free方式下调出补全的按键
# kind用于轮询不同类型
# up用于显示上一层或转到树状提示
# down用于显示下一层
# free方式下好像不能设置'down':'C-L',原因不明
# 默认map_keys = {'kind': '<C-F>', 'up': '<C-H>', 'down': '<C-L>', 'first': '<C-T>'}

# 设置智能补全


def complete(self):
    NOUSEKIND = '_'
    import re
    WORD = r'([0-9_a-zA-Z.]+)'

    def do_from_import(line):
        t = re.match(r'\s*from\s+%s\s+import\s+$' % WORD, line)
        if t:
            words = t.groups()[0]
            if words:
                words = words.split('.')
                tree = self.nodetree
                for word in words:
                    tree = tree.search(lambda x: x.word == word and x.kind == 'p')
                result = []
                for node in tree.childs:
                    result.extend(node.filter(lambda x: x.kind != NOUSEKIND))
                return result
        return []

    def do_from(line):
        t = re.match(r'\s*from\s+%s?$' % WORD, line)
        if t:
            words = t.groups()[0]
            if words:
                words = words.split('.')[:-1]
                tree = self.nodetree
                for word in words:
                    tree = tree.search(
                        lambda x: x.word == word and x.kind == 'p')
                result = []
                for node in tree.childs:
                    result.extend(node.search(lambda x: x.kind == 'p').childs)
                return result
            else:
                return self.nodetree.search(lambda x: x.kind == 'p').childs
        return []

    def do_import(line):
        t = re.match(r'\s*import\s+%s?$' % WORD, line)
        if t:
            words = t.groups()[0]
            if words:
                words = words.split('.')[:-1]
                tree = self.nodetree
                for word in words:
                    tree = tree.search(
                        lambda x: x.word == word and x.kind == 'p')
                result = []
                for node in tree.childs:
                    result.extend(node.search(lambda x: x.kind == 'p').childs)
                return result
            else:
                a = self.nodetree.search(lambda x: x.kind == 'p')
                return a.childs
        return []

    def do_class(line):
        t = re.match(r'\s*class\s+\w+\($', line)
        if t:
            return list(self.nodetree.filter(lambda x: x.kind in 'cte'))
        return []

    def do_dot(line):
        t = re.match(r'.*\W%s\.$' % WORD, line)
        if t:
            words = t.groups()[0]
            if words:
                words = words.split('.')
                tree = self.nodetree
                for word in words:
                    tree = tree.search(lambda x: x.word == word)
                result = []
                for node in tree.childs:
                    result.extend(node.filter(lambda x: x.kind != NOUSEKIND))
                if result:
                    return result
            return list(self.nodetree.filter(lambda x: x.kind in 'dm'))
        return []

    pos = self.getpos()
    line = self.getline(pos)
    t = do_from_import(line)
    if t:
        return pos, t
    t = do_from(line)
    if t:
        return pos, t
    t = do_import(line)
    if t:
        return pos, t
    t = do_class(line)
    if t:
        return pos, t
    t = do_dot(line)
    if t:
        return pos, t
    return pos, list(self.nodetree.filter(lambda x: x.kind not in 'dm' and x.kind != NOUSEKIND))



# 设置排序方式
# def sortresult(base):
#     def sortkey(x):
#         key = '%02d' % x.word.index(base) if base in x.word else '99'
#         key += '%02d' % x.word.lower().index(
#             base.lower()) if base.lower() in x.word.lower() else '99'
#         key += x.sortkey
#         return key
#     return sortkey

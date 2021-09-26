# -*- coding: utf-8 -*-
"""FP-Growth.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wpQd8SbxhyeClYTyP6EE0Dhgj9A31Ou9

# FP_Growth Algorithm

## Import
"""

import pandas as pd
import numpy as np
import itertools
from collections import defaultdict, namedtuple

"""## Define Function"""

def init(df):
  clist=[]
  for i in range(len(df.columns)):
    if i >=2:
      clist.append(df.columns[i])

  dfnk=df.drop(clist,axis=1)
  return dfnk

def check_data(list):
  zlist=[]
  plist=[]
  for i in range(len(list)):
    if len(list[i])==0:
      zlist.append(i)
  for i in range(len(zlist)):
    plist.append(zlist.pop())
  for i in plist:
    del list[i]
  return list

def find_frequent_itemsets(transactions, minimum_support, include_support=False):

    items = defaultdict(lambda: 0)
    if 0 < minimum_support <= 1:
        minimum_support = minimum_support * len(transactions)
    for transaction in transactions:
        for item in transaction:
            items[item] += 1

    items = dict(
        (item, support) for item, support in items.items() if support >= minimum_support
    )
    def clean_transaction(transaction):
        transaction = filter(lambda v: v in items, transaction)
        transaction = sorted(transaction, key=lambda v: items[v], reverse=True)
        return transaction

    master = FPTree()
    for transaction in list(map(clean_transaction, transactions)):
        master.add(transaction)

    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s

    for itemset in find_with_suffix(master, []):
        yield itemset

def maxage_of_df(df):
  lar=0
  index=0
  for i in range(len(df)):
    if df[df.columns[0]][i]>lar:
      lar=df[df.columns[0]][i]
      index=i
  return index

def data_num(df):
  return len(df)

class FPTree(object):

    Route = namedtuple("Route", "head tail")

    def __init__(self):

        self._root = FPNode(self, None, None)


        self._routes = {}

    @property
    def root(self):

        return self._root

    def add(self, transaction):

        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                next_point.increment()
            else:

                next_point = FPNode(self, item)
                point.add(next_point)

                self._update_route(next_point)

            point = next_point

    def _update_route(self, point):
        assert self is point.tree

        try:
            route = self._routes[point.item]
            route[1].neighbor = point
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            self._routes[point.item] = self.Route(point, point)

    def items(self):

        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):

        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

    def inspect(self):
        print("Tree:")
        self.root.inspect(1)

        print()
        print("Routes:")
        for item, nodes in self.items():
            print("  %r" % item)
            for node in nodes:
                print("    %r" % node)

def subs(l):
    assert type(l) is list
    if len(l) == 1:
        return [l]
    x = subs(l[1:])
    return x + [[l[0]] + y for y in x]

def creat_result(conf_list,min_confidence=0.3):
  tem8_list=[[],[],[],[],[]]
  for i in range(len(df)):
    for j in range(len(conf_list[3*i+2])):
      if conf_list[3*i+2][j]>=min_confidence:
    #    print('')
    #    print("Rule: " + str(conf_list[3*i][j]) + " -> " + str(conf_list[3*i][-1]-conf_list[3*i][j]))
    #    print("Support: " + str(conf_list[3*i+1][-1]))
    #    print("Confidence: " + str(conf_list[3*i+2][j]))
    #    print('')
    #    print("=====================================>")
        tem8_list[0].append(conf_list[3*i][j])
        tem8_list[1].append(' --> ')
        tem8_list[2].append(conf_list[3*i][-1]-conf_list[3*i][j])
        tem8_list[3].append(conf_list[3*i+1][-1])
        tem8_list[4].append(conf_list[3*i+2][j])
  df_res=pd.DataFrame()
  df_res['Body']=tem8_list[0]
  df_res['Implies']=tem8_list[1]
  df_res['Head']=tem8_list[2]
  df_res['Support']=tem8_list[3]
  df_res['Confidence']=tem8_list[4]
  return df_res



def creat_support_df(item_list):
  df=pd.DataFrame()
  df['item_name']=item_list[0]
  df['support']=item_list[1]

  tem3_list=[]
  tem4_list=[]
  for i in range(len(df)):
    tem3_list.append(len(df['item_name'][i]))
    tem4_list.append(pow(2,len(df['item_name'][i])))
  df['item_len']=tem3_list
  df['subset_num']=tem4_list

  tem5_list=[]
  for i in range(len(df)):
    tem5_list.append(3*i)
  df['conf_index']=tem5_list
  tem6_list=[]
  for i in range(len(df)):
    tem6_list.append(3*i+1)
  df['conf_n_index']=tem6_list
  tem7_list=[]
  for i in range(len(df)):
    tem7_list.append(3*i+2)
  df['conf_t_index']=tem7_list
  return df

class FPNode(object):

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):

        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if child.item not in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        return self._tree

    @property
    def item(self):
        return self._item

    @property
    def count(self):
        return self._count

    def increment(self):
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def root(self):
        return self._item is None and self._count is None

    @property
    def leaf(self):
        return len(self._children) == 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a parent.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")
        self._parent = value

    @property
    def neighbor(self):
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a neighbor.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")
        self._neighbor = value

    @property
    def children(self):
        return tuple(self._children.values())

    def inspect(self, depth=0):
        print(("  " * depth) + repr(self))
        for child in self.children:
            child.inspect(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item, self.count)

def generate_data(max,min,df):
  datalistk=[] # 初始datalist
  for i in range(max):
    datalistk.append([])
  for i in range(len(df)):
    datalistk[df[df.columns[0]][i]-min].append(df[df.columns[1]][i])
  return datalistk

def set_data(list):
  datalistk_set=[]
  for i in range(len(list)):
    datalistk_set.append(set(list[i]))
  return datalistk_set

def conditional_tree_from_paths(paths):

    tree = FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:

                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None


    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    return tree

def set_init(index):
  item_list=[[]]
  for i in range(len(index)):
    item_list[0].append(set([index[i]]))
  return item_list

def creat_conf_list(df):
  # 找出所有subset
  conf_list=[]
  for i in range(len(df)):
    conf_list.append([])
    conf_list.append([])
    conf_list.append([])
    for j in df['item_name'][i]:
      conf_list[df['conf_index'][i]].append(set([j]))
  for i in range(len(df)):
    item_len=df['item_len'][i]
    for m in range(item_len-1):
      for j in range(len(conf_list[3*i])-1):
        for k in range(j+1,len(conf_list[3*i]),1):
          st=conf_list[3*i][j].union(conf_list[3*i][k])
          if len(st)==m+2:
            stu=0
            for l in range(len(conf_list[3*i])):
              if st == conf_list[3*i][l]:
                stu=1
            if stu==0:
              conf_list[3*i].append(st)
  # 計算出所有的confidence
  for i in range(len(df)):
    for j in range(len(conf_list[3*i])):
      for k in range(len(df)):
        item=df['item_name'][k]
        if conf_list[3*i][j]==item:
          conf_list[3*i+1].append(df['support'][k])
#  print(conf_list)
#  print(len(conf_list))
  for i in range(len(df)):

    if len(conf_list[3*i])-1>0:
      for j in range(len(conf_list[3*i])-1):
#        print(conf_list[3*i])
        conf=conf_list[3*i+1][-1]/conf_list[3*i+1][j]
        conf_list[3*i+2].append(conf)
  return conf_list

def get_num(list):
  return len(list)

"""## IBM

### Pretreatment
"""

def main_IBM(min_support=0.1,min_confidence=0.3):
  dfk=pd.read_csv('./input_data/IBM_Generator_Data.csv')
  print('IBM done')
  dfk=dfk.drop(columns=[dfk.columns[1]])
  dfnk=init(dfk)
  x=maxage_of_df(dfnk)
  mini=min(dfnk[dfnk.columns[0]])
  datalistk=generate_data(x,mini,dfnk)
  datalistk=check_data(list=datalistk)
  index=dfnk.groupby([dfnk.columns[1]]).count().index
  datalistk_set= set_data(list = datalistk)
  item_list = set_init(index=index)
  num= get_num(list =datalistk_set)
  minsup=min_support*num
  item_list=[[],[]]
  for item in find_frequent_itemsets(datalistk_set, minsup):
    item_list[0].append(item)
  for i in range(len(item_list[0])):
    item_list[0][i]=set(item_list[0][i])
  for i in range(len(item_list[0])):
    num_pat=0
    for j in range(num):
      st1=item_list[0][i]
      st2=item_list[0][i]& datalistk_set[j]
      if st2 ==st1:
        num_pat += 1
    num_pat=num_pat/num
    item_list[1].append(num_pat)
  df = creat_support_df(item_list)
  conf_list=creat_conf_list(df)
  res_IBM=creat_result(conf_list,min_confidence)
  res_IBM.to_csv('./output_data_fp_growth/IBM_Generator_Data_result.csv',index=False,header=True)
  print('IBM Success')

"""## kaggle data"""

if __name__ =='__main__':
  min_support=0.1
  min_confidence=0.3
  dfk=pd.read_csv('./input_data/IBM_Generator_Data.csv')
  print('IBM done')
  dfk=dfk.drop(columns=[dfk.columns[1]])
  dfnk=init(dfk)
  x=maxage_of_df(dfnk)
  mini=min(dfnk[dfnk.columns[0]])
  datalistk=generate_data(x,mini,dfnk)
  datalistk=check_data(list=datalistk)
  index=dfnk.groupby([dfnk.columns[1]]).count().index
  datalistk_set= set_data(list = datalistk)
  item_list = set_init(index=index)
  num= get_num(list =datalistk_set)
  minsup=min_support*num
  item_list=[[],[]]
  for item in find_frequent_itemsets(datalistk_set, minsup):
    item_list[0].append(item)
  for i in range(len(item_list[0])):
    item_list[0][i]=set(item_list[0][i])
  for i in range(len(item_list[0])):
    num_pat=0
    for j in range(num):
      st1=item_list[0][i]
      st2=item_list[0][i]& datalistk_set[j]
      if st2 ==st1:
        num_pat += 1
    num_pat=num_pat/num
    item_list[1].append(num_pat)
  df = creat_support_df(item_list)
  conf_list=creat_conf_list(df)
  res_IBM=creat_result(conf_list,min_confidence)
  res_IBM.to_csv('./output_data_fp_growth/IBM_Generator_Data_result.csv',index=False,header=True)
  print('IBM Success')

  min_support=0.5
  min_confidence=0.3
  dfk=pd.read_csv('./input_data/Kaggle_UCI_Data.csv')
  print('kaggle done')
  dfnk=init(dfk)
  x=maxage_of_df(dfnk)
  mini=min(dfnk[dfnk.columns[0]])
  datalistk=generate_data(x,mini,dfnk)
  datalistk=check_data(list=datalistk)
  index=dfnk.groupby([dfnk.columns[1]]).count().index
  datalistk_set= set_data(list = datalistk)
  item_list = set_init(index=index)
  num= get_num(list =datalistk_set)
  minsup=min_support*num
  item_list=[[],[]]
  for item in find_frequent_itemsets(datalistk_set, minsup):
    item_list[0].append(item)
  for i in range(len(item_list[0])):
    item_list[0][i]=set(item_list[0][i])
  for i in range(len(item_list[0])):
    num_pat=0
    for j in range(num):
      st1=item_list[0][i]
      st2=item_list[0][i]& datalistk_set[j]
      if st2 ==st1:
        num_pat += 1
    num_pat=num_pat/num
    item_list[1].append(num_pat)
  df = creat_support_df(item_list)
  conf_list=creat_conf_list(df)
  res_Kaggle=creat_result(conf_list,min_confidence)
  res_Kaggle.to_csv('./output_data_fp_growth/Kaggle_result.csv',index=False,header=True)
  print('kaggle Success')

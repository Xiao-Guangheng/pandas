import pandas as pd
import numpy as np

# series对象

# 两个核心数据结构 ：series (一维的)， DataFrame (二维的)

# series不仅有值还有索引

s = pd.Series([1, 2, 3, 4, 5])
print(s)  #默认整数索引

sn = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
print(sn)  #自定义索引

sn['b']  #按标签取值
sn.loc['b']  #显式按标签取值
sn.iloc[1]  #按位置取值

# series由两个组成部分：values和index

s.values
s.index
type(s.values)
type(s.index)

type(s.index)  #-> 看"盒子"是什么做的（塑料盒？纸盒？）   <- 容器类型
s.index.dtype  #-> 看"盒子里面装的是什么"（黄豆？绿豆？）  <- 元素类型

s.values.shape

s.values*2  #表示值乘以二

# 从字典创建：字典本省就是名字对应值。天然符合sries的索引-值结构。

a=pd.Series({"苹果": 5.5, "香蕉": 3.2, "橙子": 6.0})# 里面是一个字典，series自动把字典的key作为索引，value作为值

order = ["橙子", "苹果", "香蕉", "葡萄"]
aligned = pd.Series({"苹果": 5.5, "香蕉": 3.2, "橙子": 6.0}, index=order)  
#这里指定了索引顺序，series会按照这个顺序来排列，如果字典里没有的索引就会显示为NaN

s.shape
s.dtype
s.size
s.name  #series的名字，默认是None，可以自己设置，当作列名


#  运算
score = pd.Series([90, 80, 70], index=["数学", "语文", "英语"])
score + 10  #每个元素加10
np.sqrt(score)  #每个元素开平方
# numpy的函数可以直接对series进行运算，返回的还是series，索引不变
score > 78 # 返回布尔数组，带索引
score[score > 78] #返回满足条件的元素，带索引

# 两个series相加，索引对齐
score2 = pd.Series([100, 60, 70], index=["数学", "语文", "物理"])
score + score2
  #两个series相加，索引对齐，如果有一个series没有这个索引，就会返回NaN

# 这里都有数学和语文，所以数学和语文的成绩会相加，英语和物理没有对应的索引，所以返回NaN

# 使用fill_value参数可以填充缺失值：
score.add(score2, fill_value=0)  #缺失值用0填充

s = pd.Series([88, 92, 76, 85], index=["张三", "李四", "王五", "赵六"])

print("平均分:", s.mean())        # 85.25
print("总分:  ", s.sum())         # 341
print("最高分:", s.max())         # 92
print("最高分是谁:", s.idxmax())   # '李四'  <- ndarray 没有的能力！
print("最低分位置:", s.idxmin())   # '王五'


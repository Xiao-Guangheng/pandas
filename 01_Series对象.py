# -*- coding: utf-8 -*-
# ============================================================
# 第1章：Series 对象 -- 一切的起点
# ============================================================
# Pandas 只有两个核心数据结构，把这两个搞懂，Pandas 就懂了一大半：
#   1. Series   ：一维的、带标签的数组（本章）
#   2. DataFrame：二维表格，可以理解为"多个 Series 拼在一起"（下一章）
#
# Series 和 ndarray 的区别一句话就能说清：
#   ndarray 只有"值"，Series 除了值，还有一套自己的"行号/名字"（索引）。
# 就像体育场看球的座位：ndarray 只有第 0 排第 0 个位置这种编号，
# Series 则是每个座位都贴了张纸条写着"张三"、"李四"。
#
# 导入惯例：和 NumPy 用 np 一样，大家都用 pd。
import pandas as pd
import numpy as np  # Series 底层就是 ndarray，经常要配合用


# ============================================================
# 1.1 创建 Series：从列表创建
# ============================================================
# 最常见的方式：把一个列表交给 pd.Series()。
# 不指定索引时，pandas 自动分配 0, 1, 2, ...（叫"默认整数索引"）。

print("=" * 50)
print("1.1 从列表创建 Series")

scores = pd.Series([88, 92, 76, 85, 90])

print(scores)
# 打印出来左边一列是索引（0~4），右边一列是值，最底下是 dtype。
# 和 ndarray 的打印不同：Series 会把索引一起显示出来。
#
# 在 pandas 3.0 里，整数的 dtype 依然显示 int64，
# 但字符串列会显示新的 str dtype（第 2 章细讲）。

# 如果给了索引，它就不再是"默认 0,1,2"，而是你指定的名字：
scores_named = pd.Series([88, 92, 76], index=["语文", "数学", "英语"])
print("\n带名字索引的 Series:")
print(scores_named)
# 现在可以用名字取值了：
print("数学成绩:", scores_named["数学"])   # 按标签取
print("数学成绩:", scores_named.loc["数学"])  # loc 显式地"按标签取"，更推荐
# 注意：scores_named[0] 在 pandas 3.0 里会直接报 KeyError！
# 老版本里"整数自动当位置"的模糊行为已被删除，按位置取必须用 iloc：
print("第 0 个（按位置）:", scores_named.iloc[0])

# 这就是 pandas 3.0 最重要的变化之一：
#   按标签取 -> loc；按位置取 -> iloc；[] 传整数不再自动猜了。


# ============================================================
# 1.2 Series 的两个组成部分：values 和 index
# ============================================================
# Series = 值（ndarray） + 索引（Index 对象）。
# 这两个属性可以把"表"和"引擎"剥开看。

print("\n" + "=" * 50)
print("1.2 Series 的内部：values 与 index")

s = pd.Series([10, 20, 30], index=["a", "b", "c"])

print("值（是个 ndarray）:", s.values)          # [10 20 30]
print("值的类型:", type(s.values))               # <class 'numpy.ndarray'>
print("索引:", s.index)                          # Index(['a', 'b', 'c'], dtype='str')
print("索引的类型:", type(s.index))               # pandas.core.indexes.base.Index
print("索引可以迭代:", list(s.index))  #可迭代，所以可以变成列表

# 既然 values 是 ndarray，你学过的 NumPy 技能全部可用：
print("值的 shape:", s.values.shape)             # (3,)
print("值翻倍:", s.values * 2)                    # [20 40 60]


# ============================================================
# 1.3 从字典创建：键变索引，值变值
# ============================================================
# 字典本来就是"名字 -> 值"的对应，天然适合变成 Series。

print("\n" + "=" * 50)
print("1.3 从字典创建 Series")

fruit_price = pd.Series({"苹果": 5.5, "香蕉": 3.2, "橙子": 6.0})
print(fruit_price)
# 注意索引顺序和字典写入顺序一致（Python 3.7+ 的字典保证有序）。

# 一个实用技巧：字典 + index 参数 = 按你想要的顺序对齐，缺的补 NaN
order = ["橙子", "苹果", "香蕉", "葡萄"]
aligned = pd.Series({"苹果": 5.5, "香蕉": 3.2, "橙子": 6.0}, index=order)
print("\n按指定索引对齐（葡萄没有数据）:")
print(aligned)
# "葡萄"在字典里不存在，所以是 NaN（Not a Number，缺失值）。
# 缺失值的处理是第 5 章的主题，这里先见个面。


# ============================================================
# 1.4 Series 的属性：shape / dtype / size / name
# ============================================================
print("\n" + "=" * 50)
print("1.4 Series 的常用属性")

s = pd.Series([88, 92, 76, 85], index=["a", "b", "c", "d"], name="成绩")

print("shape:", s.shape)       # (4,)   一维
print("dtype:", s.dtype)       # dtype('int64')
print("size: ", s.size)        # 4
print("name: ", s.name)        # '成绩'，给 Series 起个名字，合并时会当列名用

# dtype 和 ndarray 的 dtype 是同一套体系（int64/float64/bool/str...），
# 因为底层就是 ndarray。你已经懂 dtype，这里就不再展开。


# ============================================================
# 1.5 Series 的运算：和 ndarray 一样"向量化"
# ============================================================
# 对 Series 做运算，就是对其中的值逐个运算，索引原样保留。
# 这就是你在 NumPy 学的"广播/向量化"，Series 完全继承。

print("\n" + "=" * 50)
print("1.5 Series 的向量化运算")

score = pd.Series([88, 92, 76, 85], index=["张三", "李四", "王五", "赵六"])

print("每个人加 5 分:")
print(score + 5)               # 索引不动，值逐个 +5

print("\n开根号（成绩没什么必要，看个效果）:")
print(np.sqrt(score))          # numpy 的函数直接能吃 Series

print("\n比较运算得到布尔 Series:")
print(score > 85)              # [False, True, False, False]（带索引）

# 布尔 Series 可以拿来筛选（第 4 章详细讲）：
print("\n筛出 85 分以上的:")
print(score[score > 85])       # 只剩李四


# ============================================================
# 1.6 两个 Series 相加：索引自动对齐（重要！）
# ============================================================
# 这是 Series 和 ndarray 最大的行为差异，必须理解：
# ndarray 相加按"位置"硬碰硬；Series 相加按"索引名字"配对，
# 对不上的位置填 NaN。

print("\n" + "=" * 50)
print("1.6 索引对齐（Series 与 ndarray 的最大区别）")

a = pd.Series({"语文": 88, "数学": 92})
b = pd.Series({"数学": 90, "英语": 85})

print("a + b:")
print(a + b)
# 结果：
#   数学    182   （两边都有 -> 真正相加）
#   英语    NaN   （a 里没有）
#   语文    NaN   （b 里没有）
# 索引是两边索引的并集，配不上对的就是 NaN。

# 如果不想得到 NaN，可以用 add 方法的 fill_value 参数：
print("\n用 fill_value=0 把缺的当 0:")
print(a.add(b, fill_value=0))
#   数学    182.0
#   英语     85.0
#   语文     88.0

# 记住这个画面：**Series 运算按标签配对，不是按位置。**
# 这个机制叫"索引对齐"，DataFrame 的所有运算也都遵守它，
# 也是很多"结果怎么全是 NaN"这类 bug 的根源。


# ============================================================
# 1.7 常用方法速览：mean / sum / max / idxmax ...
# ============================================================
# 统计方法和你 NumPy 里学的一模一样，但有两个增强：
#   1. 默认跳过 NaN
#   2. idxmax/idxmin 直接告诉你"最大值在哪（的标签）"

print("\n" + "=" * 50)
print("1.7 统计方法")

s = pd.Series([88, 92, 76, 85], index=["张三", "李四", "王五", "赵六"])

print("平均分:", s.mean())        # 85.25
print("总分:  ", s.sum())         # 341
print("最高分:", s.max())         # 92
print("最高分是谁:", s.idxmax())   # '李四'  <- ndarray 没有的能力！
print("最低分位置:", s.idxmin())   # '王五'

# 带缺失值时统计照样工作（NaN 自动跳过）：
s_nan = pd.Series([1, np.nan, 3])
print("\n含 NaN 的求和:", s_nan.sum())    # 4.0，不是 NaN
print("含 NaN 的个数:", s_nan.count())    # 2  （count 只数非缺失的）


# ============================================================
# 本章小结
# ============================================================
# 1. Series = ndarray 的值 + Index 的标签，底层就是 NumPy
# 2. 创建：pd.Series(列表) / pd.Series(字典) / 加 index 参数
# 3. 取值：loc 按标签，iloc 按位置；pandas 3.0 里 s[整数] 不再自动当位置
# 4. 运算：向量化继承自 ndarray，但相加时按"索引名"对齐，配不上的填 NaN
# 5. 统计：mean/sum/max 全部默认跳过 NaN；idxmax 能直接给出标签

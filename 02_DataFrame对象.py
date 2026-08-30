# -*- coding: utf-8 -*-
# ============================================================
# 第2章：DataFrame 对象 -- Pandas 的主角
# ============================================================
# DataFrame 是 Pandas 真正的主角，日常说的"用 Pandas 处理数据"，
# 99% 的场景都是在操作 DataFrame。
#
# 理解 DataFrame 的最好方式：
#   DataFrame = 一组共用同一个行索引的 Series（每列一个 Series）。
# 每个 Series 有自己的名字（就是列名）和自己的 dtype。
#
#        列索引（columns）:   姓名    分数
#                          ┌──────┬──────┐
#   行索引（index）:    0   │ 张三  │  88  │
#                       1   │ 李四  │  92  │
#                       2   │ 王五  │  76  │
#                          └──────┴──────┘
# "分数"这一列单独拎出来就是上一章的 Series。
#
# 本章的示例数据（学生成绩表）会在后面各章反复出现，
# 记住它的样子，后面看到输出就能对上号。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)  # 中文对齐（可选）


# ============================================================
# 2.1 创建 DataFrame：从字典（最常用）
# ============================================================
# 字典的键 -> 列名；字典的值 -> 这一列的数据。

print("=" * 50)
print("2.1 从字典创建 DataFrame")

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})
print(df)
# 打印效果：
#    姓名  班级  语文  数学
# 0  张三  一班    88    90
# 1  李四  一班    92    85
# 2  王五  二班    76    95
# 3  赵六  二班    78    95
# 最上面一行是列索引（columns），最左边一列是行索引（index）。

# 也可以同时指定行索引（默认是 0,1,2,...）：
df2 = pd.DataFrame(
    {"语文": [88, 92], "数学": [90, 85]},
    index=["期中", "期末"],
)
# 指定行索引，就是第一个是列名，然后是值
print("\n带自定义行索引:")
print(df2)


# ============================================================
# 2.2 从其他东西创建：列表的列表 / Series 字典 / ndarray
# ============================================================
print("\n" + "=" * 50)
print("2.2 其他创建方式")

# 方式 A：列表的列表（每行一个子列表），配 columns 指定列名
df_rows = pd.DataFrame(
    [[1, "a"], [2, "b"]],
    columns=["编号", "字母"],
)
print("列表的列表:\n", df_rows, sep="")

# 方式 B：ndarray + columns（NumPy 学过来的数组直接变表格）
arr = np.arange(12).reshape(3, 4)
df_arr = pd.DataFrame(arr, columns=["c1", "c2", "c3", "c4"])
print("\nndarray:\n", df_arr, sep="")

# 方式 C：Series 组成的字典（Series 的 name 会自动当列名）
s1 = pd.Series([88, 92], name="语文")
s2 = pd.Series([90, 85], name="数学")
print("\nSeries 字典:\n", pd.DataFrame({"语文": s1, "数学": s2}), sep="")
# 如果两个 Series 索引不同，会按索引对齐（上一章的知识）。


# ============================================================
# 2.3 三大查看方法：head / tail / sample
# ============================================================
# 真实数据动辄几十万行，print(df) 会打出一大坨。
# 养成习惯：先 head() 看几行，确认数据长什么样。

print("\n" + "=" * 50)
print("2.3 head / tail / sample")

# 造一个 100 行的表（顺便复习 NumPy 随机数）
rng = np.random.default_rng(42)
big = pd.DataFrame({
    "x": rng.normal(0, 1, 100),
    "y": rng.integers(0, 10, 100),
})

print("head() 默认前 5 行:")
print(big.head())
print("\ntail(3) 最后 3 行:")
print(big.tail(3))
print("\nsample(2) 随机抽 2 行:")
print(big.sample(2, random_state=1))
# sample 的 random_state 传种子，保证每次抽样结果一样（和 NumPy 一样）。


# ============================================================
# 2.4 摸底三件套：shape / info / describe
# ============================================================
# 拿到陌生数据的第一件事永远是这三样：多少行列、什么类型、数值分布如何。

print("\n" + "=" * 50)
print("2.4 info 与 describe")

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

print("shape:", df.shape)          # (4, 4)  -> 4 行 4 列
print("列名:", df.columns.tolist())  # ['姓名', '班级', '语文', '数学']
print("行索引:", df.index.tolist())  # [0, 1, 2, 3]
print("每列类型:\n", df.dtypes, sep="")
# 姓名/班级 -> str（pandas 3.0 新的字符串类型，不再是 object）
# 语文/数学 -> int64

print("\ninfo() 综合信息:")
df.info()
# info 一次告诉你：多少行、每列叫什么、什么类型、有没有缺失、内存占用。

print("\ndescribe() 数值列统计:")
print(df.describe())
# describe 默认只统计数值列：count/mean/std/min/四分位/max。
# 这套数字就是你在 NumPy 里学的那些聚合，pandas 一次全给你。

print("\ndescribe() 也能看字符串列（include='all' 或指定）:")
print(df["班级"].describe())
# 字符串列给出：count / unique（几个不同的值）/ top（出现最多的）/ freq


# ============================================================
# 2.5 取列：df["列名"] -> Series
# ============================================================
# 这是 DataFrame 最频繁的操作，必须形成肌肉记忆。
# 取一列得到 Series；取多列（传列表）得到新的 DataFrame。

print("\n" + "=" * 50)
print("2.5 取列")

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

col = df["语文"]                # 一列 -> Series
print("取一列，类型是:", type(col))
print(col)
print("这一列的平均分:", col.mean())   # Series 的统计方法直接用

cols = df[["姓名", "数学"]]      # 多列 -> DataFrame（注意双层中括号）
print("\n取多列，类型是:", type(cols))
print(cols)

# 补充：df.列名（属性写法）也能取列，但仅当列名是合法的 Python
# 标识符（不含空格/中文其实可以）时不推荐，统一用 [] 写法最稳。
print("\n属性写法 df.数学 也行，但不推荐统一用它:")
print(df.数学)


# ============================================================
# 2.6 DataFrame 就是一堆 Series：验证一下
# ============================================================
print("\n" + "=" * 50)
print("2.6 每一列都是 Series")

df = pd.DataFrame({
    "语文": pd.Series([88, 92], index=["期中", "期末"]),
    "数学": pd.Series([90, 85], index=["期中", "期末"]),
})

chinese = df["语文"]
print("df['语文'] 的类型:", type(chinese))   # Series
print("它的 name:", chinese.name)             # '语文'（列名就是 Series 的 name）
print("它的 index:", chinese.index.tolist())  # ['期中', '期末']

# 所以第 1 章学的所有 Series 操作，对"df 的每一列"全部适用：
print("语文平均:", df["语文"].mean())
print("期末的语文:", df["语文"].loc["期末"])


# ============================================================
# 2.7 行列互换（转置）与 to_numpy()
# ============================================================
print("\n" + "=" * 50)
print("2.7 转置与 to_numpy")

df = pd.DataFrame({"语文": [88, 92], "数学": [90, 85]}, index=["期中", "期末"])

print("转置（df.T，行列互换）:")
print(df.T)
# 行变成列、列变成行。注意 dtype 会变成混合类型。

arr = df.to_numpy()   # 扔回 ndarray（需要喂给纯 NumPy/算法时用）
print("\nto_numpy 的类型:", type(arr))
print(arr)
# 提醒：含字符串的表 to_numpy 后 dtype 是 object（NumPy 的老字符串类型），
# 数值运算记得先选好列。


# ============================================================
# 2.8 打印美化（可选但实用）
# ============================================================
print("\n" + "=" * 50)
print("2.8 显示选项")

# 中文列对齐、显示更多行/列，都在 pd.set_option 里：
pd.set_option("display.max_rows", 10)        # 最多显示 10 行
pd.set_option("display.max_columns", 20)     # 最多显示 20 列
pd.set_option("display.width", 120)           # 打印宽度
# 恢复默认用 pd.reset_option("display.max_rows") 等。
# 这些不影响计算，只影响 print 出来的样子，忘了也无所谓。


# ============================================================
# 本章小结
# ============================================================
# 1. DataFrame = 共用行索引的一组 Series，每列一个类型
# 2. 创建：字典（最常用）/ 列表的列表 / ndarray + columns
# 3. 摸底：shape、info()、describe()、head()/tail()/sample()
# 4. 取列：df["列名"] -> Series；df[["a","b"]] -> DataFrame
# 5. df["列"] 拿到的 Series，上一章的所有方法都能用

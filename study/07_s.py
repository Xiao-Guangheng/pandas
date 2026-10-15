
import pandas as pd
import numpy as np

# 运算与统计
# 统计是跟numpy一样的，pandas是基于numpy的。复习一下
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
    "体育": [70, 65, 80, np.nan],      # 赵六缺考体育
})

df.mean()  # 取平均值
df.mean(numeric_only=True)  # 取平均值，跳过非数值列
# 跳过“姓名”这种字符串列。pandas 3.0 遇到字符串列不加这个参数会报错，记住带上。

df[["语文", "数学", "体育"]].sum()  # 取总和
df[["语文", "数学", "体育"]].max()  # 取最大值
df[["语文", "数学", "体育"]].min()  # 取最小值
df[["语文", "数学", "体育"]].std()  # 取标准差
df[["语文", "数学", "体育"]].var()  # 取方差

df[["语文", "数学", "体育"]].mean(axis=1)  # axis=1 按行算（每人的平均分）
# axis =1 就是每行


s = pd.Series([10, 20, 15, 30], index=["1月", "2月", "3月", "4月"])
s.cumsum()  # 累计和
# 这个和sum()不一样，sum()是把所有的加起来，cumsum()是每个元素和前面所有元素的和。
# 举个例子：10, 30, 45, 75，这个输出的结果是一个Series，里面的每个元素都是前面所有元素的和。
s.cummax()  # 累计最大
# 它保留到当前位置为止出现过的最大值，所以结果只会持平或上升，永远不会下降。输出也是一个Series
s.diff()  # 逐期差
# 计算相邻两个元素之间的差值。输出也是一个Series，现在的减上一个
s.pct_change()  # 环比
# 计算相邻两个元素之间的百分比变化。输出也是一个Series，现在的减上一个再除以上一个

# 这些在做销售/增长分析的时候经常使用



#相关系数与协方差
df2 = pd.DataFrame({
    "学习时长": [2, 4, 6, 8],
    "成绩": [60, 70, 80, 90],
    "游戏时长": [8, 6, 4, 2],
})

df2.corr()  # 相关系数
# 相关系数是衡量两个变量之间的线性关系的强度和方向的统计指标。
# 它的取值范围在-1到1之间，取值越接近1表示正相关越强，取值越接近-1表示负相关越强，取值为0表示没有线性相关关系。

# 看这个例子，学习时长和成绩完全正相关，和游戏时长完全负相关

df2.cov()
# 这是一个与相关系数同源的函数，是计算相关系数的一个中间量，返回的是一个协方差矩阵，
# 协方差矩阵是一个对称矩阵，主对角线上的元素是各个变量的方差，非主对角线上的元素是各个变量之间的协方差。

cities = pd.Series(["北京", "上海", "北京", "广州", "北京"])
cities.value_counts() # 计算出现次数
cities.value_counts(normalize=True)  # 计算出现频率
# 加上这个normalize=True参数，就会返回每个值出现的频率，而不是出现的次数。
cities.unique().tolist()  # 去重之后的列表
cities.nunique() # 不同值的个数


# map 逐元素映射（Series)专用.只作用与单个Series

df3 = pd.DataFrame({"等级": ["A", "B", "A", "C"]})
# 这是字典映射，翻译类值别
score_map= {"A": 90, "B": 80, "C": 70}
df3["分数"] = df3["等级"].map(score_map)
# 函数映射，就是没有已经定义好的一个字典，没有确定的值翻译
df3["等级"].map(lambda x: ord(x) - 64)  # A=1, B=2, C=3
# 这个就是把每个等级的字母转换为对应的数字，A对应1，B对应2，C对应3。使用了ord函数获取字符的ASCII码，然后减去64得到对应的数字。

# 这个映射有什么用，就是把原来的值翻译成我们想要的值，或者做一些计算。

# 配合其他Series方法使用，比如value_counts()，可以先用map()把值翻译成我们想要的值，
# 然后再用value_counts()计算出现次数或者频率。
name_to_score = pd.Series({"张三": 88, "李四": 92})
names = pd.Series(["张三", "李四", "王五"])
print(name_to_score.reindex(names).tolist())   # 王五查不到 -> NaN

# apply 逐元素映射（DataFrame)专用.作用于整个DataFrame，逐行/列 执行函数

df4 = pd.DataFrame({
    "语文": [88, 59, 92],
    "数学": [90, 45, 85],
})

def evaluate(row):
    total = row["语文"] + row["数学"]
    if row["语文"] < 60 or row["数学"] < 60:
        return "有挂科"
    return "优秀" if total >= 175 else "合格"

print(df4.apply(evaluate, axis=1).tolist())
# 一行一行处理，把每行的语文和数学成绩传给 evaluate 函数，返回评语。
# 这就是 apply 的作用，逐行/列 执行函数，返回一个新的Series。
print(df4.apply(lambda col: col.max() - col.min()).tolist())   # 每列极差
print(pd.Series([-1, 2, -3]).apply(abs).tolist())
# 取绝对值，映射类似于map，但是apply可以作用于整个DataFrame，而map只能作用于单个Series。


# df.map() 逐元素，DataFrame 版，替代老 applymap

df5=pd.DataFrame({
    "语文": [88, 59, 92],"数学": [90, 45, 85]})
df5.map(lambda x: x + 10)  # 每个元素加10
df5.map(lambda x:f"{x}分")  # 每个元素加上"分"字,转化为字符串
# 跟applymap()一样，都是对每个元素进行操作，但是applymap()是DataFrame专用，而map()是Series专用。

# transform
# apply聚合之后形状会改变，比如每列平均值只有一个数，transform的结果必须和原数据一样长

s = pd.Series([80, 90, 100])
# transform 传"逐元素变换函数"，输出和输入一样长：
print(s.transform(np.sqrt).tolist())

df6 = pd.DataFrame({"语文": [80, 90, 100], "数学": [60, 70, 80]})
centered = df6 - df6.mean()          # 每列减去各自的均值

# apply和向量化的对比

import time

n = 100_000
big = pd.Series(np.random.default_rng(0).normal(0, 1, n))

# 写法 A：apply + lambda（Python 循环）
t0 = time.perf_counter()
r1 = big.apply(lambda x: x * 2 + 1)
t1 = time.perf_counter()

# 写法 B：直接向量化运算
t2 = time.perf_counter()
r2 = big * 2 + 1
t3 = time.perf_counter()

print(f"apply 用时:      {(t1 - t0) * 1000:7.1f} ms")
print(f"向量化用时:     {(t3 - t2) * 1000:7.1f} ms")
print(f"结果一致:       {r1.equals(r2)}")
import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)  # 中文对齐（可选）

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

# DataFrame就是一个二维表格，行列都有索引，行索引是0,1,2,...，列索引是"姓名","班级","语文","数学"。
# DataFrame的每一列都是一个Series，Series有自己的索引和数据类型

df2 = pd.DataFrame(
    {"语文": [88, 92], "数学": [90, 85]},  #这是一个字典，没有指定行索引，默认是0,1,2,...
    index=["期中", "期末"], #这里指定了行索引
)
# 指定行索引

# 从列表创建

df_row=pd.DataFrame(
    [[1,"a"],[2,"b"]],  #这里是一个列表的列表，每个子列表就是一行数据
    columns=["编号", "字母"]  #制定了列索引
)

arr=np.arange(12).reshape(3,4)
df_arr=pd.DataFrame(arr,columns=["A","B","C","D"])  #这里是一个ndarray，指定了列索引


#Series 组成的字典（Series 的 name 会自动当列名）
s1 = pd.Series([88, 92], name="语文")
s2 = pd.Series([90, 85], name="数学")

pd.DataFrame({s1.name: s1, s2.name: s2}, index=["期中", "期末"])

# 这里用series的name自动作为列名，index指定了行索引

# head,tail,sample

rng = np.random.default_rng(42)

big = pd.DataFrame({
    "x": rng.normal(0, 1, 100),  # 这里是一个正态分布的随机数，均值为0，标准差为1，生成100个
    "y": rng.integers(0, 10, 100),  # 这里是一个均匀分布的随机整数，范围是[0,10)，生成100个
})

big.head() # 默认前五行
big.tail() # 默认后五行
big.sample(5) # 随机抽取5行

# shape,info,describe

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})  #没有指定行索引，默认是0,1,2,3

print("shape:", df.shape)          # (4, 4)  -> 4 行 4 列
print("列名:", df.columns.tolist())  # ['姓名', '班级', '语文', '数学']
print("行索引:", df.index.tolist())  # [0, 1, 2, 3]
print("每列类型:\n", df.dtypes, sep="")  #输出每一列的数据类型，比如姓名：str，语文：int64

df.info()  #输出DataFrame的基本信息，包括行数、列数、每列的数据类型、非空值数量等
df.describe()  #输出数值型列的统计信息，包括计数、均值、标准差、最小值、四分位数、最大值等
#指定列索引和行索引
df[["语文","数学"]].describe()  #只输出语文和数学两列的统计信息
# 输出的信息有：计数、均值、标准差、最小值、四分位数、最大值

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

# 取列操作

col = df["语文"]  #取出语文这一列，返回一个Series
type(col)  #<class 'pandas.core.series.Series'>
col.mean()
cols = df[["语文","数学"]]  #取出语文和数学两列，返回一个DataFrame

df = pd.DataFrame({
    "语文": pd.Series([88, 92], index=["期中", "期末"]),
    "数学": pd.Series([90, 85], index=["期中", "期末"]),
})
chinese = df["语文"]  #取出语文这一列，返回一个Series
df["语文"].mean()
df["语文"].loc["期中"]  #取出期中这一行的语文成绩


#转置

# 行列互换
df=pd.DataFrame({"语文":[88,92],"数学":[90,85]},index=["期中","期末"])  #转置，行列互换
# 原来的DataFrame输出：
#   语文  数学
# 期中  88  90
# 期末  92  85

df.T  #转置，行列互换

# 转置之后的：
#   期中  期末
# 语文  88  92
# 数学  90  85

arr = df.to_numpy()   # 扔回 ndarray（需要喂给纯 NumPy/算法时用）
# 不要行索引和列索引，只保留数据

type(arr)  #<class 'numpy.ndarray'>


# 中文列对齐、显示更多行/列，都在 pd.set_option 里：
pd.set_option("display.max_rows", 10)        # 最多显示 10 行
pd.set_option("display.max_columns", 20)     # 最多显示 20 列
pd.set_option("display.width", 120)           # 打印宽度
# 恢复默认用 pd.reset_option("display.max_rows") 等。
# 这些不影响计算，只影响 print 出来的样子，忘了也无所谓。

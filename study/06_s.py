
import pandas as pd
import numpy as np


# 数据增删改
# 对数据做增删改操作，主要是对 DataFrame 的列和行进行操作。常见的操作包括：
# 1. 新增列：可以通过直接赋值的方式新增列，也可以使用 assign 方法新增列。
# 2. 删除列：可以使用 drop 方法删除列。
# 3. 修改列：可以使用 loc 或 iloc 方法修改列的值。
# 4. 新增行：可以通过 append 方法新增行。
# 5. 删除行：可以使用 drop 方法删除行。
# 6. 修改行：可以使用 loc 或 iloc 方法修改行的值。


df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

df["总分"] = df["语文"] + df["数学"]
df["等级"] = "及格"  # 广播，这是对一整列赋同一个值，也是新增列

# 配合条件进行赋值，只改满足条件的行：
df.loc[df["总分"] >= 180, "等级"] = "优秀"  # 把符合要求的行的等级改为优秀
# 这里的loc就是按行列索引来定位数据，左边是行的条件，右边是列的名称。
# 复习一下，loc是按照标签
# iloc是按照位置定位

# assign 方法可以新增列，并且不会改变原来的 DataFrame，而是返回一个新的 DataFrame。

new_df = df.assign(总分=df["语文"] + df["数学"],
                   平均分=(df["语文"] + df["数学"]) / 2)

# 新增了两列
                   
result = (df.assign(总分=df["语文"] + df["数学"])
.query("总分 > 170")
.sort_values("总分", ascending=False))  # 链式写法，先新增列，再筛选，再排序

# 链式写法，每一步都产生一个新的 DataFrame 传给下一步，最后的结果是一个新的 DataFrame。

# 在指定位置插入列，可以使用 insert 方法。insert 方法有三个参数，分别是位置、列名和列的值。

df2= df.copy()
df2.insert(1, "学号", ["S001", "S002", "S003", "S004"])  # 插到第 1 列
# 三个参数，第一个是位置（就是要插入到第几列），第二个 是列名，第三个是列的值。

# 这里不同于赋值的写法，赋值只能添加在最右边

# 删除行，列

df.drop(columns=["语文"])  # 删除列

df.drop(index=[0,1])  # 删除第 0 行和第 1 行

mask = df["总分"] < 170
df.drop(index=df[mask].index)  # 删除总分小于 170 的

# 或者直接用~

df[~mask]  # 取反，保留总分大于等于 170 的行

# pop方法

df3= df.copy()
df3.pop("数学")  # 删除列，并返回被删除的列

math_col = df3.pop("数学")  # 删除列，并返回被删除的列


# 修改列名

df.rename(columns={"语文": "Chinese", "数学": "Math"})  # 修改列名
# 可以使用index修改行索引‘
df.rename(index={0: "A", 1: "B", 2: "C", 3: "D"})  # 修改行索引

df4=df.copy()
df4.columns =["Name", "Class", "Chinese", "Math"]  # 直接修改列名
# 这个方法不在乎列名是否存在，直接修改所有列名，如果列名数量不对，会报错，就是不会关心映射关系


# 常见的批量处理
df5= df.copy()
df5=df5.rename(columns=str.upper)  # 将所有列名改为大写

# 修改值：

df6=df.copy()
df6.loc[1, "语文"] = 95 # 修改指定行列的值,第一行第一列的值
df6["语文"] = df6["语文"].apply(lambda x: min(x, 90))   # 90 分封顶
#  apply 方法可以对 DataFrame 的每一行或每一列应用一个函数。
#  apply 第一个参数是一个函数，第二个是 axis，axis=0 表示对每一列应用函数，axis=1 表示对每一行应用函数。

# 这里就是对语文列的每一个值应用一个函数，函数是一个匿名函数，返回值是 min(x, 90)，也就是如果 x 大于 90，就返回 90，否则返回 x。

df6.loc[df6["语文"] < 80, "数学"] = df6.loc[df6["语文"] < 80, "数学"] + 5  # 补偿加分
# 小于80的语文成绩的学生，数学成绩加5分

# 添加行： concat

new_row = pd.DataFrame({"姓名": ["钱七"], "班级": ["三班"], "语文": [81], "数学": [88]})
df7 = pd.concat([df, new_row], ignore_index=True)

# 第一个参数是一个列表，里面是要合并的 DataFrame，第二个参数是 ignore_index=True，表示忽略原来的索引，重新生成索引.
# 这里把原来的 df 和新的一行 new_row 合并成一个新的 DataFrame df7，并且重新生成索引。

# 修改列的数据类型：astype

df8 = pd.DataFrame({"语文": [88, 92], "标签": ["1", "2"]})   # 标签列是字符串
df8["标签"] = df8["标签"].astype(int)  # 转为整数类型

df9=pd.DataFrame({"价格": ["1.2", "2.5", "3.8"]})  # 价格列是字符串
df9["价格"] = df9["价格"].astype(float)  # 转为浮点数类型

# 含 NaN 的列转 int 会报错（NaN 不是整数），要先处理缺失值：
s = pd.Series([1.5, np.nan])
try:
    s.astype(int)
except (ValueError, TypeError) as e:
    print("\n含 NaN 直接转 int 报错:", str(e)[:60], "...")

s.astype("Int64", errors="ignore").tolist()
# 这一步是将含有 NaN 的列转为可空整数类型 Int64，这样就不会报错了。
# 但是其实，NaN 不是整数，所以还是会有问题，只是不会报错而已。
# 它会返回一个列表[1.5, nan]——转换"看起来没报错"，但其实没转成整数类型，还是浮点数类型，只是用可空整数类型表示了。

s_int = pd.Series([1, 2], dtype="int64")  
# 这里是把一个普通的整数列转为可空整数类型 Int64，这样就可以同时装下整数和缺失值了。
s_int.astype("Int64").tolist()

s.round().astype("Int64").tolist()
# 把浮点数列四舍五入后再转为可空整数类型 Int64，这样就可以同时装下整数和缺失值了。


# 列顺序的调整

order = ["姓名", "班级", "语文", "数学", "总分", "等级"]
df[df.columns[::-1]]  # 反转列顺序
df[order]  # 按指定顺序排列列


import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"],
    "班级": ["一班", "一班", "一班", "一班", "二班", "二班", "二班", "二班"],
    "语文": [88, 92, 76, 59, 85, 90, 73, 66],
    "数学": [90, 85, 95, 78, 92, 88, 81, 70],
})

# 单条件筛选

mask= df["语文"] > 80        # 布尔 Series（每行一个 True/False）
print("掩码长这样:")
print(mask)

# 一行的写法

print(df[df["语文"] > 80])
# 原理和 NumPy 一模一样：把布尔掩码当"筛子"，True 的行留下。

# 多条件筛选

cond = (df["语文"] > 80) & (df["数学"] > 80)     # 两科都 > 80
df[cond]

cond2 = (df["班级"] == "二班") | (df["语文"] > 90)  # 二班 或 语文>90
df[cond2]

cond3 = ~(df["班级"] == "一班")                   # 不是一班（非）
df[cond3]

# 使用loc配合使用
df.loc[df["语文"] > 80, ["姓名", "语文"]]  # 语文>80的学生姓名和语文成绩

# 第一个是行筛选条件，第二个是列筛选条件。

print(df.loc[(df["语文"] > 80) & (df["数学"] > 80), ["姓名", "数学"]])

df_fix = df.copy()
df_fix.loc[df_fix["数学"] < 80, "数学"] = 80  # 数学成绩低于80的改为80
df_fix[df_fix["数学"] == 80]

df_bouns=df.copy()
df_bouns.loc[df_bouns["语文"] > 80, "语文"] *= 1.1  # 语文成绩>80的加10%
df_bouns.loc[df_bouns["数学"] > 90, "数学"] += 5  # 数学成绩>90的加5分

# isin

# 是否在集合里面

names = ["张三", "李四", "王五"]
df[df["姓名"].isin(names)]  # 选出姓名在names列表中的行
df[~df["姓名"].isin(names)]  # 选出姓名不在names列表中的行

# between 区间筛选

df[df["语文"].between(80, 90)]  # 选出语文成绩在80-90之间的行
# 等价于 (df["语文"] >= 70) & (df["l语文"] <= 85)，但更省事。

# where 与 mask : 不删除 值替换

s=df["语文"]
s.where(s>80, 0)  # 语文成绩>80的保留，其他的替换为0

s.mask(s>100, 100)  # 满足条件的替换为0，其他的保留，就是大于80的替换为100，其他的保留

df_num=df[["语文", "数学"]]

df_num.where(df_num<80)

# 使用字符串写条件

df.query("语文 > 80 & 数学 < 90")  # 语文>80 且 数学<90 的行

df.query("班级 == '一班' | 语文 > 90")  # 一班 或 语文>90 的行
th=89
df.query("语文 > @th")[["姓名", "语文"]]  # 语文>89 的行
# 使用外部变量需要加@符号，表示引用外部变量。

# 字符串直接使用and not or ，条件比较多的时候就用字符串，因为写一堆&比较麻烦

result = df[df["语文"] > 80]  # 筛选行，行呗留下，索引也被留下
result.index.tolist()  # 返回索引列表
# 这里的tolist()是将索引对象转换为列表，方便后续操作。

result.reset_index(drop=True)  # 重置索引，drop=True表示不保留原索引
# 这个打印出来是[0, 1, 2, 3]，原来的索引是[0, 1, 4, 5]，被筛掉的行让索引"有洞"。

# 这个result筛选出来的是一个新的DataFrame，直接给它赋值不会影响原表（pandas 3.0 的写时复制机制保证这点）：
result2 = df[df["语文"] > 80]

result2.loc[result2.index, "语文"] = 0  # 将筛选出来的语文成绩改为0
df["语文"].tolist()  # 原表不受影响，还是原来的成绩



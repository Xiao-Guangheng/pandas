# -*- coding: utf-8 -*-
# ============================================================
# 第6章：数据增删改 -- 把表格整理成你要的样子
# ============================================================
# 上一章解决了"窟窿"，这一章解决"形状"：
# 加一列、删几行、改列名、调整列顺序……
# 这些操作每个都很简单，但组合起来就是"数据整理"的全部日常。
#
# ⚠️ 全章核心提醒：pandas 的方法几乎都【返回新对象，不改原表】。
# 两种风格：
#   风格A（推荐）：df = df.drop(...)        # 赋值覆盖
#   风格B（老）：   df.drop(..., inplace=True)  # 3.0 里仍可用但不再推荐
# 尤其是开启"写时复制"的 pandas 3.0，官方统一建议风格 A。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})


# ============================================================
# 6.1 新增列：直接赋值（最常用）
# ============================================================
print("=" * 50)
print("6.1 新增列")

df["总分"] = df["语文"] + df["数学"]        # 数值列直接算
print(df)

df["等级"] = "及格"                          # 广播：整列同一个值
print("\n广播赋值:")
print(df)

# 配合第 4 章的条件赋值，只改满足条件的行：
df.loc[df["总分"] >= 180, "等级"] = "优秀"
print("\n条件赋值更新等级:")
print(df)

# 删除练习列，恢复原状
df = df.drop(columns=["总分", "等级"])


# ============================================================
# 6.2 新增列的进阶：assign（不改原表）
# ============================================================
print("\n" + "=" * 50)
print("6.2 assign")

new_df = df.assign(总分=df["语文"] + df["数学"],
                   平均分=(df["语文"] + df["数学"]) / 2)
print("assign 返回的新表:")
print(new_df)
print("\n原表没变（还是这些列）:", df.columns.tolist())
# assign 的好处：一条链上连续加工，也不弄脏原表：
result = (df.assign(总分=df["语文"] + df["数学"])
            .query("总分 > 170")
            .sort_values("总分", ascending=False))
print("\n链式写法（加分->筛选->排序）:")
print(result)


# ============================================================
# 6.3 insert：在指定位置插入列
# ============================================================
print("\n" + "=" * 50)
print("6.3 insert")

df2 = df.copy()
df2.insert(1, "学号", ["S001", "S002", "S003", "S004"])   # 插到第 1 列
print(df2)
# 赋值写法 df["新列"] 只能把新列加到【最右边】，
# 想插到中间就得用 insert（注意：insert 是原地操作，没有返回值！）。


# ============================================================
# 6.4 删除：drop 行 / drop 列 / pop
# ============================================================
print("\n" + "=" * 50)
print("6.4 drop 与 pop")

print("删除列（columns=）:")
print(df.drop(columns=["语文"]))            # 返回新表

print("\n删除行（index=）:")
print(df.drop(index=[0, 2]))                # 按行标签删（这里标签就是 0~3）

# 删除满足条件的行：先构造布尔掩码再取反
# mask 是"语文<80"的布尔列：[False, False, True, False]
mask = df["语文"] < 80
print("\nmask（语文<80 吗）:")
print(mask)
# ~ 是按位取反运算符，把 True/False 逐个翻转，相当于"不满足条件"：
# ~mask = [True, True, False, True]，即"语文>=80"
print("\n删除语文<80 的行（即保留 ~mask 为 True 的行）:")
print(df[~mask])
# ⚠️ 这里不能用 Python 的 not！not 只能判断单个布尔值，
# 而 mask 是一整列（Series），会报错：
#   df[not mask]  # ValueError: truth value of a Series is ambiguous
# pandas 里逐元素逻辑运算统一用位运算符：~ 取反、& 且、| 或
# 等价写法：df.query("语文 >= 80")

# pop：取出列并从原表移除（像字典的 pop）
df3 = df.copy()
math_col = df3.pop("数学")
print("\npop 出来的数学列:", math_col.tolist())
print("pop 后原表的列:", df3.columns.tolist())


# ============================================================
# 6.5 修改列名：rename / 直接赋值
# ============================================================
print("\n" + "=" * 50)
print("6.5 rename")

print(df.rename(columns={"语文": "chinese", "数学": "math"}))
# rename 返回新表。也可以改行索引（index= 参数）。

# 全部替换列名（不在乎映射关系时）：
df4 = df.copy()
df4.columns = ["name", "class", "chinese", "math"]
print("\n直接赋值替换全部列名:")
print(df4)

# 常见的批量处理（函数式映射）：
df5 = df.copy()
df5 = df5.rename(columns=str.upper)         # 列名全变大写
print("\n列名变大写:")
print(df5.columns.tolist())


# ============================================================
# 6.6 修改值：loc 条件赋值（复习 + 扩展）
# ============================================================
print("\n" + "=" * 50)
print("6.6 修改值")

df6 = df.copy()

# 改单格（第 3 章的 at/loc/iloc 都行）
df6.loc[1, "语文"] = 95 
print(df6)

# 改一整列（配合函数，第 7 章细讲 apply）
df6["语文"] = df6["语文"].apply(lambda x: min(x, 90))   # 90 分封顶
print("\n语文封顶 90:")
print(df6)

# 多列联动修改
df6.loc[df6["语文"] < 80, "数学"] = df6.loc[df6["语文"] < 80, "数学"] + 5  # 补偿加分
print("\n语文<80 的数学加 5:")
print(df6)


# ============================================================
# 6.7 添加行：concat（没有 append！）
# ============================================================
print("\n" + "=" * 50)
print("6.7 添加行")

# ⚠️ 老教程的 df.append() 在 pandas 2.0 就删除了，现在统一用 concat：
new_row = pd.DataFrame({"姓名": ["钱七"], "班级": ["三班"], "语文": [81], "数学": [88]})
df7 = pd.concat([df, new_row], ignore_index=True)
print(df7)
# concat 第 11 章会详细讲，这里先会"加一行"的用法。
# ignore_index=True 重新编号 0,1,2,...（不加的话新行的标签还是 0，会重复！）


# ============================================================
# 6.8 修改列的数据类型：astype
# ============================================================
print("\n" + "=" * 50)
print("6.8 astype")

df8 = pd.DataFrame({"语文": [88, 92], "标签": ["1", "2"]})   # 标签列是字符串
print("原类型:", df8.dtypes.tolist())

df8["标签"] = df8["标签"].astype(int)          # 字符串转整数
print("转后类型:", df8.dtypes.tolist())

# 浮点转整数（截断小数）：
df9 = pd.DataFrame({"价格": [9.9, 19.5]})
df9["价格"] = df9["价格"].astype(int)
print("\n浮点转整数（直接砍掉小数）:", df9["价格"].tolist())

# 含 NaN 的列转 int 会报错（NaN 不是整数），要先处理缺失值：
s = pd.Series([1.5, np.nan])
try:
    s.astype(int)
except (ValueError, TypeError) as e:
    print("\n含 NaN 直接转 int 报错:", str(e)[:60], "...")
# 解决：先 fillna 再转，或用可空类型 Int64（大写 I，可空整数）：
print("用可空整数 Int64:", s.astype("Int64", errors="ignore").tolist())
# Int64 是 pandas 专门的"可空整数"，能同时装下整数和缺失值。
# 注意：float64 直接 astype("Int64") 会报错（1.5 不是整数），
# 整数转可空类型才是它的正确打开方式：
s_int = pd.Series([1, 2], dtype="int64")        # 普通整数列
print("整数列转 Int64:", s_int.astype("Int64").tolist())
# 含 NaN 的浮点列想保住"整数外观"，可以先 round 再转换：
print("先取整再转 Int64:", s.round().astype("Int64").tolist())


# ============================================================
# 6.9 列顺序调整 & 行列重命名综合
# ============================================================
print("\n" + "=" * 50)
print("6.9 调整列顺序")

# 列顺序就是"按名字重新取一遍"：
order = ["数学", "语文", "姓名", "班级"]
print(df[order])
print("\n反着排（倒序列名）:")
print(df[df.columns[::-1]])
# 不存在"move_column"这种专门方法，取列本身就是排序。


# ============================================================
# 6.10 实战：整理一份原始登记表
# ============================================================
print("\n" + "=" * 50)
print("6.10 综合实战")

raw = pd.DataFrame({
    "学生姓名 ": ["张三", "李四", "王五"],      # 注意列名尾部有空格！
    "chinese": ["88", "92", "76"],              # 数字被存成了字符串
    "math": [90, 85, 95],
    "备注": ["", "", "体育生"],                  # 空字符串不是 NaN
})

print("步骤0 原始表（问题：列名带空格、语文是字符串、空串）:")
print(raw)

# 1) 修列名（strip 去掉首尾空格，第 9 章会正式讲 str 访问器）
clean = raw.rename(columns=lambda c: c.strip())
print("\n步骤1 列名去空格:", clean.columns.tolist())

# 2) 字符串转数值
clean["chinese"] = clean["chinese"].astype(int)
print("步骤2 类型:", clean.dtypes.tolist())

# 3) 空字符串当缺失处理，再统一填充
clean["备注"] = clean["备注"].replace("", pd.NA).fillna("无")
print("\n步骤3 备注列:", clean["备注"].tolist())

# 4) 加统计列、排好列顺序
clean = clean.assign(总分=clean["chinese"] + clean["math"])
clean = clean[["学生姓名", "chinese", "math", "总分", "备注"]]
clean.columns = ["姓名", "语文", "数学", "总分", "备注"]      # 顺手改成中文名
print("\n最终结果:")
print(clean)


# ============================================================
# 本章小结
# ============================================================
# 1. 加列：df["新列"] = ...（赋值）/ assign（链式不改原表）/ insert（插中间）
# 2. 删：drop(columns=/index=) 返回新表；pop 取出并移除
# 3. 改名：rename(字典或函数) / 直接给 .columns 赋值
# 4. 改值：df.loc[条件, 列] = 值 是标准句式
# 5. 加行：pd.concat([...], ignore_index=True)（append 已删除）
# 6. 类型：astype；含 NaN 想保持整数用可空类型 "Int64"
# 7. pandas 3.0 推荐赋值风格 df = df.xxx()，inplace 逐渐退出舞台

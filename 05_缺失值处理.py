# -*- coding: utf-8 -*-
# ============================================================
# 第5章：缺失值处理 -- 现实数据的第一课
# ============================================================
# 教科书上的数据干干净净，现实的数据千疮百孔：
# 问卷有人漏填、传感器断电、Excel 里手滑删了个格子……
# "缺失值怎么表示、怎么发现、怎么处理"是数据清洗的核心课题。
#
# Pandas 用三类东西表示缺失：
#   np.nan  -- 老朋友，浮点 NaN（not a number）
#   None    -- Python 的空值，混进数值列会被自动转成 NaN
#   pd.NA   -- pandas 自己的统一缺失标记（新）
# 实际使用中你只需要记住一个入口：pd.isna()，它全都认识。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

# 本章示例：一份有各种"窟窿"的成绩表
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "语文": [88, np.nan, 76, np.nan, 90],
    "数学": [90, 85, np.nan, 78, np.nan],
    "城市": ["北京", None, "上海", "广州", None],   # 字符串列的缺失
})
print("示例数据（注意数学那一列的 NaN）:")
print(df)


# ============================================================
# 5.1 缺失值长什么样：不同列里的表现
# ============================================================
print("=" * 50)
print("5.1 缺失值的表现")

print(df.dtypes)
# 语文/数学 -> float64！本来传的是整数，因为有 NaN，整数装不下，
# pandas 自动升级成 float64（NaN 是浮点值）。
# 这是新手最常见的疑惑："我的整数怎么变小数了？"--因为有缺失。
# 城市 -> str（pandas 3.0 的字符串类型，天生支持缺失值）

# 数值列里的缺失打印为 NaN，字符串列里的缺失也显示为 NaN。
# 用 repr 看单个值：
s_str = pd.Series(["北京", None])
print("\n字符串列的缺失值是:", repr(s_str[1]))   # nan


# ============================================================
# 5.2 发现缺失：isna / notna / info
# ============================================================
print("\n" + "=" * 50)
print("5.2 isna / notna")

print("isna：True 表示这个位置缺失")
print(df.isna())
# 和 np.isnan 一样是布尔矩阵，但 pd.isna 还认识 None/NA，适用面更广。

print("\n每列缺失个数:")
print(df.isna().sum())          # 布尔列求和，True 记 1（NumPy 技巧复用）

print("\n缺失比例:")
print((df.isna().mean() * 100).round(1))

print("\n至少缺一科的行:")
print(df[df.isna().any(axis=1)])     # any(axis=1)：每行里有没有 True
# 你学的 axis 知识在这里发光发热：axis=1 沿着列方向数，得到"每行"的结论。

print("\n完全无缺失的行:")
print(df[df.notna().all(axis=1)])

print("\ninfo() 也能看缺失（non-null 数量）:")
df.info()


# ============================================================
# 5.3 删除缺失：dropna
# ============================================================
print("\n" + "=" * 50)
print("5.3 dropna")

print("dropna() 默认：只要有一格缺失，整行删:")
print(df.dropna())

print("\nhow='all'：只有整行全缺失才删:")
print(df.dropna(how="all"))

print("\nsubset：只根据指定列判断缺失:")
print(df.dropna(subset=["语文"]))
# 实战中最常用！比如"我只关心语文，数学缺不缺无所谓"。

print("\nthresh：至少保留 thresh 个非缺失值才留下:")
print(df.dropna(thresh=3))
# 每行 4 列，thresh=3 表示至少 3 列有值。

# 注意：dropna 返回新表，原表不变（这是所有 pandas 方法的通例）。
# pandas 3.0 中官方更推荐 df = df.dropna(...) 这种赋值写法，
# inplace=True 虽然还能用，但已经不推荐了。


# ============================================================
# 5.4 填充缺失：fillna
# ============================================================
print("\n" + "=" * 50)
print("5.4 fillna")

# 方式 A：填固定值
print("缺失填 0:")
print(df["数学"].fillna(0).tolist())

# 方式 B：填统计量（非常常用）
mean_math = df["数学"].mean()          # mean 默认跳过 NaN
print("\n缺失填平均分 %.2f:" % mean_math)
print(df["数学"].fillna(mean_math).tolist())

# 方式 C：不同列填不同值（传字典）
filled = df.fillna({"语文": df["语文"].mean(), "数学": 0, "城市": "未知"})
print("\n每列填不同值:")
print(filled)

# ⚠️ pandas 3.0：fillna(method='ffill') 已被删除！
# 老教程里的 df.fillna(method='ffill') 现在会直接 TypeError。
# 前向/后向填充用专门的方法：


# ============================================================
# 5.5 前向/后向填充：ffill / bfill
# ============================================================
# 很多数据有时间先后（股价、气温），缺失处用"上一个有效值"填补很合理。

print("\n" + "=" * 50)
print("5.5 ffill / bfill")

s = pd.Series([10, np.nan, np.nan, 40, np.nan])
print("原始:        ", s.tolist())
print("ffill 前向填充:", s.ffill().tolist())   # [10, 10, 10, 40, 40] 用上面的填
print("bfill 后向填充:", s.bfill().tolist())   # [10, 40, 40, 40, 40] 用下面的填

# 等价于老版本的 fillna(method='ffill')，记住新写法即可。
# limit 参数控制最多连续填充几个：
print("ffill(limit=1):", s.ffill(limit=1).tolist())  # [10, 10, nan, 40, 40]


# ============================================================
# 5.6 插值：interpolate
# ============================================================
# 比填充更"讲道理"的做法：缺失值按前后值的趋势线性估出来。

print("\n" + "=" * 50)
print("5.6 interpolate")

s = pd.Series([0.0, np.nan, np.nan, 30.0])
print("线性插值:", s.interpolate().tolist())    # [0, 10, 20, 30]
# 0 和 30 之间缺两个点，线性插值估出 10 和 20。
# 适合连续型数据（温度、价格），不适合类别数据（城市）。


# ============================================================
# 5.7 缺失值的比较陷阱
# ============================================================
print("\n" + "=" * 50)
print("5.7 NaN 参与比较的陷阱")

s = pd.Series([1.0, np.nan, 3.0])
print("s > 2 的结果:", (s > 2).tolist())
# NaN 和任何数比较都得到 False！它不满足任何条件。
# 所以 df[df['列'] > 2] 会【静默丢掉】缺失行--常常不是你想要的。

# 想把缺失的行也选出来，要显式判断：
print("\n>2 或缺失:")
print((s > 2 | s.isna()).tolist())          # ⚠️ 这个写法有优先级问题！
# 注意上面这行写错了：| 的优先级比 > 高，(2 | s.isna()) 会先算。
# 正确写法是每个条件都加括号：
print("正确写法:")
print(((s > 2) | s.isna()).tolist())
# 这就是第 4 章"每个条件加括号"规矩的又一体现。


# ============================================================
# 5.8 判断缺失的姿势总结
# ============================================================
print("\n" + "=" * 50)
print("5.8 本图速查")

# pd.NA 是 pandas 自己的"统一缺失标记"，放进数值列要先声明可空类型：
s = pd.Series([1.0, np.nan, None, pd.NA], dtype="Float64")   # 大写 F = 可空浮点
print(s.tolist())

# 判断缺失只能用 isna，不能用 ==：
print("s == np.nan 的结果:", (s == np.nan).tolist())
# 全是 False！NaN 不等于任何值，包括它自己（IEEE 754 的规矩）。
print("s.isna() 的结果:  ", s.isna().tolist())
# [False, True, True, True] -- isna 才是正确的工具，
# 而且它把 NaN / None / NA 一视同仁，全都认得。

# 系列 API：
#   df.isna() / df.notna()   判断
#   df.dropna()              删除
#   df.fillna(v)             填充
#   df.ffill() / df.bfill()  前后向填充
#   df.interpolate()         插值


# ============================================================
# 5.9 实战：清洗一份"脏"成绩表
# ============================================================
print("\n" + "=" * 50)
print("5.9 综合实战")

dirty = pd.DataFrame({
    "姓名": ["张三", None, "李四", "王五", "李四"],
    "语文": [88, np.nan, 92, np.nan, 92],
    "数学": [np.nan, 85, np.nan, 78, np.nan],
})

print("步骤1 原始脏数据:")
print(dirty)

# 步骤2：姓名缺失的行没法用，删掉
step2 = dirty.dropna(subset=["姓名"])
print("\n步骤2 删掉姓名缺失的行:")
print(step2)

# 步骤3：完全重复的行去掉（第 8 章还会细讲）
step3 = step2.drop_duplicates()
print("\n步骤3 去重:")
print(step3)

# 步骤4：语文缺失填平均分，数学缺失填 0（缺考当 0 分）
step4 = step3.fillna({"语文": step3["语文"].mean(), "数学": 0})
print("\n步骤4 填充:")
print(step4.round(1))

# 这套"删 -> 去重 -> 填"的三板斧，就是数据清洗的基本流程。


# ============================================================
# 本章小结
# ============================================================
# 1. 缺失的表示：数值列 NaN（整数列会自动变 float），字符串列也有 NaN
# 2. 判断用 isna/notna，== np.nan 永远是 False
# 3. 删除 dropna：subset 指定列、how='all'、thresh
# 4. 填充 fillna：固定值/统计量/字典；前后向用 ffill/bfill（3.0 新写法）
# 5. interpolate 线性插值适合连续数据
# 6. NaN 与任何数比较都是 False，条件筛选会静默丢掉缺失行

# -*- coding: utf-8 -*-
# ============================================================
# 第7章：运算与统计 -- 从"能算"到"会算"
# ============================================================
# 这一章分两部分：
#   前半：统计方法（sum/mean/max/...），基本是 NumPy 第 7 章的复习，
#         但多了"自动跳过 NaN"和"按列计算"两个增强
#   后半：apply / map / transform -- 当内置方法不够用时，
#         对每个元素/每行/每列执行"你自己的函数"
#
# 性能心法（贯穿全章）：
#   能用内置向量化方法（+、sum、mean...）就不要用 apply 循环，
#   前者是 C 速度，后者是 Python 速度，差几十倍是常事。
#   apply 是"最后的选择"，不是"第一反应"。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
    "体育": [70, 65, 80, np.nan],      # 赵六缺考体育
})


# ============================================================
# 7.1 基础统计：默认按列
# ============================================================
print("=" * 50)
print("7.1 基础统计")

print("每列平均（数值列）:")
print(df.mean(numeric_only=True))
# numeric_only=True：跳过"姓名"这种字符串列。
# （pandas 3.0 遇到字符串列不加这个参数会报错，记住带上。）

print("\n每列总和/最大/最小:")
print(df[["语文", "数学", "体育"]].sum())
print(df[["语文", "数学", "体育"]].max())
print(df[["语文", "数学", "体育"]].min())

# 注意体育列：mean 是 (70+65+80)/3 = 71.67，NaN 被自动跳过。
# 想把 NaN 算进去，先 fillna(0)。

print("\naxis=1 按行算（每人的平均分）:")
print(df[["语文", "数学", "体育"]].mean(axis=1))
# axis 的含义和 NumPy 完全一致：axis=0 沿着行方向压扁（得到每列的），
# axis=1 沿着列方向压扁（得到每行的）。只是 pandas 里 axis=0 是默认。


# ============================================================
# 7.2 累计与排名类：cumsum / cummax / diff / pct_change
# ============================================================
print("\n" + "=" * 50)
print("7.2 累计类")

s = pd.Series([10, 20, 15, 30], index=["1月", "2月", "3月", "4月"])
print("累计和 cumsum:", s.cumsum().tolist())
print("累计最大 cummax:", s.cummax().tolist())
print("逐期差 diff:  ", s.diff().tolist())          # 当月 - 上月
print("环比 pct_change:", s.pct_change().round(2).tolist())  # (今-昨)/昨
# 这几个在做销售/增长分析时天天用。


# ============================================================
# 7.3 相关系数与协方差
# ============================================================
print("\n" + "=" * 50)
print("7.3 corr")

df2 = pd.DataFrame({
    "学习时长": [2, 4, 6, 8],
    "成绩": [60, 70, 80, 90],
    "游戏时长": [8, 6, 4, 2],
})
print(df2.corr())
# 学习时长和成绩完全正相关（1.0），和游戏时长完全负相关（-1.0）。
# corr 取值 [-1, 1]：越接近 1 越同向，越接近 -1 越反向，0 无线性关系。
print("\n只看两列:", df2["学习时长"].corr(df2["成绩"]))


# ============================================================
# 7.4 值计数：value_counts / unique / nunique
# ============================================================
print("\n" + "=" * 50)
print("7.4 value_counts")

cities = pd.Series(["北京", "上海", "北京", "广州", "北京"])
print("出现次数:")
print(cities.value_counts())

print("\n占比（normalize=True）:")
print(cities.value_counts(normalize=True))

print("\n去重列表 unique:", cities.unique().tolist())
print("不同值个数 nunique:", cities.nunique())
# value_counts 是"分类列的 describe()"，看类别分布的第一反应就该是它。


# ============================================================
# 7.5 map：逐元素映射（Series 专用）
# ============================================================
print("\n" + "=" * 50)
print("7.5 map")

df3 = pd.DataFrame({"等级": ["A", "B", "A", "C"]})

# 用法 A：字典映射（最常见）-- "翻译"类别值
score_map = {"A": 4.0, "B": 3.0, "C": 2.0}
print(df3["等级"].map(score_map).tolist())

# 用法 B：函数映射 -- 对每个元素调用
print(df3["等级"].map(lambda x: x + "等").tolist())

# 用法 C：配合其他 Series 做查找（像 Excel 的 VLOOKUP）
name_to_score = pd.Series({"张三": 88, "李四": 92})
names = pd.Series(["张三", "李四", "王五"])
print(name_to_score.reindex(names).tolist())   # 王五查不到 -> NaN
# map 的字典/函数用法覆盖 90% 场景；注意 map 只作用于【单个 Series】。


# ============================================================
# 7.6 apply：一行/一列地执行函数
# ============================================================
print("\n" + "=" * 50)
print("7.6 apply")

df4 = pd.DataFrame({
    "语文": [88, 59, 92],
    "数学": [90, 45, 85],
})

# axis=1：每次把【一行】（一个 Series）交给函数 -- "逐行处理"
def evaluate(row):
    total = row["语文"] + row["数学"]
    if row["语文"] < 60 or row["数学"] < 60:
        return "有挂科"
    return "优秀" if total >= 175 else "合格"

print(df4.apply(evaluate, axis=1).tolist())

# axis=0（默认）：每次把【一列】交给函数
print(df4.apply(lambda col: col.max() - col.min()).tolist())   # 每列极差

# Series 也有 apply（等价于 map 的函数用法）：
print(pd.Series([-1, 2, -3]).apply(abs).tolist())


# ============================================================
# 7.7 df.map：逐元素（DataFrame 版，替代老 applymap）
# ============================================================
print("\n" + "=" * 50)
print("7.7 df.map")

# ⚠️ pandas 3.0：df.applymap() 已删除，逐元素处理统一用 df.map()
df5 = pd.DataFrame({"语文": [88, 92], "数学": [76, 85]})

# 把每个格子都格式化成字符串（演示用）：
print(df5.map(lambda x: f"{x}分"))
# 注意：如果不同列类型不同，函数要能处理所有类型。
# 例如对含字符串列的整表 map 时，先选数值子集。


# ============================================================
# 7.8 transform：算完贴回原来的形状
# ============================================================
# apply 聚合后形状会变（比如每列均值只剩 1 个数）；
# transform 的结果必须和原数据【一样长】，常用于"组内标准化"
# （配合 groupby 是黄金搭档，第 10 章见）。

print("\n" + "=" * 50)
print("7.8 transform")

s = pd.Series([80, 90, 100])
# transform 传"逐元素变换函数"，输出和输入一样长：
print("transform(np.sqrt):")
print(s.transform(np.sqrt).tolist())
# 典型用途：每行减去所在列的均值（"中心化"）：
# 聚合值广播回去需要 transform + groupby 的组合（第 10 章见），
# 普通列直接用减法广播即可（NumPy 的广播思想）：

df6 = pd.DataFrame({"语文": [80, 90, 100], "数学": [60, 70, 80]})
centered = df6 - df6.mean()          # 每列减去各自的均值
print("\n中心化后（每列减去该列均值）:")
print(centered)


# ============================================================
# 7.9 性能对比：向量化 vs apply（亲眼见识差距）
# ============================================================
print("\n" + "=" * 50)
print("7.9 性能对比")

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
# 在 10 万数据上差距是几倍到几十倍，数据越大越夸张。
# 结论：先想向量化，实在写不出来（复杂 if-else 逻辑等）再用 apply。


# ============================================================
# 7.10 实战：给成绩表做一份"体检报告"
# ============================================================
print("\n" + "=" * 50)
print("7.10 综合实战")

report = df.copy()
report = report.assign(
    总分=report[["语文", "数学", "体育"]].fillna(0).sum(axis=1),
    平均分=report[["语文", "数学", "体育"]].fillna(0).mean(axis=1).round(1),
    平均分与全班差=report["语文"] - report["语文"].mean(),
)
report["评语"] = report["总分"].apply(
    lambda t: "优秀" if t >= 250 else ("良好" if t >= 240 else "继续努力")
)
print(report)

print("\n全班各科统计:")
print(df[["语文", "数学", "体育"]].agg(["mean", "max", "min"]).round(1))
# agg 一次算多个统计量，第 10 章配合 groupby 会大放异彩。


# ============================================================
# 本章小结
# ============================================================
# 1. 统计方法默认按列（axis=0）且自动跳过 NaN；axis=1 变按行
# 2. 字符串列在场时统计要 numeric_only=True 或先选数值列
# 3. corr 看相关性；value_counts 看类别分布
# 4. map(Series)：字典翻译/函数映射；apply：逐行(axis=1)/逐列(axis=0)
# 5. df.map 是老 applymap 的替代（pandas 3.0）
# 6. transform 结果形状与原表相同（广播回去）
# 7. 性能优先级：内置向量化 >> apply 循环

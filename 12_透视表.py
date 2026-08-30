# -*- coding: utf-8 -*-
# ============================================================
# 第12章：透视表 -- pivot / pivot_table / melt
# ============================================================
# "每个班男女生的平均分"用 groupby 能算，但结果是一根"长条"；
# 想要"班级为行、性别为列"的**交叉表格**（Excel 的透视表那样），
# 就轮到 pivot_table 出场。
#
# 另一个方向的问题：表格太"宽"不好分析时，用 melt 把它"熔"成长条。
# 一句话分工：
#   pivot_table：长表 -> 宽表（交叉汇总）
#   melt      ：宽表 -> 长表（拉直）

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

# 长格式的原始数据（数据库里最常见的存储格式）
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七", "孙八"],
    "班级": ["一班", "一班", "一班", "二班", "二班", "二班"],
    "性别": ["男", "女", "男", "女", "男", "女"],
    "语文": [88, 92, 76, 85, 90, 73],
    "数学": [90, 85, 95, 78, 92, 88],
})
print("原始长表:")
print(df)


# ============================================================
# 12.1 pivot_table 入门：行 x 列 x 值
# ============================================================
print("=" * 50)
print("12.1 pivot_table")

pt = pd.pivot_table(
    df,
    index="班级",        # 行：班级
    columns="性别",      # 列：性别
    values="语文",       # 单元格里放：语文
    aggfunc="mean",      # 多个值怎么合：取平均
)
print(pt)
# 结果解读：一班男生语文平均 (88+76)/2=82，二班女生 (85+73)/2=79。

# 对照 groupby 写法（同样的数据，长条形状）：
print("\ngroupby 的长条形状（同一份数字）:")
print(df.groupby(["班级", "性别"])["语文"].mean().unstack())
# unstack 就是"把多层索引的最后一级拉出去当列"，
# pivot_table(index, columns, values) ≈ groupby([index,columns])[values].agg().unstack()


# ============================================================
# 12.2 pivot_table 的常用参数
# ============================================================
print("\n" + "=" * 50)
print("12.2 常用参数")

# 多个值列：values 传列表
print("两科都看:")
print(pd.pivot_table(df, index="班级", columns="性别",
                     values=["语文", "数学"], aggfunc="mean"))

# margins=True 加汇总行/列（Excel 透视表的"总计"）：
print("\nmargins 加总计:")
print(pd.pivot_table(df, index="班级", values=["语文", "数学"],
                     aggfunc="mean", margins=True))

# fill_value 填充空格子（默认 NaN）：
print("\nfill_value=0:")
print(pd.pivot_table(df, index="班级", columns="性别",
                     values="语文", aggfunc="mean", fill_value=0))

# 多层行索引：index 传列表
print("\n班级+性别做多层行:")
print(pd.pivot_table(df, index=["班级", "性别"], values="数学", aggfunc="mean"))


# ============================================================
# 12.3 pivot_table vs pivot
# ============================================================
print("\n" + "=" * 50)
print("12.3 pivot（不汇总版）")

# pivot 只做"重新摆放"：不聚合，要求 行x列 组合不重复。
df2 = pd.DataFrame({
    "学期": ["期中", "期中", "期末", "期末"],
    "科目": ["语文", "数学", "语文", "数学"],
    "分数": [88, 90, 92, 95],
})
print(df2.pivot(index="学期", columns="科目", values="分数"))
# 行列交叉处正好一个值，pivot 直接摆好；
# 若有重复（比如两个"期中语文"），pivot 报错，必须用 pivot_table 聚合。

# 记忆：pivot = 纯变形；pivot_table = 变形 + 聚合。


# ============================================================
# 12.4 交叉表 crosstab：数人头专用
# ============================================================
print("\n" + "=" * 50)
print("12.4 crosstab")

# crosstab 就是"数个数"的透视表（values 不用给，默认计数）：
print(pd.crosstab(df["班级"], df["性别"]))
# 一班男2女1，二班男1女1。看"类别 x 类别"的分布一目了然。

# 也能带值聚合（和 pivot_table 等价的另一种写法）：
print("\ncrosstab 带 values:")
print(pd.crosstab(df["班级"], df["性别"], values=df["语文"], aggfunc="mean"))
# 归一化看占比：
print("\nnormalize='index' 每行占比:")
print(pd.crosstab(df["班级"], df["性别"], normalize="index").round(2))


# ============================================================
# 12.5 melt：把宽表熔成长表
# ============================================================
# 机器学习库、绘图库（比如 seaborn）大多喜欢吃"长表"，
# 手里的宽表就得 melt 一下。

print("\n" + "=" * 50)
print("12.5 melt")

wide = pd.pivot_table(df, index="姓名", values=["语文", "数学"], aggfunc="first")
print("宽表:")
print(wide)

long = wide.reset_index().melt(
    id_vars="姓名",            # 保持不动的列
    value_vars=["语文", "数学"],  # 要熔掉的列
    var_name="科目",            # 熔掉后"列名"存到这列
    value_name="分数",          # 熔掉后"值"存到这列
)
print("\n熔成长表:")
print(long)
# 语文、数学两列被"熔"成了 科目+分数 两列，行数翻倍。
# melt 的方向和 pivot 正好相反，两者互为逆操作（近似）。


# ============================================================
# 12.6 stack / unstack：索引级别的宽长转换
# ============================================================
print("\n" + "=" * 50)
print("12.6 stack / unstack")

p = df.groupby(["班级", "性别"])[["语文", "数学"]].mean()
print("两层索引的表:")
print(p)

print("\nunstack（把最内层索引拉出去当列）:")
print(p.unstack())
# unstack 默认拉最后一层（性别）；unstack(0) 拉第一层（班级）。

print("\n再 stack 回去:")
print(p.unstack().stack())
# stack 是 unstack 的反向：把列压回索引。
# 一句话：多层索引的表，用 stack/unstack 在"宽、长"之间切换。

# 补充：恢复"班级 性别 语文 数学"的平铺格式：
print("\nreset_index 拉平多层索引:")
print(p.reset_index())


# ============================================================
# 12.7 实战：销售数据透视
# ============================================================
print("\n" + "=" * 50)
print("12.7 综合实战")

sales = pd.DataFrame({
    "月份": ["1月"] * 3 + ["2月"] * 3 + ["3月"] * 3,
    "城市": ["北京", "上海", "广州"] * 3,
    "产品": ["A", "A", "B", "B", "A", "A", "B", "B", "A"],
    "销售额": [100, 150, 200, 120, 180, 210, 90, 160, 240],
})
print("原始流水:")
print(sales)

# 1) 月 x 城市 的销售额透视（带总计）
pt1 = pd.pivot_table(sales, index="月份", columns="城市",
                     values="销售额", aggfunc="sum",
                     margins=True, margins_name="合计")
print("\n月 x 城市:")
print(pt1)

# 2) 月 x 产品，看平均单笔
pt2 = pd.pivot_table(sales, index="月份", columns="产品",
                     values="销售额", aggfunc="mean").round(1)
print("\n月 x 产品（平均）:")
print(pt2)

# 3) 交叉计数：每个城市卖了几单
print("\n城市 x 产品 订单数:")
print(pd.crosstab(sales["城市"], sales["产品"]))

# 4) 熔成长表（喂给绘图库的格式）
long_sales = sales.melt(id_vars=["月份", "城市"], value_vars=["销售额"])
print("\nmelt 后形状:", long_sales.shape)


# ============================================================
# 本章小结
# ============================================================
# 1. pivot_table(index, columns, values, aggfunc)：长->宽交叉汇总
#    ≈ groupby([行,列])[值].agg().unstack()
# 2. margins=True 加总计；fill_value 填空格；index/columns 都可传列表
# 3. pivot 是纯变形不聚合（组合必须唯一）；crosstab 是计数透视
# 4. melt(id_vars, value_vars)：宽->长，配合绘图库
# 5. stack/unstack 在多层索引上做宽长互转
#
# 选型口诀：要交叉报表用 pivot_table，要数人头用 crosstab，
#           要喂给画图库用 melt。

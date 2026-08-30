# -*- coding: utf-8 -*-
# ============================================================
# 第8章：排序与排名 -- 让数据自己说话
# ============================================================
# "谁考得最好？""哪个商品卖得最多？"——答案全靠排序；
# "我排第几？"——这是排名。
# 排序 sort_values 和排名 rank 是一对兄弟，容易混淆：
#   sort_values：把行【重新排列】（数据顺序变了）
#   rank：       给每个值【标注名次】（数据顺序不变，多了一列名次）
#
# 另外本章顺带处理两个"排序相关的杂物"：
#   重复值 duplicated/drop_duplicates、分箱 cut/qcut。
# 它们本质都是"给数据定位次序/类别"，放在这里最顺。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七", "孙八"],
    "班级": ["一班", "一班", "一班", "二班", "二班", "二班"],
    "总分": [260, 245, 260, 230, 245, 210],
    "数学": [90, 85, 95, 78, 85, 70],
})


# ============================================================
# 8.1 sort_values：按值排序
# ============================================================
print("=" * 50)
print("8.1 sort_values")

print("按总分升序（默认 ascending=True）:")
print(df.sort_values("总分"))

print("\n按总分降序:")
print(df.sort_values("总分", ascending=False))

# 排序后行索引跟着行走（乱了）。一般习惯重置索引：
print("\n排序后重置索引:")
print(df.sort_values("总分", ascending=False).reset_index(drop=True).head(3))

# 返回新表不改原表；要保留就用变量接住。


# ============================================================
# 8.2 多列排序：先按谁、再按谁
# ============================================================
print("\n" + "=" * 50)
print("8.2 多列排序")

# 场景：总分相同时按数学高者在前。
print(df.sort_values(["总分", "数学"], ascending=[False, False]))
# by 传列表，ascending 也传列表一一对应（还可以一升一降）。

# 更经典的场景："班级内按总分排序"：
print("\n先按班级、再按总分:")
print(df.sort_values(["班级", "总分"], ascending=[True, False]))
# 注意"一班"排在"二班"前——中文字符串按 Unicode 码点排序，
# 恰好符合预期；但"十班"会排在"二班"前（'十'<'二'的码点），
# 类别顺序有要求时用下一节的 Categorical。


# ============================================================
# 8.3 类别排序：Categorical 类型
# ============================================================
print("\n" + "=" * 50)
print("8.3 自定义类别顺序")

df2 = df.copy()
df2["班级"] = pd.Categorical(df2["班级"], categories=["一班", "二班"])
# 想要"二班在前"时，把 categories 反过来写即可：
df2["班级"] = df2["班级"].cat.reorder_categories(["二班", "一班"])
print(df2.sort_values("班级")[["姓名", "班级"]])
# Categorical 是一种"有序类别"类型，month、星期、评级都适合用它。


# ============================================================
# 8.4 sort_index：按索引排序
# ============================================================
print("\n" + "=" * 50)
print("8.4 sort_index")

s = pd.Series([1, 2, 3], index=[3, 1, 2])
print("按索引升序:")
print(s.sort_index())

# 用途：操作把行序弄乱后（比如筛选、采样）恢复顺序。
shuffled = df.sample(frac=1.0, random_state=1)   # 全部行随机打乱
print("\n打乱后的索引:", shuffled.index.tolist())
print("sort_index 复原后:", shuffled.sort_index().index.tolist())


# ============================================================
# 8.5 rank：排名次（数据顺序不变）
# ============================================================
print("\n" + "=" * 50)
print("8.5 rank")

s = pd.Series([100, 90, 100, 80], index=["张三", "李四", "王五", "赵六"])
print("原始:", s.tolist())

print("\nrank()（默认 method='average'，默认升序）:")
print(s.rank().tolist())
# 张三王五并列第一，名次取平均 (1+2)/2 = 1.5；李四第 2... 等一下：
# 实际输出 [3.5, 2.0, 3.5, 1.0]？？不，仔细看：升序排名，80 最小是第 1。
# 90 是第 2，两个 100 并列第 3、4 -> 平均 3.5。
# 是的，rank 默认"值越小名次越小"（升序），比的是"小"不是"大"。

print("\nascending=False：高分=第1名:")
print(s.rank(ascending=False).tolist())    # 两个100并列1.5，90是3，80是4

# 并列的处理方式 method：
print("\nmethod='min'（并列取最小名次，体育记分常用）:")
print(s.rank(ascending=False, method="min").tolist())   # [1, 3, 1, 4]
print("method='dense'（并列占一个名次，不跳号）:")
print(s.rank(ascending=False, method="dense").tolist()) # [1, 2, 1, 3]
print("method='first'（并列时先出现者靠前）:")
print(s.rank(ascending=False, method="first").tolist()) # [1, 3, 2, 4]

# rank 返回的是【和原数据一样长的名次列】，所以常直接赋值成新列：
df3 = df.copy()
df3["名次"] = df3["总分"].rank(ascending=False, method="min").astype(int)
print("\n给成绩表加名次列:")
print(df3.sort_values("名次"))


# ============================================================
# 8.6 nlargest / nsmallest：只要前 N 名
# ============================================================
print("\n" + "=" * 50)
print("8.6 nlargest / nsmallest")

print("总分前三名:")
print(df.nlargest(3, "总分")[["姓名", "总分"]])

print("\n数学最低的两名:")
print(df.nsmallest(2, "数学")[["姓名", "数学"]])
# 等价于 sort_values().head(n)，但意图更直白，大表上也更快。


# ============================================================
# 8.7 重复值：duplicated / drop_duplicates
# ============================================================
print("\n" + "=" * 50)
print("8.7 重复值处理")

dup = pd.DataFrame({
    "姓名": ["张三", "张三", "李四", "李四", "王五"],
    "总分": [260, 260, 245, 250, 230],
})
print(dup)
print("\nduplicated（第一次出现标记 False，之后 True）:")
print(dup.duplicated().tolist())
print("\ndrop_duplicates 删完全重复的行:")
print(dup.drop_duplicates())
print("\ndrop_duplicates(subset='姓名') 只看姓名列:")
print(dup.drop_duplicates(subset="姓名"))
# keep 参数：'first'（默认，留第一条）/ 'last'（留最后一条）/ False（全删）


# ============================================================
# 8.8 分箱：cut / qcut -- 把连续值切成段
# ============================================================
print("\n" + "=" * 50)
print("8.8 cut / qcut")

scores = pd.Series([56, 78, 92, 65, 88])

# cut：手动指定区间（右闭：左开右闭 (a, b]）
grade = pd.cut(scores, bins=[0, 60, 80, 100], labels=["不及格", "及格", "优秀"])
print(grade.tolist())
# labels 直接给每段起名，输出瞬间可读。
# 默认区间是 (0,60]、(60,80]、(80,100]，右端包含。

# qcut：按分位数切，保证每段【数量差不多】
income = pd.Series([2000, 3500, 5000, 8000, 12000, 25000, 40000])
print("\nqcut 3 段（人数尽量均匀）:")
print(pd.qcut(income, 3).tolist())
# 收入这种偏态数据用 cut 均匀切会一边倒，qcut 更合理。

# 统计每段人数（分箱 + value_counts = 分布分析）:
print("\n各分数段人数:")
print(grade.value_counts())


# ============================================================
# 8.9 实战：一份完整的"榜单"
# ============================================================
print("\n" + "=" * 50)
print("8.9 综合实战")

board = df.copy()

board["总分排名"] = board["总分"].rank(ascending=False, method="dense").astype(int)
board["数学排名"] = board["数学"].rank(ascending=False, method="dense").astype(int)
board = board.sort_values(["总分排名", "数学排名"]).reset_index(drop=True)
board["档次"] = pd.cut(
    board["总分"],
    bins=[0, 220, 250, 300],
    labels=["C", "B", "A"],
)
print(board)
print("\n各档次人数:")
print(board["档次"].value_counts())
print("\n班级人数分布:")
print(board["班级"].value_counts())


# ============================================================
# 本章小结
# ============================================================
# 1. sort_values（单列/多列，ascending 可传列表）；sort_index 按索引
# 2. 类别有固定顺序时用 pd.Categorical
# 3. rank 是"标注名次"，不改变顺序；method 处理并列：
#    average/min/dense/first，ascending=False 让大的排第 1
# 4. nlargest/nsmallest 快速取前 N
# 5. duplicated 标记重复行；drop_duplicates(subset=, keep=) 去重
# 6. cut 按区间分箱（labels 命名）；qcut 按分位数分箱（每段人数均匀）

# -*- coding: utf-8 -*-
# ============================================================
# 第11章：合并拼接 -- merge / concat / join
# ============================================================
# 一张表往往不够用：学生表一张、成绩表一张，要拼起来分析。
# Pandas 合并表有三大件：
#   pd.concat  ：简单摞起来（上下叠 / 左右拼），不看内容只看形状
#   pd.merge   ：按"键"配对（像 SQL 的 JOIN），日常主力
#   df.join    ：merge 按索引连接的快捷方式
#
# 用生活比喻：
#   concat 是把两沓纸摞成一沓（或左右并排）；
#   merge 是拿着两张名单对暗号（学号对上了才拼一行）。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

# 两张主示例表：学生表 + 成绩表，靠"学号"关联
students = pd.DataFrame({
    "学号": ["S001", "S002", "S003", "S004"],
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
})
scores = pd.DataFrame({
    "学号": ["S002", "S003", "S004", "S005"],
    "语文": [92, 76, 85, 90],
    "数学": [85, 95, 78, 88],
})
print("学生表:")
print(students)
print("\n成绩表:")
print(scores)


# ============================================================
# 11.1 concat：上下摞 / 左右拼
# ============================================================
print("=" * 50)
print("11.1 concat")

# 竖向摞（默认 axis=0）：追加行（比如两个月的表拼成年表）
more_scores = pd.DataFrame({"学号": ["S006"], "语文": [70], "数学": [65]})
stacked = pd.concat([scores, more_scores])
print(stacked)
# 注意行索引 0~3,0 有重复！ignore_index=True 重新编号：
print("\nignore_index=True:")
print(pd.concat([scores, more_scores], ignore_index=True))

# 横向拼（axis=1）：按行索引左右并排
extra = pd.DataFrame({"体育": [80, 75, 90, 85]})
print("\n左右拼 axis=1:")
print(pd.concat([scores, extra], axis=1))
# axis=1 时按行索引对齐，行的顺序/数量要自己对得上，否则出 NaN。

# 竖向摞时列名不同会怎样：
diff_cols = pd.DataFrame({"学号": ["S007"], "英语": [77], "数学": [66]})
print("\n列名不完全一致时的竖拼:")
print(pd.concat([scores, diff_cols], ignore_index=True))
# 对不上的列填 NaN（外连接的感觉）。concat 的 join 参数可控制：
print("\njoin='inner' 只保留共有列:")
print(pd.concat([scores, diff_cols], ignore_index=True, join="inner"))


# ============================================================
# 11.2 merge 入门：四种连接方式
# ============================================================
# merge(students, scores, on="学号", how="...")
# on：用哪列对暗号；how：对不上怎么办（inner/left/right/outer）。
# 记住下面这张图，merge 就懂了 90%：
#
#   students: S001 S002 S003 S004        scores: S002 S003 S004 S005
#              └────┼────┘ ── 对暗号 ── └────┼────┘
#   共同：S002 S003 S004 | 只在左：S001 | 只在右：S005
#
#   how='inner' 只留共同     -> S002 S003 S004
#   how='left'   以左表为准   -> S001 S002 S003 S004（S005 丢弃）
#   how='right'  以右表为准   -> S002 S003 S004 S005
#   how='outer'  全都要       -> S001 S002 S003 S004 S005

print("\n" + "=" * 50)
print("11.2 merge 四种 how")

print("inner（默认，只留两边都有的）:")
print(pd.merge(students, scores, on="学号"))

print("\nleft（以左表为准，右表缺的填 NaN）:")
print(pd.merge(students, scores, on="学号", how="left"))
# 张三（S001）在成绩表没有记录 -> 语文数学是 NaN，但行保住了。

print("\nright（以右表为准）:")
print(pd.merge(students, scores, on="学号", how="right"))
# S005 在学生表没有 -> 姓名 NaN。

print("\nouter（全都要，能配的配，配不上的留 NaN）:")
print(pd.merge(students, scores, on="学号", how="outer"))
# S001 和 S005 都保留了，各自缺的部分是 NaN。


# ============================================================
# 11.3 merge 细节：键名不同 / 多键 / 重名列
# ============================================================
print("\n" + "=" * 50)
print("11.3 merge 细节")

# 两边键列名不同：left_on / right_on
scores2 = scores.rename(columns={"学号": "student_id"})
print(pd.merge(students, scores2, left_on="学号", right_on="student_id"))
# 两列都会保留（学号和 student_id 内容一样），再 drop 掉一个即可。

# 多个键同时匹配（on 传列表）：
a = pd.DataFrame({"学号": ["S001", "S001"], "学期": ["上", "下"], "分": [80, 90]})
b = pd.DataFrame({"学号": ["S001", "S001"], "学期": ["上", "下"], "评": ["良", "优"]})
print("\n多键合并:")
print(pd.merge(a, b, on=["学号", "学期"]))

# 两边有同名的非键列 -> 自动加后缀 _x / _y：
a2 = pd.DataFrame({"学号": ["S001"], "分数": [88]})
b2 = pd.DataFrame({"学号": ["S001"], "分数": [92]})
print("\n重名列自动加后缀:")
print(pd.merge(a2, b2, on="学号"))
# 也可以自己指定后缀：suffixes=("_期中", "_期末")

# indicator：加一列显示每行来自哪种匹配（排查利器）：
print("\nindicator=True:")
print(pd.merge(students, scores, on="学号", how="outer", indicator=True)
      [["学号", "_merge"]])
# both=两边都有，left_only=只在左表，right_only=只在右表。
# "哪些学号没匹配上"这种排查问题，indicator 一眼看出。


# ============================================================
# 11.4 验证合并：validate 参数
# ============================================================
print("\n" + "=" * 50)
print("11.4 validate")

# validate 声明你预期的关系，不符合就报错（防止数据意外）：
#   "one_to_one"（一对一）/"one_to_many"（一对多）/"many_to_one"
try:
    pd.merge(students, scores, on="学号", validate="one_to_one")
except pd.errors.MergeError as e:
    print("one_to_one 校验失败:", e)
# 本例一个学号在成绩表可能出现多次，所以报错；改成 one_to_many 就通过：
merged = pd.merge(students, scores, on="学号", how="left", validate="one_to_many")
print("one_to_many 通过，形状:", merged.shape)


# ============================================================
# 11.5 join：按索引连接的快捷方式
# ============================================================
print("\n" + "=" * 50)
print("11.5 join")

# join 默认用【行索引】当键（merge 默认用列）：
left = students.set_index("学号")
right = scores.set_index("学号")
print(left.join(right))
# 等价于 pd.merge(left, right, left_index=True, right_index=True, how='left')
# join 也支持 on 参数，但多数场景直接用 merge 更清晰统一。
# 建议：join 看得懂即可，写代码统一用 merge。


# ============================================================
# 11.6 陷阱合集：merge 常见翻车现场
# ============================================================
print("\n" + "=" * 50)
print("11.6 常见陷阱")

# 陷阱1：键列的类型不一致（一边是字符串一边是数字）
# 新版 pandas 直接报错拦住你（旧版更坑：静默返回空表，一个 Warning 完事）：
s1 = pd.DataFrame({"k": ["1", "2"], "v": [10, 20]})
s2 = pd.DataFrame({"k": [1, 2], "v": [30, 40]})
try:
    pd.merge(s1, s2, on="k")
except ValueError as e:
    print("类型不一致时直接报错:")
    print(" ", e)
print("统一类型后可以合并:", pd.merge(s1, s2.astype({"k": str}), on="k").shape[0], "行")
# 教训：合并前先 df['键'].dtype 看一眼两边类型是否一致。

# 陷阱2：忘了 how，默认 inner 悄悄丢数据
# 需求"所有学生的成绩"却写了 inner -> 没成绩的学生消失。
# 起手式建议：写 merge 时永远显式写 how=...。

# 陷阱3：重复键导致行数爆炸
dup_scores = pd.concat([scores, scores.head(1)])   # S002 出现两次
boom = pd.merge(students, scores, on="学号")
boom2 = pd.merge(students, dup_scores, on="学号")
print("\n正常合并行数:", len(boom), "；键重复后:", len(boom2), "（一对多扩散）")
# 合并前先查键是否唯一：scores['学号'].is_unique


# ============================================================
# 11.7 实战：三表合并
# ============================================================
print("\n" + "=" * 50)
print("11.7 综合实战")

# 场景：学生表 + 成绩表 + 班主任表（通过班级关联）
teachers = pd.DataFrame({
    "班级": ["一班", "二班", "三班"],
    "班主任": ["刘老师", "陈老师", "杨老师"],
})

final = (students
         .merge(scores, on="学号", how="left")       # 补成绩
         .merge(teachers, on="班级", how="left")     # 补班主任
         )
final["总分"] = final[["语文", "数学"]].sum(axis=1)
print(final)
print("\n各班（含班主任）总分平均:")
print(final.groupby(["班级", "班主任"])["总分"].mean().round(1))
# merge 可以链式串联，一张"宽表"就这样层层拼出来。
# 注意 how='left' 保证学生一个都不丢（分析主体是学生）。


# ============================================================
# 本章小结
# ============================================================
# 1. concat：摞行（axis=0, ignore_index=True）/ 并列（axis=1）
# 2. merge(on=, how=)：inner / left / right / outer，画两个圈想一想
# 3. 键名不同用 left_on/right_on；重名列加后缀；indicator 排查匹配
# 4. validate 校验一对一/一对多关系
# 5. join 是按索引的 merge 快捷键；统一用 merge 即可
# 6. 陷阱：键类型不一致全丢、默认 inner 丢行、重复键行数爆炸

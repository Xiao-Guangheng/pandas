# -*- coding: utf-8 -*-
# ============================================================
# 第9章：字符串与日期 -- 两大访问器 .str 与 .dt
# ============================================================
# 列类型是字符串时，用 .str 访问器批量操作；
# 列类型是日期时，用 .dt 访问器批量操作。
# 它们的共同特点：像"对整列的每个元素调用对应方法"，返回整列。
#
#   df["姓名"].str.upper()      <- 对每个名字做 upper
#   df["日期"].dt.year          <- 取每个日期的年份
#
# 类比：.str 是"字符串方法的向量化版本"，.dt 是"日期字段的向量化版本"。
# 这两个访问器是数据清洗的绝对主力。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)


# ============================================================
# 9.1 .str 访问器基础：大小写 / 长度 / 去空白
# ============================================================
print("=" * 50)
print("9.1 .str 基础")

names = pd.Series(["  zhangSan ", " liSi ", " wangWu "])

print("转大写:", names.str.upper().tolist())
print("转小写:", names.str.lower().tolist())
print("首字母大写:", names.str.capitalize().tolist())
print("去两端空白 strip:", names.str.strip().tolist())      # 清洗必做！
print("长度 len:", names.str.len().tolist())

# 注意：.str 只对字符串列有效（dtype 是 str/object）。
# 如果列里有数字，先 astype(str) 再 .str。


# ============================================================
# 9.2 判断类：contains / startswith / endswith / isdigit
# ============================================================
print("\n" + "=" * 50)
print("9.2 判断类（返回布尔列，正好接筛选！）")

info = pd.Series(["电话:13800138000", "邮箱:a@x.com", "电话:13911112222", "未知"])

print("包含'电话':", info.str.contains("电话").tolist())
print("以'电话'开头:", info.str.startswith("电话").tolist())

# contains 返回布尔列，直接接布尔筛选（第 4 章）：
print("\n筛出所有电话行:")
print(info[info.str.contains("电话")])

# contains 默认支持正则（regex=True 是默认）：
print("\n正则找手机号:")
print(info[info.str.contains(r"1[0-9]{10}")])

# 其他判断：isdigit / isalpha / isnumeric（对中文数字也有效）
s = pd.Series(["123", "abc", "１２３", "一二三"])
print("\nisdigit:", s.str.isdigit().tolist())      # [T, F, T, F] 全角数字也算
print("isnumeric:", s.str.isnumeric().tolist())    # [T, F, T, T] 中文数字算


# ============================================================
# 9.3 替换与分割：replace / split
# ============================================================
print("\n" + "=" * 50)
print("9.3 replace / split")

s = pd.Series(["张三-男-18", "李四-女-19", "王五-男-20"])

# split 切开 -> 每个元素变成一个"列表"
print("split 后每格是列表:")
print(s.str.split("-").tolist())

# .str.get(i) 取列表的第 i 个（或直接 .str[i]）：
print("\n取第 0 段（姓名）:", s.str.split("-").str[0].tolist())
print("取第 2 段（年龄）:", s.str.split("-").str[2].tolist())

# expand=True 直接炸开成多列（超实用！）：
parts = s.str.split("-", expand=True)
print("\nexpand=True 变成 DataFrame:")
print(parts)
# 配合列名整理，一步把"张三-男-18"拆成三列：
parts.columns = ["姓名", "性别", "年龄"]
print(parts)

# replace：默认也是正则
t = pd.Series(["电话:13800138000", "手机:13911112222"])
print("\n脱敏手机号（正则替换）:")
print(t.str.replace(r"(1[0-9]{2})[0-9]{4}([0-9]{4})", r"\1****\2", regex=True).tolist())

# 拼接整列：cat
print("\n整列拼接:", pd.Series(["a", "b", "c"]).str.cat(sep=", "))


# ============================================================
# 9.4 字符串的切片和索引
# ============================================================
print("\n" + "=" * 50)
print("9.4 字符串切片")

s = pd.Series(["20260101", "20260215", "20260320"])
print("前 4 位（年份）:", s.str[:4].tolist())
print("后 2 位:", s.str[-2:].tolist())
print("切出年月:", s.str[:6].tolist())
# .str[...] 的语法和 Python 字符串切片完全相同，只是作用在整列上。


# ============================================================
# 9.5 .str 的缺失值行为
# ============================================================
print("\n" + "=" * 50)
print("9.5 缺失值与 .str")

s = pd.Series(["abc", None, "def"])
print("长度:", s.str.len().tolist())
# 缺失位置的结果也是缺失（NaN），不会报错。
print("是否含'a':", s.str.contains("a").tolist())
# 判断类遇到缺失也是 NaN（不是 False），筛选时会被条件自动滤掉。
# ⚠️ contains 的 na 参数可以把缺失当作指定的布尔值：
print("na=False 时:", s.str.contains("a", na=False).tolist())


# ============================================================
# 9.6 .dt 访问器：把字符串变成日期
# ============================================================
# 日期处理第一步永远是"变成真正的日期类型"，然后才有 .dt。
# pd.to_datetime() 负责这个转换。

print("\n" + "=" * 50)
print("9.6 to_datetime")

raw = pd.Series(["2026-01-15", "2026/03/20", "2026-06-01"])
# 格式不统一（有 - 有 /）时用 format='mixed' 让它逐个猜：
dt = pd.to_datetime(raw, format="mixed")
print(dt.tolist())

# 常见转换方式：
print(pd.to_datetime("2026-08-24"))                     # 单个字符串
print(pd.to_datetime(pd.Series(["20260101", "20260215"]), format="%Y%m%d").tolist())
# format 参数：明确告诉它日期长什么样（%Y年 %m月 %d日 %H时 %M分 %S秒）
# 格式统一时给 format 速度飞快；不统一时用 format='mixed'。
# 中文日期（"2026年6月1日"）mixed 也认不了，要显式给格式：
cn = pd.Series(["2026年6月1日", "2026年12月25日"])
print(pd.to_datetime(cn, format="%Y年%m月%d日").tolist())

# 转换失败的典型：把"13月32日"这种非法日期喂进去会报错，
# errors='coerce' 可以让失败的变 NaT（时间版的 NaN）：
bad = pd.Series(["2026-01-15", "2026-13-45"])
print(pd.to_datetime(bad, errors="coerce").tolist())


# ============================================================
# 9.7 .dt 取字段：年月日时分秒、星期
# ============================================================
print("\n" + "=" * 50)
print("9.7 .dt 取字段")

dates = pd.Series(pd.date_range("2026-01-01", periods=5, freq="D"))
print("日期列:", dates.tolist())

print("年:", dates.dt.year.tolist())
print("月:", dates.dt.month.tolist())
print("日:", dates.dt.day.tolist())
print("星期几（数字，周一=0）:", dates.dt.dayofweek.tolist())
print("星期几（英文）:", dates.dt.day_name().tolist())
print("一年中第几天:", dates.dt.dayofyear.tolist())
print("该月天数:", dates.dt.days_in_month.tolist())
print("季度:", dates.dt.quarter.tolist())

# 配合 value_counts 统计（分析常规套路）：
print("\n按月统计出现次数:")
sales = pd.Series(pd.to_datetime(["2026-01-05", "2026-01-20", "2026-03-09"]))
print(sales.dt.month.value_counts().sort_index())


# ============================================================
# 9.8 日期的运算：差值与加减
# ============================================================
print("\n" + "=" * 50)
print("9.8 日期运算")

d1 = pd.Series(pd.to_datetime(["2026-01-01", "2026-03-15"]))
d2 = pd.Series(pd.to_datetime(["2026-02-01", "2026-03-20"]))

diff = d2 - d1
print("日期相减:", diff.tolist())
print("天数:", diff.dt.days.tolist())
# 两个日期相减得到 Timedelta（时间差），再用 .dt.days 取天数。

print("\n日期加一段时间:")
print((d1 + pd.Timedelta(days=30)).tolist())
# Timedelta(days=30) 是"30天"这个量；也可用 hours=, weeks= 等。

# 实战例子：注册到现在多少天
reg = pd.to_datetime(pd.Series(["2025-01-01", "2026-08-01"]))
today = pd.Timestamp("2026-08-24")
print("\n注册至今天数:", (today - reg).dt.days.tolist())


# ============================================================
# 9.9 date_range：批量生成日期
# ============================================================
print("\n" + "=" * 50)
print("9.9 date_range")

print("连续 5 天:")
print(pd.date_range("2026-01-01", periods=5, freq="D").tolist())

print("\n每 2 天:")
print(pd.date_range("2026-01-01", periods=3, freq="2D").tolist())

print("\n按小时:")
print(pd.date_range("2026-01-01", periods=3, freq="h").tolist())

print("\n月末:")
print(pd.date_range("2026-01-01", periods=3, freq="ME").tolist())

print("\n每周一:")
print(pd.date_range("2026-01-01", periods=3, freq="W").tolist())

# ⚠️ pandas 3.0 的频率别名已经全面小写化：
#   'D'天 'h'时 'min'分 's'秒 | 'ME'月末 'QE'季末 'YE'年末 | 'W'周
# 老教程的 'H'（时）和 'M'（月）已删除，现在会直接报错。
# （大写 'D'、'W' 仍可用，但新代码统一写小写更保险。）


# ============================================================
# 9.10 实战：清洗一份"脏"日期表
# ============================================================
print("\n" + "=" * 50)
print("9.10 综合实战")

log = pd.DataFrame({
    "账号": ["  ZhangSan ", "LiSi", "  WangWu", "zhangsan "],
    "注册日期": ["2026/01/05", "2026-02-17", "2026.3.9", "2026/01/05"],
})
print("原始脏数据:")
print(log)

clean = log.copy()
# 1) 账号标准化：去空白 + 转小写
clean["账号"] = clean["账号"].str.strip().str.lower()
# 2) 日期标准化：统一格式解析
clean["注册日期"] = pd.to_datetime(clean["注册日期"], format="mixed")
# 3) 去重
clean = clean.drop_duplicates().reset_index(drop=True)
# 4) 加工：月份、注册天数
clean["注册月"] = clean["注册日期"].dt.month
clean["已注册天数"] = (pd.Timestamp("2026-08-24") - clean["注册日期"]).dt.days
print("\n清洗后:")
print(clean)
# 一条链写法（熟练后推荐）：
# clean = (log.assign(账号=lambda d: d["账号"].str.strip().str.lower())
#             .assign(注册日期=lambda d: pd.to_datetime(d["注册日期"], format="mixed"))
#             .drop_duplicates())


# ============================================================
# 本章小结
# ============================================================
# 1. .str 访问器：upper/lower/strip/len/contains/replace/split
# 2. contains 支持正则；na= 参数处理缺失；split(expand=True) 一拆多列
# 3. .str[切片] 语法同 Python 字符串
# 4. 先 to_datetime（给 format 提速、errors='coerce' 容错），再 .dt 取字段
# 5. 日期相减 -> Timedelta，用 .dt.days 取天数；Timedelta(days=30) 做加法
# 6. date_range 的 freq：'D'/'h'/'min'/'ME'/'W'（'H'、'M' 已删除）

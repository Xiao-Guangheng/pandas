# -*- coding: utf-8 -*-
# ============================================================
# 第14章：时间序列 -- 日期当索引，切片/重采样/滑窗
# ============================================================
# 股价、气温、日志、销售额……凡是按时间排列的数据都叫时间序列。
# Pandas 的时间序列三件套：
#   1) 把日期设成索引 -> 像切字符串一样切时间段
#   2) resample 重采样 -> 按天/月/年聚合
#   3) rolling 滑动窗口 -> 移动平均等"平滑"指标
#
# 上一章学的 .dt 和 date_range 是本章的地基。

import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

# 先造一份"每日股价"数据（随机游走模拟）
np.random.seed(42)
dates = pd.date_range("2026-01-01", periods=90, freq="D")   # 90 天
price = 100 + np.random.randn(90).cumsum()                  # 累计扰动
volume = np.random.randint(1000, 5000, 90)                  # 成交量
stock = pd.DataFrame({"收盘": price.round(2), "成交量": volume}, index=dates)
stock.index.name = "日期"
print("模拟股价（前 5 行）:")
print(stock.head())
print("索引类型:", type(stock.index).__name__)


# ============================================================
# 14.1 日期索引的切片：随便切，按年/月/日都行
# ============================================================
print("=" * 50)
print("14.1 部分字符串索引")

# DatetimeIndex 支持"部分字符串"切片——只写到月，就是整月：
print("2026-01 全月（前 3 行）:")
print(stock.loc["2026-01"].head(3))

print("\n2026-02-01 到 2026-02-10:")
print(stock.loc["2026-02-01":"2026-02-10"])
# 日期索引切片是【闭区间】（两端都包含），和普通 loc 一致。

# 单日 -> 会得到一个 Series：
print("\n单独一天 2026-01-15:")
print(stock.loc["2026-01-15"])

# 每年/每月/每天的特征列也可以随时补（第 9 章的 .dt 在索引上也行）：
print("\n按月分组求成交量合计:")
print(stock.groupby(stock.index.month)["成交量"].sum())


# ============================================================
# 14.2 resample：重采样（改时间粒度）
# ============================================================
# 日数据想看"周/月"级别 -> resample 把时间分桶再聚合，
# 用法和 groupby 几乎一样，只是分组的键换成了"时间段"。
# 频率别名（pandas 3.0 全小写）：
#   D 日 | W 周 | ME 月末 | MS 月初 | QE 季末 | YE 年末 | h 时 | min 分

print("\n" + "=" * 50)
print("14.2 resample")

print("周线（每周最后一天的收盘、周成交量合计）:")
weekly = stock.resample("W").agg({"收盘": "last", "成交量": "sum"})
print(weekly.head())

print("\n月线（月末收盘、月内最高、平均成交量）:")
monthly = stock.resample("ME").agg({"收盘": "last", "成交量": "mean"})
print(monthly)

print("\n降频的另一种聚合：每 10 天一个桶，取收盘均价:")
print(stock["收盘"].resample("10D").mean())
# 日 -> 周/月 是"降频聚合"；反过来"升频"（如 D->h）会出缺失，
# 常配合 asfreq() + 插值，进阶话题，了解即可。

# 记公式：resample(频率).聚合() == groupby(时间段).聚合()
# 日均 -> 周均就是 stock['收盘'].resample('W').mean()，一行的事。


# ============================================================
# 14.3 rolling：滑动窗口（移动平均）
# ============================================================
print("\n" + "=" * 50)
print("14.3 rolling")

# 7 日移动平均：从第 7 个点开始，每个点 = 前 7 天的平均
stock["MA7"] = stock["收盘"].rolling(7).mean()
stock["MA30"] = stock["收盘"].rolling(30).mean()
print(stock.head(10)[["收盘", "MA7", "MA30"]])
# 前 6 行 MA7 是 NaN（窗口不满 7 个值，凑不出平均）。

# rolling 常用参数 min_periods：窗口不满也要个值
ma = stock["收盘"].rolling(7, min_periods=1).mean()
print("\nmin_periods=1（不满窗口也硬算）:")
print(ma.head(3))

# 别的统计也行：
print("\n7 日滚动最大值（前 3 个）:")
print(stock["收盘"].rolling(7).max().head(3))

# 应用场景：股价的"金叉/死叉"（短均线上穿/下穿长均线）：
cross = (stock["MA7"] > stock["MA30"])
signal = cross != cross.shift(1)         # 今天和昨天状态不同 = 交叉点
print("\n金叉死叉出现的日期（最多 5 个）:")
print(stock.index[signal][:5])


# ============================================================
# 14.4 shift 与 pct_change：错位比较、算涨跌幅
# ============================================================
print("\n" + "=" * 50)
print("14.4 shift / pct_change")

stock["昨日"] = stock["收盘"].shift(1)          # 整列往下挪一格
print(stock.head()[["收盘", "昨日"]])

# 涨跌幅 = (今天 - 昨天) / 昨天，pct_change 一行搞定：
stock["日涨跌幅"] = stock["收盘"].pct_change()
print("\n日涨跌幅（前 3 个）:")
print(stock["日涨跌幅"].head(3))

# 累计收益（从第一天起翻了多少倍）：
print("\n累计收益（期末/期初）:", round((stock["收盘"].pct_change() + 1).prod() - 1, 4))
# 另一种直白算法：
print("直接相除法:", round(stock["收盘"].iloc[-1] / stock["收盘"].iloc[0] - 1, 4))

# shift(-1) 往上挪 = "看明天"；构造"今天 vs 明天"对照表：
stock["明日"] = stock["收盘"].shift(-1)
print("\n今天 vs 明天（最后两行，明日出现 NaN）:")
print(stock[["收盘", "明日"]].tail(2))


# ============================================================
# 14.5 expanding：不断变大的窗口（累计统计）
# ============================================================
print("\n" + "=" * 50)
print("14.5 expanding")

# rolling 窗口大小固定；expanding 窗口"从开头一直到当前"：
print("累计最大值（前 5 个）:")
print(stock["收盘"].expanding().max().head())

print("\n历史均值（到当前为止的平均，前 3 个）:")
print(stock["收盘"].expanding().mean().head(3))
# rolling 看局部趋势，expanding 看全程累计，注意区分。


# ============================================================
# 14.6 时区与索引整理（了解即可）
# ============================================================
print("\n" + "=" * 50)
print("14.6 时区")

# tz_localize 打时区标签 / tz_convert 换时区（不改变时刻本身）：
idx = pd.date_range("2026-01-01", periods=3, freq="D", tz="Asia/Shanghai")
print(idx)
print(idx.tz_convert("UTC"))

# 时间序列索引排序：真实数据常有乱序/重复时间戳
messy = stock.sample(frac=1, random_state=1)   # 打乱顺序
print("\n乱序索引 is_monotonic_increasing:", messy.index.is_monotonic_increasing)
fixed = messy.sort_index()
print("排序后:", fixed.index.is_monotonic_increasing)
# 时间序列第一件事：sort_index()，否则切片/rolling 结果都不对。


# ============================================================
# 14.7 实战：气温数据分析
# ============================================================
print("\n" + "=" * 50)
print("14.7 综合实战")

# 造一份每小时气温数据（3 天，模拟日夜温差）
hours = pd.date_range("2026-06-01", periods=72, freq="h")
temp = pd.Series(
    25 + 6 * np.sin(np.arange(72) / 24 * 2 * np.pi) + np.random.randn(72),
    index=hours, name="气温",
)

# 1) 只看每天 14:00 的气温（at_time 精确到时刻）
print("每天 14 点的气温:")
print(temp.at_time("14:00"))

# 2) 每天 10:00~16:00 之间的均值（between_time）
print("\n白天时段均值（按天 resample）:")
day = temp.between_time("10:00", "16:00")
print(day.resample("D").mean().round(2))

# 3) 3 小时滑动平均平滑曲线
smooth = temp.rolling(3, min_periods=1).mean()
print("\n原始 vs 平滑（前 5 个）:")
print(pd.DataFrame({"原始": temp, "平滑": smooth}).head())

# 4) 找出每天最高温出现的时刻
# resample 没有 idxmax，换个思路：按天分组后对每组用 idxmax：
daily_max_time = temp.groupby(temp.index.day).apply(lambda s: s.idxmax())
print("\n每日最高温时刻:")
print(daily_max_time)
# idxmax 返回最大值所在的索引（这里索引是时间戳 = 出现时刻）：
print("\n每日最高温数值:")
print(temp.loc[daily_max_time])


# ============================================================
# 本章小结
# ============================================================
# 1. 日期设为索引后：loc["2026-01"]、loc["2026-01-01":"2026-01-15"] 随便切
# 2. resample(频率).聚合()：D/W/ME/QE/YE（pandas 3.0 全小写）
# 3. rolling(n)：移动平均/最值；min_periods=1 消除前缘 NaN
# 4. shift(1) 错位比较；pct_change() 涨跌幅；shift(-1) 看未来
# 5. expanding()：从头到当前的累计窗口
# 6. at_time / between_time 按时刻取数；乱序先 sort_index()
#
# 恭喜！学到这里，pandas 14 章全部完结。
# 建议的下一步：找一份真实 CSV（比如股票、天气、销售数据），
# 把 04 筛选 -> 05 清洗 -> 07 统计 -> 10 分组 -> 12 透视 -> 13 读写
# 串成一条完整流水线，跑一遍就算真正出师了。

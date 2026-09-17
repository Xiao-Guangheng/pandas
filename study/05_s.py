# 处理缺失值
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "语文": [88, np.nan, 76, np.nan, 90],
    "数学": [90, 85, np.nan, 78, np.nan],
    "城市": ["北京", None, "上海", "广州", None],   # 字符串列的缺失
})

print(df.dtypes)
#显示的是：float64，float64，float64，object    
# 可以看到本来传的是整数，因为有 NaN，整数装不下，pandas 自动升级成 float64（NaN 是浮点值）。
# 但是字符串天生支持缺失值，所以城市列的类型是 object。

s_str = pd.Series(["北京", None])
# 存入了一个空值
print(repr(s_str[1]))   # nan
# 但是打印出来是 nan，和数值列的缺失打印一样。
# 这是因为 pandas 3.0 的字符串类型，天生支持缺失值，所以打印出来是 nan。

# 发现缺失

# isna / notna / info
print(df.isna())
# 这个是布尔矩阵，True 表示这个位置缺失，False 表示这个位置不缺失。
# 和 np.isnan 一样是布尔矩阵，但 pd.isna 还认识 None/NA，适用面更广。

df.isna().sum()

df.isna().mean()  # 求平均值，True 记 1，False 记 0，所以就是缺失比例。

# 至少缺失一科的行
df.isna().any(axis=1)
# axis=1 表示沿着列方向数，得到"每行"的结论。

# notna() 是 isna() 的反义词，表示不缺失。

df[df.notna().all(axis=1)]
# 表示检查每一行，只有所有列都不缺失的行才会被保留下来。
df.isna().all(axis=1)
# 表示整行全缺失
df.notna().any(axis=1)
# 表示整行至少有一个不缺失

df.info()
# 整体分析

# 删除缺失值

# dropna

df.dropna()  # 删除所有含有缺失值的行
df.dropna(how="all")  # 删除整行全缺失的行
df.dropna(axis=1)  # 删除所有含有缺失值的列
df.dropna(axis=1, how="all")  # 删除整列全缺失的列
df.dropna(subset=["语文"])  # 删除语文列中含有缺失值的行
df.dropna(thresh=2)  # 保留至少有 2 个非缺失值的行

# 填充缺失 fillna

# 方式 A：填固定值
print("缺失填 0:")
print(df["数学"].fillna(0).tolist())
# 表示把数学列的缺失值填充为 0，返回一个新的 Series。

mean_math = df["数学"].mean()  # 这里mean默认跳过缺失值，计算数学列的平均值
df["数学"].fillna(mean_math).tolist()
# 表示把数学列的缺失值填充为数学列的平均值，

# 不同的列可以填充不同的值
filled = df.fillna({"语文": 60, "数学": df["数学"].mean(), "城市": "未知"})

# 前向/后向填充

s = pd.Series([1, np.nan, np.nan, 4, 5, np.nan, 7])

s.ffill().tolist()  # 前向填充，缺失值用前一个非缺失值填充
s.bfill().tolist()  # 后向填充，缺失值用后一个非缺失值填充

s.ffill(limit=1).tolist()  # limit=1 表示最多填充 1 个缺失值
# 这个值填1后面的那个缺失值

# 插值

# inyerpolate() 方法可以对缺失值进行插值，默认使用线性插值。

s=pd.Series([0.0,np.nan,2.0,np.nan,4.0])

s.interpolate().tolist()  # [0.0, 1.0, 2.0, 3.0, 4.0]，线性插值
# 就是他自己判断出来缺失值应该填什么，但是必须像这样是线性的

# 缺失值的比较陷阱

s =pd.Series([1.0,np.nan,3.0])
print(s>2.0)

print(((s>2)| s.isna()).tolist())
# 这个是表示"大于2或者缺失值"，因为缺失值和任何数比较都是 False，所以要用 isna() 来判断缺失值。


dirty = pd.DataFrame({
    "姓名": ["张三", None, "李四", "王五", "李四"],
    "语文": [88, np.nan, 92, np.nan, 92],
    "数学": [np.nan, 85, np.nan, 78, np.nan],
})

step2= dirty.dropna(subset=["姓名"])

step3 = step2.fillna({"语文": step2["语文"].mean(), "数学": step2["数学"].mean()})
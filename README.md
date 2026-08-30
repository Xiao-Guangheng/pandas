# Pandas 学习笔记

这个文件夹是我学习 **Pandas** 的完整记录：14 章循序渐进的教程笔记，延续 NumPy 的学习方法。

## Pandas 是什么？

如果说 NumPy 解决的是"**数值**怎么算得快"，那 Pandas 解决的是"**表格数据**怎么处理得方便"。

现实中拿到的数据往往是一张表：学生名单有姓名、性别、生日（字符串 + 日期 + 缺失值混杂）、销售记录有订单号、日期、金额。NumPy 的 ndarray 要求所有元素同类型，处理这种"脏脏的"表格很吃力。

Pandas 在 ndarray 之上加了两层东西：

- **索引（Index）**：每一行、每一列都有名字，可以按名字（标签）查找，而不是死记第 0 行第 3 列
- **类型容忍**：每一**列**是一个类型，不同列可以是不同类型，就像真正的 Excel 表

一句话总结：**NumPy 是引擎，Pandas 是装了方向盘和后视镜的整车。** 你在 NumPy 学的布尔筛选、广播、聚合，在 Pandas 里全部能复用，只是换了名字。

## 目录结构

```
pandas/
├── 01_Series对象.py          # 一维带标签数组：创建、索引、与 ndarray 的关系
├── 02_DataFrame对象.py       # 二维表格：创建、head/tail/info/describe
├── 03_索引与选择.py          # [] / loc / iloc / at / iat（全章最重要）
├── 04_布尔筛选与查询.py       # 条件筛选、isin、between、where、query
├── 05_缺失值处理.py          # NaN / None / NA、isna、fillna、dropna、ffill
├── 06_数据增删改.py          # 新增列、insert、drop、rename、assign
├── 07_运算与统计.py          # 统计函数、apply/map/transform、向量化
├── 08_排序与排名.py          # sort_values / sort_index / rank / nlargest
├── 09_字符串与日期.py        # .str 访问器、.dt 访问器、to_datetime
├── 10_分组groupby.py         # 拆分-应用-合并（重中之重）
├── 11_合并拼接.py            # merge / concat / join（类比 SQL 的 JOIN）
├── 12_透视表.py              # pivot / pivot_table / melt（宽表⇄长表）
├── 13_文件读写.py            # read_csv / to_csv / read_excel / to_excel
├── 14_时间序列.py            # 日期索引、resample、rolling 滚动窗口
└── output/                   # 练习产生的数据文件
```

## 学习方法

每章的流程是：

1. **阅读正文章节**（`01` ~ `14`），里面带有大量注释和打印输出
2. **合上教程，自己凭记忆写一遍**，报错的地方就是没真懂的地方
3. **遇到不确定的 API，写两行代码跑一下**，比查十篇博客都管用

## 重要：本笔记基于 pandas 3.0

网上大量教程是 pandas 1.x / 2.x 时代的，有几个地方**已经过时**，本笔记全部按 3.0 的实际行为写：

| 老教程写法 | pandas 3.0 现状 |
|---|---|
| `s[0]`（按位置取值） | ❌ 已删除。标签索引的 Series 传整数会直接 KeyError，必须用 `s.iloc[0]` |
| `fillna(method='ffill')` | ❌ 已删除。直接用 `s.ffill()` / `s.bfill()` |
| `freq='H'` / `freq='M'` | ❌ 已删除。用小写 `'h'`、`'min'`，月末是 `'ME'`，年末是 `'YE'` |
| `df.applymap(f)` | ❌ 已删除。用 `df.map(f)` |
| 字符串列 dtype 是 `object` | 现在是专门的 `str` dtype，更快且支持缺失值 |
| 链式赋值"有时能成功" | 写时复制（CoW）成为默认，链式赋值**永远无效**并警告 |
| `inplace=True` 万能 | 仍可用但不再推荐，官方建议用赋值写法 `df = df.drop(...)` |

## 和 NumPy 的对照表（迁移你的知识）

| 你在 NumPy 学的 | Pandas 对应写法 |
|---|---|
| `arr[arr > 5]` | `df[df['分数'] > 5]` |
| `np.sum(arr, axis=0)` | `df.sum()`（默认跳过缺失值） |
| `np.where(cond, a, b)` | `s.where(cond, b)` |
| `arr.reshape` | `df.pivot`（更长见的使用场景是表格变换） |
| `np.isnan(arr)` | `pd.isna(df)`（还能认出 None、NA） |
| `arr.mean()` | `df['列'].mean()` |
| 花式索引 `arr[[1,3]]` | `df.iloc[[1, 3]]` / `df.loc[[标签, 标签]]` |

## 学完之后的检验项目

用一份虚构的成绩单 CSV 完成：读入 → 清洗缺失值 → 计算总分排名 → 分组统计各班平均分 → 排序导出。能独立完成，就说明这 14 章真的掌握了。

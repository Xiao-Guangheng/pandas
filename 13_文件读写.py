# -*- coding: utf-8 -*-
# ============================================================
# 第13章：文件读写 -- 让数据和代码连起来
# ============================================================
# 前面所有章节的数据都是代码里现写的，真实世界的数据在文件里：
# CSV、Excel、数据库……本章解决"读进来"和"存出去"。
#
# 核心函数就两个：
#   pd.read_csv / df.to_csv
#   pd.read_excel / df.to_excel
# 参数众多但常用的就那几个，本章按"最常用 -> 进阶"顺序展开。
#
# 本章会生成文件到 output/ 子文件夹（模仿 numpy 的习惯）。

import os
import pandas as pd
import numpy as np

pd.set_option("display.unicode.east_asian_width", True)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)      # output 文件夹不存在就创建


# ============================================================
# 13.1 to_csv：先把示例数据存出去
# ============================================================
print("=" * 50)
print("13.1 to_csv")

df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "班级": ["一班", "一班", "二班", "二班"],
    "语文": [88, 92, 76, 85],
    "数学": [90, 85, 95, 78],
})

csv_path = os.path.join(OUT, "students.csv")
df.to_csv(csv_path, index=False)     # index=False：行号不写入文件！
print("已保存:", csv_path)

# index=False 是最重要的参数：不加的话文件里会多一列 0,1,2,...，
# 读回来就多一个 Unnamed 列（新手最常见的困惑之一）。

# 看一眼文件内容（编码 utf-8-sig 让 Excel 打开不乱码）：
df.to_csv(os.path.join(OUT, "students_excel.csv"),
          index=False, encoding="utf-8-sig")
# 中文 Windows 的 Excel 用 ANSI/GBK 打开 CSV，utf-8-sig 带 BOM 头，
# Excel 才能正确识别 UTF-8。要给同事传 CSV 就用它。


# ============================================================
# 13.2 read_csv：读回来
# ============================================================
print("\n" + "=" * 50)
print("13.2 read_csv")

read_back = pd.read_csv(csv_path)
print(read_back)
print("\n列名:", read_back.columns.tolist())

# 常用参数速查（按出场频率排序）：
demo = pd.read_csv(
    csv_path,
    # encoding="utf-8-sig",     # 文件是什么编码就写什么（乱码时先想它）
    # index_col="姓名",          # 把某列当行索引
    # usecols=["姓名", "语文"],   # 只读需要的列（大文件提速）
    # nrows=100,                 # 只读前 100 行（先探探底）
    # header=0,                  # 第几行是列名（默认 0）
)
print(demo.shape)


# ============================================================
# 13.3 读 Excel：read_excel / to_excel
# ============================================================
print("\n" + "=" * 50)
print("13.3 Excel 读写")

# 需要 openpyxl 库（pip install openpyxl），你已经装好了。
xlsx_path = os.path.join(OUT, "students.xlsx")
df.to_excel(xlsx_path, index=False, sheet_name="成绩")

back = pd.read_excel(xlsx_path, sheet_name="成绩")   # 不写 sheet_name 默认第一个
print(back)

# 多个表写进同一个 Excel 文件（sheet 一张一张追加）：
xlsx2 = os.path.join(OUT, "multi.xlsx")
with pd.ExcelWriter(xlsx2) as writer:
    df.to_excel(writer, sheet_name="成绩", index=False)
    df.describe().to_excel(writer, sheet_name="统计", index=True)
print("\nExcel 的 sheet 列表:", pd.ExcelFile(xlsx2).sheet_names)

# 小知识：xlsx 是压缩格式，读写都比 CSV 慢，还保留格式；
# 数据交换优先 CSV，要给人看/带格式才用 Excel。


# ============================================================
# 13.4 读取时的常见坑
# ============================================================
print("\n" + "=" * 50)
print("13.4 常见坑与对策")

# 坑1：数字列被读成字符串（列里混了 "88" 和 "未知"）
tricky_path = os.path.join(OUT, "tricky.csv")
pd.DataFrame({"分数": ["88", "92", "未知"]}).to_csv(tricky_path, index=False)
t = pd.read_csv(tricky_path)
print("混入文字后的 dtype:", t["分数"].dtype)     # str
print("转数值（errors='coerce' 把文字变 NaN）:")
print(pd.to_numeric(t["分数"], errors="coerce").tolist())

# 坑2：缺失值其实是特殊字符串（"-"、""、"NA"）
na_path = os.path.join(OUT, "na.csv")
pd.DataFrame({"值": ["10", "-", "30", ""]}).to_csv(na_path, index=False)
n1 = pd.read_csv(na_path)
print("\n不告诉 pandas 时 - 被当成普通字符串:", n1["值"].tolist())
n2 = pd.read_csv(na_path, na_values=["-"])
print("na_values=['-'] 后:", n2["值"].tolist())
# read_csv 的 na_values 参数：这些值一律视为缺失。

# 坑3：日期列读进来是字符串
date_path = os.path.join(OUT, "dates.csv")
pd.DataFrame({"日期": ["2026-01-01", "2026-02-01"]}).to_csv(date_path, index=False)
d1 = pd.read_csv(date_path)
print("\n默认读法 dtype:", d1["日期"].dtype)
d2 = pd.read_csv(date_path, parse_dates=["日期"])   # 读的时候直接转
print("parse_dates 后 dtype:", d2["日期"].dtype)

# 坑4：大文件 -- 用 chunksize 分块读，一块一块处理：
total = 0
for chunk in pd.read_csv(csv_path, chunksize=2):    # 每次只读 2 行（演示）
    total += len(chunk)
print("\nchunksize 分块累计行数:", total)
# 百万行的日志文件：chunksize=100000，逐块过滤/聚合，内存不爆。


# ============================================================
# 13.5 其他格式一览（知道有这些就好）
# ============================================================
print("\n" + "=" * 50)
print("13.5 其他格式")

# JSON（网页/接口常见）：
json_path = os.path.join(OUT, "students.json")
df.to_json(json_path, orient="records", force_ascii=False)
print(pd.read_json(json_path))

# NumPy 的 npy/npz（你在 NumPy 第 11 章学过的，无缝衔接）：
np_path = os.path.join(OUT, "array.npy")
np.save(np_path, df[["语文", "数学"]].to_numpy())
print("\nnpy 读回来的 shape:", np.load(np_path).shape)

# 剪贴板（从 Excel 复制一块直接读，调试神器）：
# pd.read_clipboard()   # 复制表格后运行这行
# df.to_clipboard()     # 直接粘到 Excel

# 数据库（SQL）：需要 sqlalchemy
# import sqlalchemy; engine = sqlalchemy.create_engine("sqlite:///xx.db")
# pd.read_sql("SELECT * FROM students", engine)
# df.to_sql("students", engine, if_exists="replace")


# ============================================================
# 13.6 实战：完整的"读-算-存"流水线
# ============================================================
print("\n" + "=" * 50)
print("13.6 综合实战")

# 模拟收到一份"原始成绩.csv"，完成：读入->清洗->统计->导出
raw_path = os.path.join(OUT, "raw_scores.csv")
pd.DataFrame({
    "学号": ["S001", "S002", "S003", "S004", "S005"],
    "姓名": ["张三", "李四", "", "赵六", "钱七"],
    "班级": ["一班", "一班", "二班", "二班", "二班"],
    "语文": [88, "", 76, 85, 90],
    "数学": [90, 85, 95, "", 92],
}).to_csv(raw_path, index=False)

# 1) 读入（空字符串自动识别为 NaN）
raw = pd.read_csv(raw_path)
print("读入:")
print(raw)

# 2) 清洗：删掉姓名缺失的行；分数填 0（当作缺考）
clean = raw.dropna(subset=["姓名"]).fillna({"语文": 0, "数学": 0})
clean["语文"] = clean["语文"].astype(int)
clean["数学"] = clean["数学"].astype(int)

# 3) 统计：加总分、排名
clean["总分"] = clean["语文"] + clean["数学"]
clean = clean.sort_values("总分", ascending=False).reset_index(drop=True)

# 4) 导出（utf-8-sig，Excel 打开不乱码）
result_path = os.path.join(OUT, "result.csv")
clean.to_csv(result_path, index=False, encoding="utf-8-sig")
print("\n清洗统计后:")
print(clean)
print("\n已导出:", result_path)


# ============================================================
# 本章小结
# ============================================================
# 1. to_csv/read_csv 是主力；index=False 存 CSV（读回没有幽灵列）
# 2. 中文给 Excel 用：encoding="utf-8-sig"
# 3. read_csv 常用参数：usecols/nrows/index_col/na_values/parse_dates/chunksize
# 4. Excel：read_excel/to_excel，多 sheet 用 ExcelWriter，需 openpyxl
# 5. 数字列变字符串 -> pd.to_numeric(errors='coerce')
# 6. 大文件 chunksize 分块；JSON/npy/sql/剪贴板知道入口即可
#
# output/ 文件夹里现在有本章生成的所有文件，可以打开对照看看。

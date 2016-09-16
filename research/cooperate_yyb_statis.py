import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection
import pandas as pd
import numpy as np

# --------------------------------------------------
# 描述：统计营业部之间的协同关系
# --------------------------------------------------


# 统计item内容，计算总同榜次数和不同场景同榜次数
def statis(x):

    # 传入为空则直接返回空
    if x == "":
        return ""

    # 统计各场景次数
    item_list = x.split("@")
    total_count = 0                   # 总的同上榜次数
    co_buy_count = 0                  # 同买次数
    co_sell_count = 0                 # 同卖次数
    buy_sell_count = 0                # 对手盘，1买2卖
    sell_buy_count = 0                # 对手盘，1卖2买

    for item in item_list:

        if item == "":
            continue

        total_count += 1
        if item == "00":
            co_buy_count += 1
        elif item == "01":
            buy_sell_count += 1
        elif item == "10":
            sell_buy_count += 1
        elif item == "11":
            co_sell_count += 1
        else:
            print("宜昌item：" + item)

    return [total_count, co_buy_count, buy_sell_count, sell_buy_count, co_sell_count]


# 获取数据库连接
con = get_db_connection()

# 获取明细表中所有数据
df = sql.read_sql("select * from lhb_detail_dfcf where lhb_date >= '2014-09-02' and lhb_date <= '2016-09-02'",  con)

# 某些挖回来的数据中，营业部名字列需要进一步处理，包括：
# 1、营业部名字最后有的缺失了“部”字
# 2、营业部年代不同，名字中包含了“有限”，“股份”，“责任”，“公司”等关键字，实际上是一样的
df['yyb_name'] = df['yyb_name'].map(lambda x: x + u"部" if x.endswith(u"营业") else x)
df['yyb_name'] = df['yyb_name'].map(lambda x:
                                    x.replace("股份", "").replace("有限", "").replace("责任", "").replace("公司", ""))

# 对于同一天内完全相同的记录去重（由于不同原因上榜，但明细完全一样）
df = df.drop_duplicates(['lhb_date', 'stock_id', 'yyb_name', 'buy_or_sell', 'buy_or_sell_order'])

# ！！！ 去除机构专用数据，因为名字一样，容易混乱
df = df[df['yyb_name'] != "机构专用"]

# 获取唯一的营业部名称列表
yyb_name_list = list(np.unique(df['yyb_name']))

# 按照日期，股票，原因进行分组
item_group = df.groupby(['stock_id', 'lhb_date', 'reason'])

# 初始化返回结果，这里采用空间换时间策略
df_ret = pd.DataFrame(data="", index=yyb_name_list, columns=yyb_name_list, dtype=np.object_)

# 对每一个分组元素，更新统计结果
for (stock_id, lhb_date, reason), item in item_group:

    print('当前处理[{0}]日[{1}]股票，上榜原因:{2}'.format(lhb_date, stock_id, reason))

    # ii_index, jj_index 代表索引的索引，总是0~n，n代表当前有多少条记录
    index_len = len(item.index)
    for ii_index in range(index_len):
        jj_index = ii_index + 1
        while jj_index < index_len:

            # ii_df, jj_df 代表真实的索引值，用以获取数据
            ii = item.index[ii_index]
            jj = item.index[jj_index]

            # 获取营业部名字
            yyb_name_ii = item.ix[ii, 'yyb_name']
            yyb_name_jj = item.ix[jj, 'yyb_name']

            # 获取已有统计结果，并添加最新值
            # prev_result = df_ret.ix[yyb_name_ii, yyb_name_jj]
            # prev_result += "@{0}{1}".format(item.ix[ii, 'buy_or_sell'], item.ix[jj, 'buy_or_sell'])
            df_ret.ix[yyb_name_ii, yyb_name_jj] += "@{0}{1}".format(item.ix[ii, 'buy_or_sell'],
                                                                    item.ix[jj, 'buy_or_sell'])

            jj_index += 1

# 计算统计值
df_ret = df_ret.applymap(statis)
yyb_num = len(df_ret.index)

# 对结果进行加工，转存为空间更合理的结构
df_final = pd.DataFrame(columns=['yyb_pair',
                                 'total',
                                 'co_buy',
                                 'buy_sell',
                                 'sell_buy',
                                 'co_sell'],
                        index=range(yyb_num*yyb_num))

# 遍历中间结果，提取有效数据，添加到新的返回值中
index = 0
for index_name, row in df_ret.iterrows():
    for col_name in df_ret.columns:
        item_value = row[col_name]
        if item_value == "":
            continue
        row_value = ["{0}-{1}".format(index_name, col_name),
                     int(item_value[0]),
                     int(item_value[1]),
                     int(item_value[2]),
                     int(item_value[3]),
                     int(item_value[4])]
        df_final.ix[index] = pd.Series(row_value, index=df_final.columns)

        index += 1

# 取同榜次数大于1的数据
df_final = df_final[df_final.total > 1]
df_final = df_final.sort_values(by='total', ascending=False)

df_final.to_csv("data/cooperate_yyb.csv")



























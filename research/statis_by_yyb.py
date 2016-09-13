import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection

# --------------------------------------------------
# 描述：统计各个营业部每年度上榜次数，找寻活跃营业部
# --------------------------------------------------


# 统计2016年上榜次数
def date_aggregate_2016(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2016-01-01' <= item <= '2016-12-31']
    return len(arr_str)


# 统计2015年上榜次数
def date_aggregate_2015(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2015-01-01' <= item <= '2015-12-31']
    return len(arr_str)


# 统计2014年上榜次数
def date_aggregate_2014(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2014-01-01' <= item <= '2014-12-31']
    return len(arr_str)


# 统计2013年上榜次数
def date_aggregate_2013(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2013-01-01' <= item <= '2013-12-31']
    return len(arr_str)


# 统计2012年上榜次数
def date_aggregate_2012(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2012-01-01' <= item <= '2012-12-31']
    return len(arr_str)


# 统计2011年上榜次数
def date_aggregate_2011(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2011-01-01' <= item <= '2011-12-31']
    return len(arr_str)


# 统计2010年上榜次数
def date_aggregate_2010(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2010-01-01' <= item <= '2010-12-31']
    return len(arr_str)


# 统计2009年上榜次数
def date_aggregate_2009(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2009-01-01' <= item <= '2009-12-31']
    return len(arr_str)


# 统计2008年上榜次数
def date_aggregate_2008(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2008-01-01' <= item <= '2008-12-31']
    return len(arr_str)


# 统计2007年上榜次数
def date_aggregate_2007(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2007-01-01' <= item <= '2007-12-31']
    return len(arr_str)


# 统计2006年上榜次数
def date_aggregate_2006(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2006-01-01' <= item <= '2006-12-31']
    return len(arr_str)


# 统计2005年上榜次数
def date_aggregate_2005(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2005-01-01' <= item <= '2005-12-31']
    return len(arr_str)


# 统计2004年上榜次数
def date_aggregate_2004(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    arr_str = [item for item in arr_str.values if '2004-01-01' <= item <= '2004-12-31']
    return len(arr_str)

# --------------------------------------------------------------------------------------

# 获取数据库连接
con = get_db_connection()

# 获取明细表数据（年代不同，营业部名字有变化，而且太早以前的数据参考性不强）
df = sql.read_sql("select * from lhb_detail_dfcf where lhb_date >= '2015-09-15'",  con)
# df = sql.read_sql("select * from lhb_detail_dfcf",  con)

# 某些挖回来的数据中，营业部名字列需要进一步处理，包括：
# 1、营业部名字最后有的缺失了“部”字
# 2、营业部年代不同，名字中包含了“有限”，“股份”，“责任”，“公司”等关键字，实际上是一样的
# df['yyb_name'] = df['yyb_name'].map(lambda x: x + u"部" if x.endswith(u"营业") else x)
# df['yyb_name'] = df['yyb_name'].map(lambda x:
#                                     x.replace("股份", "").replace("有限", "").replace("责任", "").replace("公司", ""))


# 对于同一天内完全相同的记录去重（由于不同原因上榜，但明细完全一样）
# df = df.drop_duplicates(['lhb_date', 'stock_id', 'yyb_name', 'buy_or_sell', 'buy_or_sell_order'])

# 根据yyb_name进行分组
yyb_group = df['lhb_date'].groupby(df['yyb_name'])
yyb_df = yyb_group.agg([('total', 'count'),
                        ('first_date', 'min'),
                        ('2004',date_aggregate_2004),
                        ('2005',date_aggregate_2005),
                        ('2006',date_aggregate_2006),
                        ('2007',date_aggregate_2007),
                        ('2008',date_aggregate_2008),
                        ('2009',date_aggregate_2009),
                        ('2010',date_aggregate_2010),
                        ('2011',date_aggregate_2011),
                        ('2012',date_aggregate_2012),
                        ('2013',date_aggregate_2013),
                        ('2014',date_aggregate_2014),
                        ('2015',date_aggregate_2015),
                        ('2016',date_aggregate_2016),
                        ('last_date', 'max')])

yyb_df.to_csv('data/yyb_group.csv')


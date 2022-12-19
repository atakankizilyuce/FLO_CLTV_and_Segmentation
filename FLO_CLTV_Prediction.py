##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# GÖREV 1: Veriyi Hazırlama
###############################################################


import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment = None

# 1. OmniChannel.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df_ = pd.read_csv("crm_analitigi/flo_project/flo_data_20k.csv")
df = df_.copy()

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit,0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit,0)


columns = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline","customer_value_total_ever_online"]
for col in columns:
    replace_with_thresholds(df, col)


df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)

###############################################################
# GÖREV 2: CLTV Veri Yapısının Oluşturulması
###############################################################

df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)


cltv_df = pd.DataFrame()
cltv_df["customer_id"] = df["master_id"]
cltv_df["recency_cltv_weekly"] = ((df["last_order_date"]- df["first_order_date"]).astype('timedelta64[D]')) / 7
cltv_df["T_weekly"] = ((analysis_date - df["first_order_date"]).astype('timedelta64[D]'))/7
cltv_df["frequency"] = df["order_num_total"]
cltv_df["monetary_cltv_avg"] = df["customer_value_total"] / df["order_num_total"]

cltv_df.head()

###############################################################
# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, 6 aylık CLTV'nin hesaplanması
###############################################################

bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T_weekly'])

cltv_df["exp_sales_3_month"] = bgf.predict(4*3,
                                       cltv_df['frequency'],
                                       cltv_df['recency_cltv_weekly'],
                                       cltv_df['T_weekly'])

cltv_df["exp_sales_6_month"] = bgf.predict(4*6,
                                       cltv_df['frequency'],
                                       cltv_df['recency_cltv_weekly'],
                                       cltv_df['T_weekly'])

cltv_df.sort_values("exp_sales_3_month",ascending=False)[:10]

cltv_df.sort_values("exp_sales_6_month",ascending=False)[:10]

ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])
cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                cltv_df['monetary_cltv_avg'])
cltv_df.head()

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency_cltv_weekly'],
                                   cltv_df['T_weekly'],
                                   cltv_df['monetary_cltv_avg'],
                                   time=6,
                                   freq="W",
                                   discount_rate=0.01)
cltv_df["cltv"] = cltv

cltv_df.sort_values("cltv",ascending=False)[:20]

###############################################################
# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
###############################################################

# 1. 6 aylık standartlaştırılmış CLTV'ye göre tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz.
# cltv_segment ismi ile atayınız.
cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])
cltv_df.head()

###############################################################
# Tüm sürecin fonksiyonlaştırılması
###############################################################

def create_cltv_df(dataframe):

    # Veriyi Hazırlama
    columns = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline","customer_value_total_ever_online"]
    for col in columns:
        replace_with_thresholds(dataframe, col)

    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    dataframe = dataframe[~(dataframe["customer_value_total"] == 0) | (dataframe["order_num_total"] == 0)]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # CLTV veri yapısının oluşturulması
    dataframe["last_order_date"].max()  # 2021-05-30
    analysis_date = dt.datetime(2021, 6, 1)
    cltv_df = pd.DataFrame()
    cltv_df["customer_id"] = dataframe["master_id"]
    cltv_df["recency_cltv_weekly"] = ((dataframe["last_order_date"] - dataframe["first_order_date"]).astype('timedelta64[D]')) / 7
    cltv_df["T_weekly"] = ((analysis_date - dataframe["first_order_date"]).astype('timedelta64[D]')) / 7
    cltv_df["frequency"] = dataframe["order_num_total"]
    cltv_df["monetary_cltv_avg"] = dataframe["customer_value_total"] / dataframe["order_num_total"]
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]

    # BG-NBD Modelinin Kurulması
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency_cltv_weekly'],
            cltv_df['T_weekly'])
    cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency_cltv_weekly'],
                                               cltv_df['T_weekly'])
    cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6,
                                               cltv_df['frequency'],
                                               cltv_df['recency_cltv_weekly'],
                                               cltv_df['T_weekly'])

    # # Gamma-Gamma Modelinin Kurulması
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])
    cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                           cltv_df['monetary_cltv_avg'])

    # Cltv tahmini
    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency_cltv_weekly'],
                                       cltv_df['T_weekly'],
                                       cltv_df['monetary_cltv_avg'],
                                       time=6,
                                       freq="W",
                                       discount_rate=0.01)
    cltv_df["cltv"] = cltv

    # CLTV segment
    cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_df

cltv_df = create_cltv_df(df)


cltv_df.head(10)



# Libraries
import pandas as pd
import datetime as dt
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x:"%.2f" % x)
pd.set_option("display.width", 1000)

# Read Data
df_ = pd.read_csv("crm_analitigi/flo_project/flo_data_20k.csv")
df = df_.copy()
df.head()
df["order_channel"].value_counts()
df["last_order_channel"].value_counts()

df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
df.head()

date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

df.groupby("order_channel").agg({"master_id": "count",
                                 "order_num_total": "sum",
                                 "customer_value_total": "sum"})

df.sort_values("customer_value_total", ascending=False)[:10]

df.sort_values("order_num_total", ascending=False)[:10]

def data_pred(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[dataframe].apply(pd.to_datetime)
    return df

# RFM Metrics

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasının analizini yapınız
df["last_order_date"].max()
# 2021-05-30
analysis_date = dt.datetime(2021, 6, 1)

# customer_id, recency, frequency ve monetary değerlerinin yer aldığı yeni bir rfm dataframe'i oluşturunuz
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype("timedelta64[D]")
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]
rfm.head()

# RF ve RFM Skorlarının hesaplanması
# Recency, Frequency, Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve bu skorların kayıt edilmesi
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
rfm.head()

# recency_score ve frequency_scoru'un tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi
rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
rfm.head()

# recency_score ve frequency_score ve monetary_score'un tek bir değişken olarak ifade edilmesi
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str) + rfm["monetary_score"].astype(str))
rfm.head()

# RF_SCORE'u segmentlere çevirme
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)
rfm.head()

# Görev 5
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

target_segments_customer_ids = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_musteri_id.csv", index=False)
cust_ids.shape
rfm.head()

target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose", "at_Risk", "hibernating", "new_customer"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK")) | (df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

def create_rfm(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    #RF ve RFM skorlari
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
    rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str) + rfm["monetary_score"].astype(str))

    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency", "frequency", "monetary", "RF_SCORE", "RFM_SCORE", "segment"]]

rfm_df = create_rfm(df)


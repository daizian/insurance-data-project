import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import time

# 配置页面
st.set_page_config(
    page_title="保险理赔分析平台",
    layout="wide",
    page_icon="🛡️"
)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("data/insurance_claims.csv", parse_dates=["claim_datetime"])
    return df

df = load_data()

# 侧边栏过滤器
st.sidebar.header("🔍 筛选条件")
selected_type = st.sidebar.multiselect(
    "保险类型",
    options=df["policy_type"].unique(),
    default=df["policy_type"].unique()
)

time_range = st.sidebar.slider(
    "报案时间范围",
    min_value=time(0,0),
    max_value=time(23,59),
    value=(time(8,0), time(20,0))
)

# 数据处理
filtered_df = df[
    (df["policy_type"].isin(selected_type)) &
    (pd.to_datetime(df["claim_time"]).dt.time.between(*time_range))
]

# 主界面
st.title("📊 保险理赔智能分析平台")
st.markdown("""
*基于真实业务场景模拟数据开发*  
*数据量：{:,} 条记录 | 欺诈比例：{:.1f}%*  
""".format(len(df), df["is_fraud"].mean()*100))

# 关键指标卡片
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总理赔金额", f"¥{filtered_df['claim_amount'].sum():,.2f}")
with col2:
    st.metric("平均理赔额", f"¥{filtered_df['claim_amount'].mean():,.2f}")
with col3:
    st.metric("欺诈案件", f"{filtered_df['is_fraud'].sum()} 件")

# 可视化图表
tab1, tab2, tab3 = st.tabs(["金额分析", "时间分布", "欺诈检测"])

with tab1:
    fig1 = px.box(
        filtered_df,
        x="policy_type",
        y="claim_amount",
        color="customer_gender",
        title="各险种理赔金额分布"
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.histogram(
        filtered_df,
        x="claim_time",
        color="policy_type",
        title="报案时间分布",
        nbins=24
    )
    fig2.update_xaxes(title="小时")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.scatter(
        filtered_df,
        x="customer_age",
        y="claim_amount",
        color="is_fraud",
        size="claim_amount",
        hover_data=["policy_id"],
        title="年龄-金额-欺诈关系"
    )
    st.plotly_chart(fig3, use_container_width=True)

# 原始数据展示
if st.checkbox("显示原始数据"):
    st.dataframe(filtered_df, height=300)
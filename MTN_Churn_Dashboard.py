import streamlit as st
import pandas as pd
import plotly.express as px

with open(r"Streamlit\MTN_Style.css", "r") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

st.set_page_config(page_title="MTN Customer Churn Analysis",
                   initial_sidebar_state="collapsed",
                   page_icon=":bar_chart:",
                   layout="wide")
st.markdown('<style>div.block-container{padding-top:1.8rem;}</style>', unsafe_allow_html=True)


@st.cache_data
def read_data():
    data = pd.read_csv(r"c:\Users\USER\Documents\CODES\MTN\new_mtn.csv")
    return data


# start = time.time()
data = read_data()
# st.write(time.time()-start)


# Dashboard

# Sidebar
st.sidebar.header('MTN Customer Churn Analysis')
churn = st.sidebar.multiselect("**Churn Status:**", data["Customer Churn Status"].unique())
if not churn:
    df1 = data.copy()
else:
    df1 = data[data["Customer Churn Status"].isin(churn)]

gender = st.sidebar.multiselect("**Choose Gender**:", df1["Gender"].unique())
if not gender:
    df2 = df1.copy()
else:
    df2 = df1[df1["Gender"].isin(gender)]

month = st.sidebar.multiselect("**Select Month(s):**", df2["Month"].unique())
if not month:
    df3 = df2.copy()
else:
    df3 = df2[df2["Month"].isin(month)]

state = st.sidebar.multiselect("**Choose State(s):**", df3["State"].unique())
if not state:
    df4 = df3.copy()
else:
    df4 = df3[df3["State"].isin(state)]

age_group = st.sidebar.multiselect("**Select Age Groups:**", df4["Age_group"].unique())
if not age_group:
    df5 = df4.copy()
else:
    df5 = df4[df4["Age_group"].isin(age_group)]

reason = st.sidebar.multiselect("**Reason(s) for Churn:**", df5["Reasons for Churn"].unique())
if not reason:
    df6 = df5.copy()
else:
    df6 = df5[df5["Reasons for Churn"].isin(reason)]

# Filtering the Dataframes
# individual widgets
if not churn and not gender and not month and not state and not age_group and not reason:
    filtered_df = data
elif not gender and not month and not state and not age_group and not reason:
    filtered_df = data[data["Customer Churn Status"].isin(churn)]
elif not churn and not month and not state and not age_group and not reason:
    filtered_df = data[data["Gender"].isin(gender)]
elif not churn and not gender and not state and not age_group and not reason:
    filtered_df = data[data["Month"].isin(month)]
elif not churn and not gender and not month and not age_group and not reason:
    filtered_df = data[data["State"].isin(state)]
elif not churn and not gender and not month and not state and not reason:
    filtered_df = data[data["Age_group"].isin(age_group)]
elif not churn and not gender and not month and not state and not age_group:
    filtered_df = data[data["Reasons for Churn"].isin(reason)]
# leading widget: churn
elif churn and gender:
    filtered_df = df5[data["Customer Churn Status"].isin(churn) & df5["Gender"].isin(gender)]
elif churn and state:
    filtered_df = df5[data["Customer Churn Status"].isin(churn) & df5["Month"].isin(month)]
elif churn and state:
    filtered_df = df5[data["Customer Churn Status"].isin(churn) & df5["State"].isin(state)]
elif churn and age_group:
    filtered_df = df5[data["Customer Churn Status"].isin(churn) & df5["Age_group"].isin(age_group)]
elif churn and reason:
    filtered_df = df5[data["Customer Churn Status"].isin(churn) & df5["Reasons for Churn"].isin(reason)]
# leading widget: gender
elif gender and month:
    filtered_df = df5[data["Gender"].isin(gender) & df5["Month"].isin(month)]
elif gender and state:
    filtered_df = df5[data["Gender"].isin(gender) & df5["State"].isin(state)]
elif gender and age_group:
    filtered_df = df5[data["Gender"].isin(gender) & df5["Age_group"].isin(age_group)]
elif gender and reason:
    filtered_df = df5[data["Gender"].isin(gender) & df5["Reasons for Churn"].isin(reason)]
# leading widget: month
elif month and state:
    filtered_df = df5[data["Month"].isin(month) & df5["State"].isin(state)]
elif month and age_group:
    filtered_df = df5[data["Month"].isin(month) & df5["Age_group"].isin(age_group)]
elif month and reason:
    filtered_df = df5[data["Month"].isin(month) & df5["Reasons for Churn"].isin(reason)]
# leading widget: state
elif state and age_group:
    filtered_df = df5[data["State"].isin(state) & df5["Age_group"].isin(age_group)]
elif gender and reason:
    filtered_df = df5[data["State"].isin(state) & df5["Reasons for Churn"].isin(reason)]
# leading widget: state
elif age_group and reason:
    filtered_df = df5[data["Age_group"].isin(age_group) & df5["Reasons for Churn"].isin(reason)]
# agregation of all widgets
else:
    filtered_df = df5[(df5["Customer Churn Status"].isin(churn)) & (df5["Gender"].isin(gender)) & (df5["Month"].isin(month)) & (df5["State"].isin(state)) & (df5["Age_group"].isin(age_group)) & (df5["Reasons for Churn"].isin(reason))]

# Data Analysis

# Currency & Unit format functions
def format_currency(x):
    return f"₦{x:,.2f}"

def approx_val(x):
    if abs(x) >= 1000000000:
        return f"₦{(x/1000000000).round(0).astype(int)}B"
    elif abs(x) >= 1000000:
        return f"₦{(x/1000000).round(0).astype(int)}M"
    else:
        return f"₦{x:,.2f}"

# Metrics

# Total Revenue
# metric value
tot_rev = approx_val(filtered_df['Total Revenue'].sum())
# metric delta
tot_rev_rate = ((1-(filtered_df['Total Revenue'].sum()/(data['Total Revenue'].sum())))*100).round(1)
if tot_rev_rate == 0:
    rev_rate = "Normal"
else:
    rev_rate = "-"+f"{tot_rev_rate}%"

# Avg Revenue
# metric value
avg_rev = approx_val(filtered_df['Total Revenue'].mean())
# metric delta
avg_rev_rate = ((1-(filtered_df['Total Revenue'].mean()/(data['Total Revenue'].mean())))*100).round(1)
if avg_rev_rate == 0:
    avg_rate = "Normal"
elif avg_rev_rate <= -0:
    avg_rate = f"{-(avg_rev_rate)}%"
else:
    avg_rate = "-"+f"{avg_rev_rate}%"

# Total Customer Transactions
tot_cust = filtered_df["Customer ID"].count()

# Churned Customers
sub_churn = filtered_df[filtered_df['Customer Churn Status'] == 'Yes']

# Customer Churn Count & Rate
churn_count = sub_churn['Customer Churn Status'].count()
churn_rate = (sub_churn['Customer Churn Status'].count()/(filtered_df['Customer ID'].count())*100).round(1)

# Avg Customer Tenure
# metric value
mean_month = filtered_df['Customer Tenure in months'].mean()
mean_month = round(mean_month, 1)
mean_month = f"{mean_month}mnths"
# metric delta
mean_month_rate = ((1-(filtered_df['Customer Tenure in months'].mean()/(data['Customer Tenure in months'].mean())))*100).round(1)
if mean_month_rate == 0:
    month_rate = "Normal"
elif mean_month_rate <= -0:
    month_rate = f"{-(mean_month_rate)}%"
else:
    month_rate = "-"+f"{mean_month_rate}%"

# Avg Data Usage
# metric value
avg_data = filtered_df['Data Usage'].mean()
avg_data = round(avg_data, 1)
avg_data = f"{avg_data}GB"
# metric delta
avg_data_rate = ((1-(filtered_df['Data Usage'].mean()/(data['Data Usage'].mean())))*100).round(1)
if avg_data_rate == 0:
    data_rate = "Normal"
elif avg_data_rate <= -0:
    data_rate = f"{-(avg_data_rate)}%"
else:
    data_rate = "-"+f"{avg_data_rate}%"

# Avg Customer Review
# review
mean_score = filtered_df['Satisfaction Rate'].mean()
if mean_score <= 1:
    review = "Poor"
elif mean_score <= 2:
    review = "Fair"
elif mean_score <= 3:
    review = "Good"
elif mean_score <= 4:
    review = "Very Good"
else:
    review = "Excellent"
# delta
mean_score = filtered_df['Satisfaction Rate'].mean()
if mean_score <= 1:
    delta = "-"
elif mean_score <= 2:
    delta = ""
elif mean_score <= 3:
    delta = "+"
elif mean_score <= 4:
    delta = "++"
else:
    delta = "+++"

# Plots

# Revenue by States
Top_Revenue = filtered_df.groupby('State')['Total Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
Top_Revenue['Total Revenue Currency'] = Top_Revenue['Total Revenue'].apply(format_currency)

# Gender Distribution of Churn
gender_churn = filtered_df.groupby(['Gender', 'Customer Churn Status']).size().reset_index(name='count')

# Revenue by Months
month_rev = filtered_df.groupby('Month')['Total Revenue'].sum().sort_values(ascending=False).reset_index()
month_rev['Total Revenue Currency'] = month_rev['Total Revenue'].apply(format_currency)

# Churn Status by State
state_churn = filtered_df.groupby('State')['Customer Churn Status'].value_counts().reset_index(name='count').sort_values(by="count", ascending=False)

# Revenue by Subscriptions
Rev_Sub = filtered_df.groupby('Subscription Plan')['Total Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
Rev_Sub['Total Revenue Currency'] = Rev_Sub['Total Revenue'].apply(format_currency)

# Most Purchased Subscriptions vs Avg Review
sub_behave = filtered_df.groupby(['Subscription Plan', "Customer Review"])['Number of Times Purchased'].sum().sort_values(ascending=False).reset_index()

# Device Type Distribution
dev_dist = filtered_df.groupby('MTN Device')['Customer Churn Status'].value_counts().reset_index()

# Reasons for Churn
churn_reason = filtered_df.groupby('Reasons for Churn')['Customer Churn Status'].value_counts().sort_values(ascending=False).reset_index(name='count')


# Tabs
tab1, tab2, tab3 = st.tabs(["Demography", "Revenue", "Customer Behaviour"])
# Demography
with tab1:
    # Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("**Total Customer Transactions**", value=tot_cust, delta="", height=100, help="Total Customer Transactions")
    with col2:
        st.metric("**Churn Count**", value=churn_count, delta="-"+(f"{churn_rate}%"), height=100, help="Customer Churn Count & Rate")
    with col3:
        st.metric("**Retention Count**", value=tot_cust-churn_count, delta=(f"{(100-churn_rate)}%"), height=100, help="Customer Retention Count & Rate")
    with col4:
        st.metric("**Avg Customer Tenure**", value=mean_month, delta=month_rate, height=100, help="Average Customer Tenure in months")
    with col5:
        st.metric("**Avg Data Usage**", value=avg_data, delta=data_rate, height=100, help="Average Data Usage")

    # Gender Distribution of Churn
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Gender Distribution of Churn")
        fig = px.sunburst(gender_churn, path=["Gender", "Customer Churn Status"], values="count",  height=420)
        fig.update_traces(textinfo='label+value', insidetextorientation="horizontal")
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a")
        st.plotly_chart(fig, use_container_width=True)

    # Churn Status by Age Group
    with col2:
        st.markdown("### Churn Status by Age Group")
        fig = px.histogram(filtered_df, x="Age_group", color="Customer Churn Status",
                           category_orders={"Age_group": ['18-24', '25-34', '35-44', '45-54', '55+']}, height=420,
                           text_auto=True)
        fig.update_traces(textangle=0)
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                          legend=dict(font=dict(color="white"), title=dict(font=dict(color="white")), bgcolor="#111136"),
                          xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                          yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
        st.plotly_chart(fig, use_container_width=True)

    # Churn Status by State
    st.markdown("### Churn Status by State")
    fig = px.bar(state_churn, x="State", y="count", color="Customer Churn Status", text="count")
    fig.update_traces(textposition="auto")
    fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                      legend=dict(font=dict(color="white"), title=dict(font=dict(color="white")), bgcolor="#111136"),
                      xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                      yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
    st.plotly_chart(fig, use_container_width=True)

# Revenue
with tab2:
    # Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("**Total Customer Transactions**", value=tot_cust, delta="", height=100, help="Total Customer Transactions")
    with col2:
        st.metric("**Total Revenue**", value=tot_rev, delta=rev_rate, height=100, help="Total Revenue")
    with col3:
        st.metric("**Avg Customer Revenue**", value=avg_rev, delta=avg_rate, height=100, help="Avg Customer Revenue")
    with col4:
        st.metric("**Avg Customer Tenure**", value=mean_month, delta=month_rate, height=100, help="Average Customer Tenure in months")
    with col5:
        st.metric("**Avg Data Usage**", value=avg_data, delta=data_rate, height=100, help="Average Data Usage")

    col1, col2 = st.columns([0.6, 0.4])
    # Revenue by States
    with col1:
        st.markdown("### Top Revenue Generating States")
        fig = px.bar(Top_Revenue, x="State", y="Total Revenue", text="Total Revenue Currency", color="Total Revenue")
        fig.update_traces(textposition="outside", textfont_color="white")
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                          xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                          yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Months
    with col2:
        st.markdown("### Revenue by Months")
        fig = px.bar(month_rev, x="Month", y="Total Revenue", text="Total Revenue Currency", color="Total Revenue")
        fig.update_traces(textposition="outside", textfont_color="white")
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                          xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                          yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Subscriptions
    st.markdown("### Top Revenue Generating Subscriptions")
    fig = px.bar(Rev_Sub, x="Total Revenue", y="Subscription Plan", text="Total Revenue Currency", color="Total Revenue")
    fig.update_traces(textposition="inside")
    fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                      xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                      yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
    st.plotly_chart(fig, use_container_width=True)

# Customer Behaviour
with tab3:
    # Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("**Total Customer Count**", value=filtered_df["Customer ID"].nunique(), delta="", height=100, help="Total Customer Count")
    with col2:
        st.metric("**Avg Customer Review**", value=review, delta=delta, height=100, help="Avg Customer Review")
    with col3:
        st.metric("**Avg Customer Tenure**", value=mean_month, delta=month_rate, height=100, help="Average Customer Tenure in months")
    with col4:
        st.metric("**Avg Data Usage**", value=avg_data, delta=data_rate, height=100, help="Average Data Usage")

    col1, col2 = st.columns(2)
    # Device Type Distribution
    with col1:
        st.markdown("### Device Type Distribution")
        fig = px.bar(dev_dist, x="MTN Device", y="count", color="Customer Churn Status", barmode="group", text="count")
        fig.update_traces(textposition="inside", textangle=0)
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                          legend=dict(font=dict(color="white"), title=dict(font=dict(color="white")), bgcolor="#111136"),
                          xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                          yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
        st.plotly_chart(fig, use_container_width=True)

    # Reasons for Churn
    with col2:
        st.markdown("### Reasons for Churn")
        fig = px.bar(churn_reason, x="count", y="Reasons for Churn", text="count")
        fig.update_traces(textposition="inside", textangle=0)
        fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                          legend=dict(font=dict(color="white"), title=dict(font=dict(color="white")), bgcolor="#111136"),
                          xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                          yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
        st.plotly_chart(fig, use_container_width=True)

    # Most Purchased Subscriptions vs Avg Review
    st.markdown("### Most Purchased Subscriptions vs Avg Review")
    fig = px.bar(sub_behave, x="Number of Times Purchased", y="Subscription Plan", color="Customer Review",
                 text="Number of Times Purchased")
    fig.update_traces(textposition="inside", textangle=0)
    fig.update_layout(paper_bgcolor='#29295a', plot_bgcolor="#29295a",
                      legend=dict(font=dict(color="white"), title=dict(font=dict(color="white")), bgcolor="#111136"),
                      xaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
                      yaxis=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))))
    st.plotly_chart(fig, use_container_width=True)

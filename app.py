import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Credit Risk Dashboard")

st.success("Imports Working ✅")
import pymysql

# Establish database connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="mariammal93",
    database="credit_risk",
    port=3306
) 
combined_df = pd.read_sql("select * from loan_data",mydb)

st.dataframe(combined_df)
 #  SIDEBAR
# --------------------------------------------------

st.sidebar.title(" Credit Risk Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard Overview",
        "Loan Analysis",
        "Financial Analysis",
        "Customer Analysis",
        "Risk Analysis",
        "SQL Reports",
        "Business Insights"
    ]
)
# ==================================================
# DASHBOARD OVERVIEW
# ==================================================

if page == "Dashboard Overview":

    st.title(" Credit Risk Analysis Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Applicants",
        f"{len(combined_df):,}"
    )

    col2.metric(
        "Avg Credit Amount",
        f"{combined_df['AMT_CREDIT'].mean():,.0f}"
    )

    col3.metric(
        "Avg Application Amount",
        f"{combined_df['AMT_APPLICATION'].mean():,.0f}"
    )

    col4.metric(
        "Avg Annuity",
        f"{combined_df['AMT_ANNUITY'].mean():,.0f}"
    )

    st.markdown("---")

    st.subheader("Contract Type Distribution")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=combined_df,
        x="NAME_CONTRACT_TYPE",
        order=combined_df["NAME_CONTRACT_TYPE"].value_counts().index,
        ax=ax
    )

    plt.xticks(rotation=30)

    st.pyplot(fig)
   
   
    # LOAN ANALYSIS
# 

elif page == "Loan Analysis":

    st.title(" Loan Analysis")

    st.subheader("Loan Contract Status")

    fig1, ax1 = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=combined_df,
        x="NAME_CONTRACT_STATUS",
        order=combined_df["NAME_CONTRACT_STATUS"].value_counts().index,
        ax=ax1
    )

    plt.xticks(rotation=25)

    st.pyplot(fig1)

    st.subheader("Loan Portfolio Distribution")

    fig2, ax2 = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=combined_df,
        x="NAME_PORTFOLIO",
        order=combined_df["NAME_PORTFOLIO"].value_counts().index,
        ax=ax2
    )

    plt.xticks(rotation=25)

    st.pyplot(fig2)

    # FINANCIAL ANALYSIS
# 

elif page == "Financial Analysis":

    st.title(" Financial Analysis")

    selected_col = st.selectbox(
        "Choose Financial Variable",
        [
            "AMT_CREDIT",
            "AMT_APPLICATION",
            "AMT_ANNUITY",
            "AMT_GOODS_PRICE",
            "AMT_DOWN_PAYMENT"
        ]
    )

    st.write(combined_df[selected_col].describe())

    fig1, ax1 = plt.subplots(figsize=(8,5))

    sns.histplot(
        combined_df[selected_col],
        kde=True,
        ax=ax1
    )

    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8,2))

    sns.boxplot(
        x=combined_df[selected_col],
        ax=ax2
    )

    st.pyplot(fig2)

   #  CUSTOMER ANALYSIS
# 
elif page == "Customer Analysis":

    st.title(" Customer Analysis")

    customer_chart = st.selectbox(
        "Select Customer View",
        [
            "NAME_CLIENT_TYPE",
            "NAME_TYPE_SUITE",
            "CHANNEL_TYPE",
            "NAME_SELLER_INDUSTRY"
        ]
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.countplot(
        data=combined_df,
        x=customer_chart,
        order=combined_df[customer_chart].value_counts().index,
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

# RISK ANALYSIS
# ==================================================

elif page == "Risk Analysis":

    st.title(" Credit Risk Indicators")

    st.subheader("Reject Reason Analysis")

    fig1, ax1 = plt.subplots(figsize=(10,5))

    sns.countplot(
        data=combined_df,
        x="CODE_REJECT_REASON",
        order=combined_df["CODE_REJECT_REASON"].value_counts().index,
        ax=ax1
    )

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    st.subheader("Yield Group Analysis")

    fig2, ax2 = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=combined_df,
        x="NAME_YIELD_GROUP",
        order=combined_df["NAME_YIELD_GROUP"].value_counts().index,
        ax=ax2
    )

    st.pyplot(fig2)

# SQL REPORTS
# ==================================================

elif page == "SQL Reports":

    st.title("🗄 SQL Query Reports")

    query_option = st.selectbox(
        "Select SQL Query",
        [
            "1. Contract Type Count",
            "2. Contract Status Count",
            "3. Client Type Count",
            "4. Portfolio Distribution",
            "5. Product Type Distribution",
            "6. Yield Group Distribution",
            "7. Reject Reason Distribution",
            "8. Seller Industry Count",
            "9. Goods Category Count",
            "10. Payment Type Distribution",
            "11. Average Credit Amount",
            "12. Average Application Amount",
            "13. Average Annuity",
            "14. Top 10 Seller Industries",
            "15. Top 10 Goods Categories",
            "16. Applications by Weekday",
            "17. Applications by Hour",
            "18. Product Combination Count",
            "19. Loan Purpose Distribution",
            "20. Client Type vs Contract Status"
        ]
    )

    from sqlalchemy import create_engine
    engine = create_engine(
        "mysql+pymysql://root:mariammal93@localhost/credit_risk"
    )

    if query_option == "1. Contract Type Count":

        query = """
        SELECT NAME_CONTRACT_TYPE,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_CONTRACT_TYPE
        """

    elif query_option == "2. Contract Status Count":

        query = """
        SELECT NAME_CONTRACT_STATUS,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_CONTRACT_STATUS
        """

    elif query_option == "3. Client Type Count":

        query = """
        SELECT NAME_CLIENT_TYPE,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_CLIENT_TYPE
        """

    elif query_option == "4. Portfolio Distribution":

        query = """
        SELECT NAME_PORTFOLIO,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_PORTFOLIO
        """

    elif query_option == "5. Product Type Distribution":

        query = """
        SELECT NAME_PRODUCT_TYPE,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_PRODUCT_TYPE
        """

    elif query_option == "6. Yield Group Distribution":

        query = """
        SELECT NAME_YIELD_GROUP,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_YIELD_GROUP
        """

    elif query_option == "7. Reject Reason Distribution":

        query = """
        SELECT CODE_REJECT_REASON,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY CODE_REJECT_REASON
        """
    elif query_option == "8. Seller Industry Count":

        query = """
        SELECT NAME_SELLER_INDUSTRY,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_SELLER_INDUSTRY
        """

    elif query_option == "9. Goods Category Count":

        query = """
        SELECT NAME_GOODS_CATEGORY,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_GOODS_CATEGORY
        """

    elif query_option == "10. Payment Type Distribution":

        query = """
        SELECT NAME_PAYMENT_TYPE,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_PAYMENT_TYPE
        """

    elif query_option == "11. Average Credit Amount":

        query = """
        SELECT AVG(AMT_CREDIT) AS Average_Credit
        FROM loan_data
        """

    elif query_option == "12. Average Application Amount":

        query = """
        SELECT AVG(AMT_APPLICATION) AS Average_Application
        FROM loan_data
        """

    elif query_option == "13. Average Annuity":

        query = """
        SELECT AVG(AMT_ANNUITY) AS Average_Annuity
        FROM loan_data
        """

    elif query_option == "14. Top 10 Seller Industries":

        query = """
        SELECT NAME_SELLER_INDUSTRY,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_SELLER_INDUSTRY
        ORDER BY Total DESC
        LIMIT 10
        """

    elif query_option == "15. Top 10 Goods Categories":

        query = """
        SELECT NAME_GOODS_CATEGORY,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_GOODS_CATEGORY
        ORDER BY Total DESC
        LIMIT 10
        """

    elif query_option == "16. Applications by Weekday":

        query = """
        SELECT WEEKDAY_APPR_PROCESS_START,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY WEEKDAY_APPR_PROCESS_START
        """

    elif query_option == "17. Applications by Hour":

        query = """
        SELECT HOUR_APPR_PROCESS_START,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY HOUR_APPR_PROCESS_START
        ORDER BY HOUR_APPR_PROCESS_START
        """

    elif query_option == "18. Product Combination Count":

        query = """
        SELECT PRODUCT_COMBINATION,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY PRODUCT_COMBINATION
        """

    elif query_option == "19. Loan Purpose Distribution":

        query = """
        SELECT NAME_CASH_LOAN_PURPOSE,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_CASH_LOAN_PURPOSE
        """

    else:

        query = """
        SELECT NAME_CLIENT_TYPE,
               NAME_CONTRACT_STATUS,
               COUNT(*) AS Total
        FROM loan_data
        GROUP BY NAME_CLIENT_TYPE,
                 NAME_CONTRACT_STATUS
        """

    result = pd.read_sql(query, engine)

    st.dataframe(result)

# BUSINESS INSIGHTS
# ==================================================

elif page == "Business Insights":

   st.title(" Key Business Insights")

   st.success(
        """
        ✅ Consumer Loans are the most common contract type.

        ✅ Approved applications dominate the dataset.

        ✅ Repeat customers form the majority of applicants.

        ✅ Most loan applications occur during business hours.

        ✅ Consumer Electronics and Mobile products are heavily financed.

        ✅ High-value loan applications create positive skewness in financial variables.

        ✅ Credit and Cash Offices are the dominant application channel.
        """
    )

import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

selected_page = st.sidebar.selectbox('Select an option', ['Top 10 Green Stocks', 'Top 10 Loss Stocks', 
                                                            'Overall Number Of Green Vs Red Stocks',
                                                            'Average Price Across All Stocks',
                                                            'Average Volume Across All Stocks', 'Volatility Analysis',
                                                            'Cumulative Return Over Time',
                                                            'Sector-wise Performance', 'Stock Price Correlation',
                                                            'Top 5 Gainers and Losers (Month-wise)'])

st.markdown(f'**{selected_page}**')

conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pwd12345',
        database='practice'
    )

cursor = conn.cursor()

if selected_page == 'Top 10 Green Stocks':
    st.write('Top 10 Stocks based on yearly return.')
    cursor.execute("SELECT TICKER, YEARLY_RETURN FROM GREEN_RED_STOCKS ORDER BY YEARLY_RETURN DESC LIMIT 10")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['TICKER', 'YEARLY_RETURN'])

    st.dataframe(df)

    fig, ax = plt.subplots()
    bar_chart = ax.bar(df['TICKER'], df['YEARLY_RETURN'])
    ax.set_xlabel('Stocks')
    ax.set_ylabel('Yearly Return')
    plt.xticks(rotation = 45)
    ax.bar_label(bar_chart)
    st.pyplot(fig)

if selected_page == 'Top 10 Loss Stocks':
    st.write('Top 10 Loss Stocks based on yearly return.')
    cursor.execute("SELECT TICKER, YEARLY_RETURN FROM GREEN_RED_STOCKS ORDER BY YEARLY_RETURN ASC LIMIT 10")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['TICKER', 'YEARLY_RETURN'])

    st.dataframe(df)

    fig, ax = plt.subplots()
    bar_chart = ax.bar(df['TICKER'], df['YEARLY_RETURN'])
    ax.set_xlabel('Stocks')
    ax.set_ylabel('Yearly Return')
    plt.xticks(rotation = 45)
    ax.bar_label(bar_chart)
    st.pyplot(fig)

if selected_page == 'Overall Number Of Green Vs Red Stocks':
    cursor.execute("SELECT GREEN_RED_STOCK, COUNT(TICKER) AS STOCK_COUNT FROM NUMBER_OF_GREEN_VS_RED_STOCKS GROUP BY GREEN_RED_STOCK")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['STOCK', 'STOCK COUNT'])

    st.dataframe(df)

if selected_page == 'Average Price Across All Stocks':
    st.write('Average Price Of Each Stock')
    cursor.execute("SELECT * FROM STOCKS_AVERAGE_PRICE ORDER BY AVERAGE_PRICE")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['STOCK', 'Average Price'])

    st.dataframe(df)

    cursor.execute("SELECT round(AVG(AVERAGE_PRICE), 2) AS AVERAGE_PRICE FROM STOCKS_AVERAGE_PRICE")
    rows = cursor.fetchone()

    st.write(f'**Average Price Across All Stocks : {rows[0]}**')

if selected_page == 'Average Volume Across All Stocks':
    st.write('Average Volume Of Each Stock')
    cursor.execute("SELECT * FROM STOCKS_AVERAGE_VOLUME ORDER BY AVERAGE_VOLUME")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['STOCK', 'Average Volume'])

    st.dataframe(df)

    cursor.execute("SELECT ROUND(AVG(AVERAGE_VOLUME)) AS AVERAGE_VOLUME FROM STOCKS_AVERAGE_VOLUME")
    rows = cursor.fetchone()

    st.write(f'**Average Volume Across All Stocks : {rows[0]}**')

if selected_page == 'Volatility Analysis':
    st.write('Top 10 most volatile stocks over the year')
    cursor.execute("SELECT * FROM volatility_analysis")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Stocks', 'Volatility'])

    fig, ax = plt.subplots()
    bar_chart = ax.bar(df['Stocks'], df['Volatility'])
    ax.set_xlabel('Stocks')
    ax.set_ylabel('Volatility')
    plt.xticks(rotation = 45)
    ax.bar_label(bar_chart)
    st.pyplot(fig)

elif selected_page == 'Cumulative Return Over Time':
    st.write('Top 5 performing stocks (based on cumulative return) over the course of the year')
    cursor.execute("SELECT * FROM cumulative_return_over_time")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Stocks', 'Cumulative_Return_Over_Time'])

    fig, ax = plt.subplots()
    ax.plot(df['Stocks'], df['Cumulative_Return_Over_Time'], marker='o', color='green')
    ax.set_xlabel('Stocks')
    ax.set_ylabel('Cumulative Return Over Time')
    ax.set_title('Cumulative Return for Top 5 Performing Stocks')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif selected_page == 'Sector-wise Performance':
    cursor.execute("SELECT * FROM sectorwise_performance")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Sector', 'Yearly_Return'])

    fig, ax = plt.subplots(figsize = (20, 10))
    bar_chart = ax.bar(df['Sector'], df['Yearly_Return'])
    ax.set_xlabel('Sector')
    ax.set_ylabel('Average Yearly Return Percentage')
    plt.xticks(rotation = 45)
    ax.bar_label(bar_chart)
    st.pyplot(fig)

elif selected_page == 'Stock Price Correlation':
    st.write('Heatmap shows the correlation between the closing prices of various stocks')
    cursor.execute("SELECT * FROM stock_price_correlation")
    rows = cursor.fetchall()

    db_column_name = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns = db_column_name)
    fig, ax = plt.subplots(figsize=(30, 25))
    sns.heatmap(df.corr(), annot = True)
    st.pyplot(fig)

elif selected_page == 'Top 5 Gainers and Losers (Month-wise)':
    
    gainers, losers = st.tabs(["Gainers", "Losers"])

    with gainers:
        st.title('Gainers')
        cursor.execute("SELECT DISTINCT(MONTH) FROM top_5_gainers")
        gainers_months = cursor.fetchall()

        gainers_month_list = []

        for gainers_month in gainers_months:
            gainers_month_list.append(gainers_month[0])

        gainers_month_tab_objects = st.tabs(gainers_month_list)
        for tab, month in zip(gainers_month_tab_objects, gainers_month_list):
            with tab:
                st.write(f"Top 5 gainers for month: {month}")
                cursor.execute(f"SELECT Ticker, Monthly_return FROM top_5_gainers where month = '{month}'")
                rows = cursor.fetchall()

                db_column_name = [desc[0] for desc in cursor.description]
                gainers_df = pd.DataFrame(rows, columns = db_column_name)

                fig, ax = plt.subplots()
                bar_chart = ax.bar(gainers_df['Ticker'], gainers_df['Monthly_return'])
                ax.set_xlabel('Ticker')
                ax.set_ylabel('Monthly Return')
                plt.xticks(rotation = 45)
                ax.bar_label(bar_chart)
                st.pyplot(fig)
    
    with losers:
        st.title('Losers')

        cursor.execute("SELECT DISTINCT(MONTH) FROM top_5_losers")
        losers_months = cursor.fetchall()

        losers_month_list = []

        for losers_month in losers_months:
            losers_month_list.append(losers_month[0])

        losers_month_tab_objects = st.tabs(losers_month_list)
        for tab, month in zip(losers_month_tab_objects, losers_month_list):
            with tab:
                st.write(f"Top 5 losers for month: {month}")
                cursor.execute(f"SELECT Ticker, Monthly_return FROM top_5_losers where month = '{month}'")
                rows = cursor.fetchall()

                db_column_name = [desc[0] for desc in cursor.description]
                losers_df = pd.DataFrame(rows, columns = db_column_name)
                
                fig, ax = plt.subplots()
                bar_chart = ax.bar(losers_df['Ticker'], losers_df['Monthly_return'])
                ax.set_xlabel('Ticker')
                ax.set_ylabel('Monthly Return')
                plt.xticks(rotation = 45)
                ax.bar_label(bar_chart)
                st.pyplot(fig)


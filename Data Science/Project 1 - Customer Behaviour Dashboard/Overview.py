import streamlit as st
import pandas as pd
from babel.numbers import format_currency
import altair as alt


def get_unique_years(df: pd.DataFrame) -> list:
    """Get unique years from the dataset."""
    return df['YearOfTransaction'].unique().tolist()

def get_unique_months(df: pd.DataFrame) -> list:
    """Get unique months from the dataset."""
    return df['MonthOfTransaction'].unique().tolist()

def get_unique_purchase_types(df: pd.DataFrame) -> list:
    """Get unique purchase types from the dataset."""
    return df['PurchaseType'].unique().tolist()

def filter_data(df: pd.DataFrame, year: int, month: int, purchase_type: str) -> pd.DataFrame:
    """Filter the dataset based on year and purchase type."""
    return df[(df['YearOfTransaction'] == year) & (df['MonthOfTransaction'] == month) & (df['PurchaseType'] == purchase_type)]

def get_period_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total quantity of orders for each period (year and month). The result dataframe contains columns 'YearOfTransaction', 'MonthOfTransaction', 'TotalQuantity', 'Period', and 'PeriodDate'. The 'Period' column contains a string representation of each period in the format 'MM/YYYY'. The 'PeriodDate' column contains a datetime representation of each period."""
    period_quantity = df.groupby(by=['YearOfTransaction', 'MonthOfTransaction'], observed=True)[['Quantity']].agg({
        'Quantity': 'sum'
    }).rename(columns={
        'Quantity':'TotalQuantity'
    }).reset_index()
    period_quantity['Period'] = period_quantity['MonthOfTransaction'].astype(str).str.zfill(2) + '/' + period_quantity['YearOfTransaction'].astype(str)
    period_quantity['PeriodDate'] = pd.to_datetime(period_quantity['Period'])
    return period_quantity.sort_values(by=['YearOfTransaction', 'MonthOfTransaction'], ascending=True)

def get_period_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total revenue of orders for each period (year and month). The result dataframe contains columns 'YearOfTransaction', 'MonthOfTransaction', 'Revenue', 'Period', and 'PeriodDate'. The 'Period' column contains a string representation of each period in the format 'MM/YYYY'. The 'PeriodDate' column contains a datetime representation of each period."""
    period_revenue = df.groupby(by=['YearOfTransaction', 'MonthOfTransaction'], observed=True)[['TotalPrice']].agg({
        'TotalPrice': 'sum'
    }).rename(columns={
        'TotalPrice':'Revenue'
    }).reset_index()
    period_revenue['Period'] = period_revenue['MonthOfTransaction'].astype(str).str.zfill(2) + '/' + period_revenue['YearOfTransaction'].astype(str)
    period_revenue['PeriodDate'] = pd.to_datetime(period_revenue['Period'])
    return period_revenue.sort_values(by=['YearOfTransaction', 'MonthOfTransaction'], ascending=True)

def get_weekly_order_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total quantity of orders for each week in each month. The result dataframe contains columns 'YearMonth', 'Week', 'Quantity', and 'PeriodDate'. The 'YearMonth' column contains a string representation of each month in the format 'YYYY-MM'. The 'PeriodDate' column contains a datetime representation of each month."""
    df['Week'] = df['InvoiceDate'].dt.isocalendar().week
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    weekly_orders = df.groupby(['YearMonth', 'Week'])[['Quantity']].sum().reset_index()
    weekly_orders['PeriodDate'] = pd.to_datetime(weekly_orders['YearMonth'])
    return weekly_orders

def get_weekly_day_order_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Get the total quantity of orders for each day of the week in each month.

    The resulting dataframe contains columns 'YearMonth', 'DayName', and 'Quantity'.
    The 'YearMonth' column contains a string representation of each month in the format 'YYYY-MM'.
    The 'DayName' column contains the name of the day (e.g., Monday, Tuesday).
    """

    df['DayName'] = df['InvoiceDate'].dt.day_name()
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    day_trend = df.groupby(['YearMonth', 'DayName'])[['Quantity']].sum().reset_index()
    return day_trend

def get_top_5_country_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the top 5 countries with the highest revenue. The resulting dataframe contains columns 'Country' and 'TotalPrice'.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe containing the data.

    Returns
    -------
    pd.DataFrame
        A dataframe containing the top 5 countries with the highest revenue.
    """
    top_countries = df.groupby('Country')[['TotalPrice']].sum().sort_values(by='TotalPrice', ascending=False).reset_index().head(5)
    return top_countries

def get_barplot_using_altair(df: pd.DataFrame, xfield: str, yfield: str, xlabel: str, ylabel: str, main_title: str, color_schemes: str, xtype: str='nominal', ytype: str='quantitative', sorter=None) -> alt.Chart:
    """Get a barplot using Altair.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe containing the data.
    xfield : str
        The name of the column for the x-axis.
    yfield : str
        The name of the column for the y-axis.
    xlabel : str
        The label for the x-axis.
    ylabel : str
        The label for the y-axis.
    main_title : str
        The title for the plot.
    color_schemes : str
        The color scheme for the bars.
    xtype : str, optional
        The type of the x-axis, by default 'nominal'.
    ytype : str, optional
        The type of the y-axis, by default 'quantitative'.
    sorter : list or None, optional
        A list of values to sort the x-axis by, by default None.

    Returns
    -------
    alt.Chart
        A barplot using Altair.
    """
    chart = alt.Chart(df).mark_bar().encode(
        x = alt.X(xfield, type=xtype, title=xlabel, sort=sorter, axis=alt.Axis(labelAngle=45, labelOverlap=False)),
        y = alt.Y(yfield, type=ytype, title=ylabel),
        color=alt.Color(yfield, type=ytype, scale=alt.Scale(scheme=color_schemes)),
        tooltip=[xfield, yfield]
    ).properties(
        width=1200,
        height=400,
        title=main_title
    )
    return chart

def get_lineplot_using_altair(df: pd.DataFrame, xfield: str, yfield: str, xtitle: str, ytitle: str, main_title: str, color_field: str, color_field_title: str, xtype: str='ordinal', ytype: str='quantitative', color_field_type: str='nominal', color_schemes: str='viridis', sorter=None):
    """
    Function to create a lineplot using Altair.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe containing the data.
    xfield : str
        The name of the column for the x-axis.
    yfield : str
        The name of the column for the y-axis.
    xtitle : str
        The label for the x-axis.
    ytitle : str
        The label for the y-axis.
    main_title : str
        The title for the plot.
    color_field : str
        The name of the column for the color of the line.
    color_field_title : str
        The title of the color legend.
    xtype : str, optional
        The type of the x-axis, by default 'ordinal'.
    ytype : str, optional
        The type of the y-axis, by default 'quantitative'.
    color_field_type : str, optional
        The type of the color field, by default 'nominal'.
    color_schemes : str, optional
        The color scheme for the lines, by default 'viridis'.
    sorter : list or None, optional
        A list of values to sort the x-axis by, by default None.

    Returns
    -------
    alt.Chart
        A lineplot using Altair.
    """
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(xfield, type=xtype, sort=sorter, title=xtitle),
        y=alt.Y(yfield, type=ytype, title=ytitle),
        color=alt.Color(color_field, type=color_field_type, title=color_field_title, scale=alt.Scale(scheme=color_schemes)),
        tooltip=[color_field, xfield, yfield]
    ).properties(
        width=1000,
        height=400,
        title=main_title
    )
    return chart

def main(df: pd.DataFrame):
    """Main function to render the Streamlit dashboard."""
    st.title("Sales Overview Dashboard ✨")
    st.write("Overview All Insight About All Online Retail Transaction In 2010 Until 2011!")
    st.divider()

    # Sidebar filters
    with st.sidebar:
        st.header("Filter Options")
        year_option = st.selectbox("Select Year", get_unique_years(df))
        month_option = st.selectbox("Select Month", get_unique_months(df))
        purchase_type_option = st.selectbox("Select Purchase Type", get_unique_purchase_types(df))
        submit_button = st.button("Apply Filters")

    # Filter dataset based on usert input
    filtered_data = filter_data(df, year_option, month_option, purchase_type_option) if submit_button else df

    # Metrics section
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.metric(label="Total Transactions", value=len(filtered_data['InvoiceNo'].tolist()) if 'InvoiceNo' in filtered_data else 'N/A')
    with col2:
        st.metric(label="Unique Customers", value=filtered_data['CustomerID'].nunique() if 'CustomerID' in filtered_data else "N/A")
    with col3:
        st.metric(label="Total Country", value=len(filtered_data['Country'].unique().tolist()) if 'Country' in filtered_data else "N/A")
    col4, col5 = st.columns([1, 2])
    with col4:
        st.metric(label="Unique Product", value=len(filtered_data['Description'].unique().tolist()) if 'Description' in filtered_data else 'N/A')
    with col5:
        st.metric(label="Total Revenue (USD)", value=format_currency(filtered_data['TotalPrice'].sum(), 'USD', locale='en_US') if 'TotalPrice' in filtered_data else "N/A")
    
    # Display monthly transaction trends
    st.divider()
    st.subheader("Monthly Transactions Trends 2010 to 2011")
    period_quantity_data = get_period_quantity(df=df)
    period_quantity_chart = get_barplot_using_altair(df=period_quantity_data, xfield='Period', yfield='TotalQuantity', xlabel='Transaction Period', ylabel='Total of Quantity', main_title='Total of Transaction Per Month In 2010 to 2011', color_schemes='reds', sorter=period_quantity_data.sort_values(by='PeriodDate')['Period'].tolist())
    with st.container():
        st.altair_chart(period_quantity_chart, use_container_width=True)

    # Display monthly revenue trends
    st.divider()
    st.subheader('Monthly Revenue Trends 2010 to 2011')
    period_revenue_data = get_period_revenue(df=df)
    period_revenue_chart = get_barplot_using_altair(df=period_revenue_data, xfield='Period', yfield='Revenue', xlabel='Transaction Period', ylabel='Total Revenue', main_title='Total of Revenue Per Month In 2010 to 2011', color_schemes='greens', sorter=period_revenue_data.sort_values(by='PeriodDate')['Period'].tolist())
    with st.container():
        st.altair_chart(period_revenue_chart, use_container_width=True)

    # Displays sales trends for each item each week for each month
    st.divider()
    st.subheader('Trends in Orders for Goods Every Week and Month from 2010 to 2011')
    weekly_orders_data = get_weekly_order_trend(df=df)
    weekly_orders_chart = get_lineplot_using_altair(df=weekly_orders_data, xfield='Week', yfield='Quantity', main_title='Weekly Order Trend per Month (2010-2011)', color_field='YearMonth', color_field_title='Transaction Period', xtitle='Week Number', ytitle='Total Quantity', sorter=weekly_orders_data.sort_values(by='PeriodDate')['Week'].tolist())
    with st.container():
        st.altair_chart(weekly_orders_chart, use_container_width=True)
        
    # Displays the most transaction trends every day (Monday-Sunday) for every month
    st.divider()
    st.subheader('Most Transaction Trends Monday-Sunday Per Month')
    day_trends_data = get_weekly_day_order_trend(df=df)
    day_trends_chart = get_lineplot_using_altair(df=day_trends_data, xfield='DayName', yfield='Quantity', main_title='Most Frequent Transaction Days Per Month', color_field='YearMonth', color_field_title='Transaction Period', xtype='nominal', sorter=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], xtitle='DayNames', ytitle='Total Quantity')
    with st.container():
        st.altair_chart(day_trends_chart, use_container_width=True)

    # Showing the Top 5 Countries with the Most Revenue 
    st.divider()
    st.subheader('Top 5 Countries Contributing the Most Revenue from 2010 to 2011')
    top_country_data = get_top_5_country_revenue(df=df)
    top_country_chart = get_barplot_using_altair(df=top_country_data, xfield="Country", xtype='nominal', yfield='TotalPrice', ytype='quantitative', sorter='-y', xlabel='Country', ylabel='Total Revenue', color_schemes='blues', main_title='Top 5 Countries by Total Revenue (2010–2011)')
    with st.container():
        st.altair_chart(top_country_chart, use_container_width=True)

    

if __name__ == "__main__":
    # Load dataset
    df = pd.read_feather("dataset/online_retail_with_date.feather")
    main(df)
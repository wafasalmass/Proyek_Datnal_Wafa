import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import numpy as np

#load Bike_day
Bike_day = pd.read_excel('dashboard/Bike_rental.xlsx', sheet_name='day')
Bike_hour = pd.read_excel('dashboard/Bike_rental.xlsx', sheet_name='period')

def sidebar(Bike_day):
    Bike_day['dteday'] = pd.to_datetime(Bike_day['dteday'])
    min_date = Bike_day['dteday'].min()
    max_date = Bike_day['dteday'].max()
    with st.sidebar:
        st.image("https://png.pngtree.com/png-clipart/20230807/original/pngtree-vector-illustration-of-a-bicycle-rental-logo-on-a-white-background-vector-picture-image_10130406.png")
        def on_change():
            st.session_state.date =date
        
        date = st.date_input(
            label='Date Range',
            min_value=min_date,
            max_value=max_date,
            value=[min_date,max_date],
            on_change=on_change
        )
    return date

dateBar = sidebar(Bike_day)
if len(dateBar) == 2:
    main_bikeDay = Bike_day[(Bike_day['dteday'] >= str(dateBar[0])) & (Bike_day['dteday'] <= str(dateBar[1]))]
else:
    main_bikeDay = Bike_day[(Bike_day['dteday'] >= str(st.session_date[0]) & (Bike_day['dteday'] <= str(st.session_state.date[1])))]

st.sidebar.write('Dashboard by: Wafa Salma Sentanu')

total = int(main_bikeDay['count'].sum())
average = round(main_bikeDay['count'].mean())
current_date = datetime.datetime.now()
def get_season(months):
    if months in range(3, 6):
        return "Spring"
    elif months in range(6, 9):
        return "Summer"
    elif months in range(9, 12): 
        return "Autumn"
    else: 
        return "Winter"
current_date = datetime.datetime.now()
current_month = current_date.month
current_season = get_season(current_month)

st.title("Bike Sharing Dashboard")
left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader("Rent Total:")
    st.subheader(f"{total:,}")
with mid_col:
    st.subheader("Rent Average:")
    st.subheader(f"{average:,}")
with right_col:
    st.subheader("Season Today:")
    st.subheader(f"{current_season}")

st.markdown("---")

#---Visualization 1 ------------------------------------------------
st.subheader('Total Rental Bike in weekday and weekend by Period')

weekday_Filter = Bike_hour[Bike_hour['weekday'].isin(["Mon", "Tue", "Wed", "Thu", "Fri"])]
countRent_Weekday = weekday_Filter.groupby(['period']).agg({
    'count': ['sum', 'mean', 'max', 'min'],
})
countRent_Weekday.sort_values(('count', 'sum'), ascending=False)

weekend_Filter = Bike_hour[Bike_hour['weekday'].isin(["Sun", "Sat"])]
countRent_Weekend = weekend_Filter.groupby(['period']).agg({
    'count': ['sum', 'mean', 'max', 'min'],
})
countRent_Weekend.sort_values(('count', 'sum'), ascending=False)

# Plotting total rental bike for weekday by period
countRent_PeriodWeekday_sum = countRent_Weekday[('count', 'sum')].sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(20, 12))
countRent_PeriodWeekday_sum.plot(kind='bar', color='skyblue', label='Weekday', ax=ax)

# Plotting total rental bike for weekend by period
countRent_PeriodWeekend_sum = countRent_Weekend[('count', 'sum')].sort_values(ascending=False)
countRent_PeriodWeekend_sum.plot(kind='bar', color='maroon', alpha=0.7, label='Weekend', ax=ax)

ax.tick_params(axis='x', rotation = 0, labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend()
for i, value in enumerate(countRent_PeriodWeekday_sum):
    plt.text(i, value, str(int(value)), ha='center', va='bottom', fontsize=20)
for i, value in enumerate(countRent_PeriodWeekend_sum):
    plt.text(i, value, str(int(value)), ha='center', va='bottom', fontsize=20)


# Displaying the plot
st.pyplot(fig)

# --- Visualization 2 ------------------------------------------
st.subheader('Total Rental Count by Month in 2011 and 2012')
countRent_Month = Bike_day.groupby(['years','months']).agg({
    'count':'sum'
}).reset_index()

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
countRent_Month['months'] = pd.Categorical(countRent_Month['months'], categories=month_order, ordered=True)
countRent_Month = countRent_Month.sort_values(by=['months'])

# Plotting
fig, ax = plt.subplots(figsize=(20, 12))
countRent_Month.groupby('years').plot(kind='line', x='months', y='count', marker='o', ax=ax)
ax.tick_params(axis = 'x', labelsize=20)
ax.tick_params(axis = 'y', labelsize=20)
ax.legend(title='Year')
ax.grid(True)
st.pyplot(fig)

    
#--- Visualization 3---------------------------------------------------------------
st.subheader('Correlation between temperature, humidity, and windspeed and the count of total rental bikes')
fig, ax = plt.subplots(figsize=(10, 6))
correlation = Bike_day[['temp','hum','windspeed','count']]
correlation = correlation.corr()
sns.heatmap(correlation, annot=True, ax=ax)
st.pyplot(fig)
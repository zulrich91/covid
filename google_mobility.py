import pandas as pd

# data source https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=a43fe0ffe294f86f
google_m_df = pd.read_csv("Global_Mobility_Report.csv")
france_df = google_m_df[google_m_df['country_region']=='France']
columns = ['date',
          'retail_and_recreation_percent_change_from_baseline', 
          'grocery_and_pharmacy_percent_change_from_baseline',
         'parks_percent_change_from_baseline',
         'transit_stations_percent_change_from_baseline',
         'workplaces_percent_change_from_baseline',
         'residential_percent_change_from_baseline']

for date, data in france_df.groupby('date'):
    col0 = date
    col1 = round(data[result_df.columns[1]].mean(),2)
    col2 = round(data[result_df.columns[2]].mean(),2)
    col3 = round(data[result_df.columns[4]].mean(),2)
    col4 = round(data[result_df.columns[4]].mean(),2)
    col5 = round(data[result_df.columns[5]].mean(),2)
    col6 = round(data[result_df.columns[6]].mean(),2)
    data_append = {result_df.columns[0]:col0, 
                   result_df.columns[1]:col1,
                   result_df.columns[2]:col2,
                   result_df.columns[3]:col3,
                   result_df.columns[4]:col4,
                   result_df.columns[5]:col5,
                   result_df.columns[6]:col6
                  }
    append_df = pd.DataFrame(data=[data_append])
    result_df = pd.concat([result_df, append_df])

result_df.to_csv('mobility.csv', index=False)



import pandas as pd
import re
import streamlit as st
import plotly.express as px

def main():
    # Read saved bracket data from csv
    entries_data = pd.read_csv('output/2024_entries_data.csv')

    # build superbowl winner picks dataframe for plotting
    superbowl_picks = entries_data.groupby(['superbowl-winner'])['superbowl-winner'].count().reset_index(name='count')
    total_entries=superbowl_picks['count'].sum()
    superbowl_picks['percent'] = superbowl_picks['count'] / total_entries * 100

    # round and sort
    superbowl_picks = superbowl_picks.round({'percent': 2}).sort_values(by=['count', 'superbowl-winner'], ascending=False)

    # convert percent to string and add '%' symbol for displaying
    superbowl_picks['percent'] = superbowl_picks['percent'].astype(str) + '%'


    print(superbowl_picks)

    fig = px.bar(superbowl_picks, x='count', y='superbowl-winner', text='percent', color='superbowl-winner'
                 ,title='Super Bowl Winners', orientation='h')

    # st.write(fig)
    st.plotly_chart(fig, use_container_width=True)

    # st.subheader('Raw data')
    # st.write(entries_data)

    

 
    

if __name__ == '__main__':
    main()
# https://docs.google.com/spreadsheets/d/10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko/edit?usp=sharing
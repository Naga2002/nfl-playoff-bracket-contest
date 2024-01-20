import pandas as pd
import streamlit as st
import plotly.express as px

def build_superbowl_picks_df(entries_data):
    # build superbowl winner picks dataframe for plotting
    superbowl_picks = entries_data.groupby(['superbowl-winner'])['superbowl-winner'].count().reset_index(name='count')
    total_entries=superbowl_picks['count'].sum()
    superbowl_picks['percent'] = superbowl_picks['count'] / total_entries * 100

    # round and sort
    superbowl_picks = superbowl_picks.round({'percent': 2}).sort_values(by=['count', 'superbowl-winner'], ascending=False)

    # convert percent to string and add '%' symbol for displaying
    superbowl_picks['percent'] = superbowl_picks['percent'].astype(str) + '%'

    return superbowl_picks

def build_superbowl_appears_df(entries_data):
    # Concat series of both column values
    series1 = entries_data['superbowl-team_1']
    series2 = entries_data['superbowl-team_2']
    unioned_df = pd.concat([series1, series2]).to_frame(name = 'superbowl-teams')

    # Group by and get counts along with percent of total
    superbowl_appears = unioned_df.groupby(['superbowl-teams'])['superbowl-teams'].count().reset_index(name='count')
    total_entries=superbowl_appears['count'].sum()
    superbowl_appears['percent'] = superbowl_appears['count'] / total_entries * 100

    # round and sort
    superbowl_appears = superbowl_appears.round({'percent': 2}).sort_values(by=['count', 'superbowl-teams'], ascending=False)

    # convert percent to string and add '%' symbol for displaying
    superbowl_appears['percent'] = superbowl_appears['percent'].astype(str) + '%'

    return superbowl_appears    

def main():

    st.set_page_config(layout='wide')

    # Read saved bracket data from csv
    entries_data = pd.read_csv('output/2024_entries_data.csv', index_col='name')

    # Remove the "actual" entry if already added
    entries_data.drop('actual', inplace = True)

    superbowl_picks = build_superbowl_picks_df(entries_data)

    superbowl_appears = build_superbowl_appears_df(entries_data)

    superbowl_picks_fig = px.bar(superbowl_picks, x='count', y='superbowl-winner', text='percent', color='superbowl-winner'
                 ,title='Super Bowl Winners', orientation='h')
    
    superbowl_appears_fig = px.bar(superbowl_appears, x='count', y='superbowl-teams', text='percent', color='superbowl-teams'
                 ,title='Super Bowl Team Appearances', orientation='h')    

    superbowl_picks_fig.update_layout(showlegend=False)
    superbowl_appears_fig.update_layout(showlegend=False)


    
    tab_sb, tab_conf, tab_div, tab_wc = st.tabs(['Superbowl', 'Conference', 'Divisional', 'Wild Card'])

    with tab_sb:
        col1, col2 = st.columns(2)
        col1.plotly_chart(superbowl_picks_fig, use_container_width=True, )
        col2.plotly_chart(superbowl_appears_fig, use_container_width=True, showlegend=False)

    tab_conf.write('comming soon')


if __name__ == '__main__':
    main()
# https://docs.google.com/spreadsheets/d/10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko/edit?usp=sharing
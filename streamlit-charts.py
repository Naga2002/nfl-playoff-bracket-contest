import pandas as pd
import streamlit as st
import plotly.express as px

def group_counts_percent(input_df, column_name):
    """
    input_df: original dataframe with data to be aggregated
    column_name: the column in input_df to use for grouping

    returns: df - will have orignal column_name count, and percent fields
    """
    # group by input column and set count as result
    df = input_df.groupby([column_name])[column_name].count().reset_index(name='count')
    # calculate precent of total
    total_entries=df['count'].sum()
    df['percent'] = df['count'] / total_entries * 100
    # round and sort
    df = df.round({'percent': 2}).sort_values(by=['count',column_name], ascending=False)

    # convert percent to string and add '%' symbol for displaying
    df['percent'] = df['percent'].astype(str) + '%'

    return df


def build_superbowl_picks_df(entries_data):
    # get counts of teams selected as superbowl-winners
    return group_counts_percent(entries_data, 'superbowl-winner')

def build_superbowl_appears_df(entries_data):
    # Concat series of both column values
    series1 = entries_data['superbowl-team_1']
    series2 = entries_data['superbowl-team_2']
    unioned_df = pd.concat([series1, series2]).to_frame(name = 'superbowl-teams')

    return group_counts_percent(unioned_df, 'superbowl-teams')    

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

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
    # Concat series of column values
    series1 = entries_data['superbowl-team_1']
    series2 = entries_data['superbowl-team_2']
    unioned_df = pd.concat([series1, series2]).to_frame(name = 'superbowl-teams')

    return group_counts_percent(unioned_df, 'superbowl-teams')

def build_conference_picks_df(entries_data):
    # Concat series of column values
    series1 = entries_data['conference1-winner']
    series2 = entries_data['conference2-winner']
    unioned_df = pd.concat([series1, series2]).to_frame(name = 'conference-winners')     

    return group_counts_percent(unioned_df, 'conference-winners')   

def build_conference_appears_df(entries_data):
    # Concat series of column values
    series1 = entries_data['conference1-team_1']
    series2 = entries_data['conference1-team_2']
    series3 = entries_data['conference2-team_1']
    series4 = entries_data['conference2-team_2']        
    unioned_df = pd.concat([series1, series2, series3, series4]).to_frame(name = 'conference-teams')     

    return group_counts_percent(unioned_df, 'conference-teams')   

def build_figure(input_df, title, y_name, nfl_team_colors):
    fig = px.bar(input_df, x='count', y=y_name, text='percent', color=y_name
                 ,title=title, orientation='h', color_discrete_map=nfl_team_colors)

    fig.update_layout(showlegend=False)

    return fig        

def main():

    st.set_page_config(layout='wide')

    # Read saved bracket data from csv
    entries_data = pd.read_csv('output/2024_entries_data.csv', index_col='name')

    # Remove the "actual" entry if already added
    entries_data.drop('actual', inplace = True)

    nfl_team_colors  = {
            'Arizona Cardinals': '#8B0021',
            'Atlanta Falcons': '#A71930',
            'Baltimore Ravens': '#241773',
            'Buffalo Bills': '#00338D',
            'Carolina Panthers': '#0085CA',
            'Chicago Bears': '#0B162A',
            'Cincinnati Bengals': '#FB4F14',
            'Cleveland Browns': '#311D00',
            'Dallas Cowboys': '#FFFFFF',
            'Denver Broncos': '#002244',
            'Detroit Lions': '#0076B6',
            'Green Bay Packers': '#203731',
            'Houston Texans': '#03202F',
            'Indianapolis Colts': '#002C5F',
            'Jacksonville Jaguars': '#006778',
            'Kansas City Chiefs': '#E31837',
            'Las Vegas Raiders': '#000000',
            'Los Angeles Chargers': '#002A5E',
            'Los Angeles Rams': '#002244',
            'Miami Dolphins': '#008E97',
            'Minnesota Vikings': '#4F2683',
            'New England Patriots': '#002244',
            'New Orleans Saints': '#D3BC8D',
            'New York Giants': '#0B2265',
            'New York Jets': '#125740',
            'Philadelphia Eagles': '#004C54',
            'Pittsburgh Steelers': '#FFB612',
            'San Francisco 49ers': '#B3995D',
            'Seattle Seahawks': '#002244',
            'Tampa Bay Buccaneers': '#D50A0A',
            'Tennessee Titans': '#4B92DB',
            'Washington Commanders': '#773141'
            }

    # build each graph dataframe
    superbowl_picks = build_superbowl_picks_df(entries_data)
    superbowl_appears = build_superbowl_appears_df(entries_data)
    conference_picks = build_conference_picks_df(entries_data)
    conference_appears = build_conference_appears_df(entries_data)

    # build each plottly figure
    superbowl_picks_fig = build_figure(superbowl_picks, 'Super Bowl Winners', 'superbowl-winner', nfl_team_colors)
    superbowl_appears_fig = build_figure(superbowl_appears, 'Super Bowl Team Appearances', 'superbowl-teams', nfl_team_colors)
    conference_picks_fig = build_figure(conference_picks, 'Conference Winners', 'conference-winners', nfl_team_colors)
    conference_appears_fig = build_figure(conference_appears, 'Conference Team Appearances', 'conference-teams', nfl_team_colors)

    # set tabs for streamlit   
    tab_sb, tab_conf, tab_div, tab_wc = st.tabs(['Superbowl', 'Conference', 'Divisional', 'Wild Card'])

    # build graphs in columns on each tab
    with tab_sb:
        col1, col2 = st.columns(2)
        col1.plotly_chart(superbowl_picks_fig, use_container_width=True, )
        col2.plotly_chart(superbowl_appears_fig, use_container_width=True, showlegend=False)

    with tab_conf:
        col1, col2 = st.columns(2)
        col1.plotly_chart(conference_picks_fig, use_container_width=True, )
        col2.plotly_chart(conference_appears_fig, use_container_width=True, showlegend=False)


if __name__ == '__main__':
    main()

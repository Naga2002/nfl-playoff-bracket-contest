import pandas as pd
import re

def read_entries_sheet():
    """ reads Google sheet that has links to other Google sheets - each one an entry bracket """
    sheet_id = '10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko'
    sheet_name = 'Entries'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)

    index = 0
    while index <= len(df)-1:
        """ loop through each entry and go the bracket link to retrieve bracket data """
        entry_row = df.iloc[index]
        entry_name = entry_row['email_address']
        sheet_link = entry_row['sheet_link']
        sheet_id = re.search(r'\/d\/([^\/]*)', sheet_link).group(1)
        sheet_name = 'Data'

        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        df2 = pd.read_csv(url)
        bracket_row = df2.iloc[0]

        print(bracket_row['wildcard1-team_1'], bracket_row['wildcard1-winner'], bracket_row['tie_breaker_points'])


        index += 1

def main():
    read_entries_sheet()

if __name__ == '__main__':
    main()
# https://docs.google.com/spreadsheets/d/10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko/edit?usp=sharing
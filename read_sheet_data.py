import pandas as pd
import re

#https://docs.google.com/spreadsheets/d/1KBk8eBUA5bfnOLxF20X9eS1xIqjAsSFF6xWuv2oTAas/edit?usp=sharing
def read_entries_sheet():
    """ reads Google sheet that has links to other Google sheets - each one an entry bracket """
    # sheet_id = '10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko'
    sheet_id = '1KBk8eBUA5bfnOLxF20X9eS1xIqjAsSFF6xWuv2oTAas'
    sheet_name = 'Entries'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)

    final_entries_df = pd.DataFrame([])
    index = 0
    while index <= len(df)-1:
        # loop through each entry and go the bracket link to retrieve bracket data
        entry_row = df.iloc[index]
        entry_name = entry_row['email_address']
        sheet_link = entry_row['sheet_link']
        sheet_id = re.search(r'\/d\/([^\/]*)', sheet_link).group(1)
        sheet_name = 'Data'

        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        single_entry_df = pd.read_csv(url)
        # bracket_row = df2.iloc[0]

        # print(bracket_row['email_address'], bracket_row['wildcard1-winner'], bracket_row['tie_breaker_points'])
        final_entries_df = pd.concat([final_entries_df, single_entry_df])

        index += 1
    
    print(final_entries_df)
    return final_entries_df

def main():
    # Read Google sheets of entry data
    entries_data = read_entries_sheet()
    # save to csv for easier reuse
    entries_data.to_csv('output/2024_entries_data.csv')

    
if __name__ == '__main__':
    main()
# https://docs.google.com/spreadsheets/d/10AsqEXEEziW_oCshbEcBQJ0OEVOTigsGmWlPk59T7Ko/edit?usp=sharing
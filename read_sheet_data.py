import pandas as pd
import re

# 2025-26 entries:
#https://docs.google.com/spreadsheets/d/1NGZYnFrHBeyj6UKEaupuUIvWUedGlPDw9zskHzQMrlQ/edit?usp=sharing
def read_entries_sheet():
    """ reads Google sheet that has links to other Google sheets - each one an entry bracket """

    sheet_id = '1NGZYnFrHBeyj6UKEaupuUIvWUedGlPDw9zskHzQMrlQ'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0'
    print("Reading entries sheet...")
    try:
        df = pd.read_csv(url)
        print(f"Successfully read {len(df)} rows")
        # print(df.head())
    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")

    final_entries_df = pd.DataFrame([])
    index = 0
    while index <= len(df)-1:
        # loop through each entry and go the bracket link to retrieve bracket data
        entry_row = df.iloc[index]
        entry_name = entry_row['email_address']
        sheet_link = entry_row['sheet_link']
        sheet_id = re.search(r'\/d\/([^\/]*)', sheet_link).group(1)
        gid = 2008579852 # this may change each year, but 2026 was this value for all entries
        print(entry_name, sheet_id)

        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
        single_entry_df = pd.read_csv(url)
        bracket_row = single_entry_df.iloc[0]

        print(bracket_row['name'], bracket_row['wildcard1-winner'], bracket_row['tie_breaker_points'])
        final_entries_df = pd.concat([final_entries_df, single_entry_df])

        index += 1
    
    print(final_entries_df)
    return final_entries_df

def main():
    # Read Google sheets of entry data
    entries_data = read_entries_sheet()
    # save to csv for easier reuse
    entries_data.to_csv('output/2026_entries_data.csv')

    
if __name__ == '__main__':
    main()

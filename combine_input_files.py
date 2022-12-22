from csv import reader
import json


with open('/Users/nathanmott/workspaces/nmott/nfl-playoff-bracket-contest/input/contest_form_data.csv',
          newline='') as form_data_file:
    csv_read = reader(form_data_file)
    tmp_list = list(csv_read)

# use two lists to keep track of fields in csv file with header info
header = tmp_list[0]
form_data = tmp_list[1:]

with open('/Users/nathanmott/workspaces/nmott/nfl-playoff-bracket-contest/input/wild_card_matchups.json') \
        as wild_card_file:
    wild_card_data = json.load(wild_card_file)

# unpack the json contents into a single dictionary
wild_card_dict = {}
for game in wild_card_data['wild_card_games']:
    # combining dictionaries into one
    wild_card_dict.update(game)

# print(wild_card_dict['Wild Card 2'])

json_data = {}

for row in form_data:
    bracket_entry = {}
    entryname = row[1]
    index = 2
    previous_matchup_name = ''
    print(entryname)

    while index < len(row):
        header_split = header[index].split(' - ')
        matchup_name = header_split[0]  # e.g. 'Wild Card 1'
        value_type = header_split[1]  # e.g. 'Winner Selection'

        # if matchup is a wild card, only the winner selection is in form data
        # get the matchup details from wild_card_data
        if matchup_name in wild_card_dict:
            matchup = {matchup_name: 'placeholder'}
            matchup_list_values = wild_card_dict[matchup_name]

        elif matchup_name != previous_matchup_name:
            matchup = {matchup_name: 'placeholder'}
            matchup_list_values = []
            previous_matchup_name = matchup_name

            # strip off trailing space and digit to get generic matchuptype
            # matchuptype = matchup_name[:-2]
            matchuptype = {'matchuptype': matchup_name[:-2]}

            if matchuptype not in matchup_list_values:
                matchup_list_values.append(matchuptype)

        if value_type.strip() == 'Team 1':
            awayteam = eval("{'awayteam':'" + row[index] + "'}")
            matchup_list_values.append(awayteam)

        if value_type.strip() == 'Team 2':
            hometeam = eval("{'hometeam':'" + row[index] + "'}")
            matchup_list_values.append(hometeam)

        if value_type.strip() == 'Winner Selection':
            winningteam = eval("{'winningteam':'" + row[index] + "'}")
            matchup_list_values.append(winningteam)

        # print(matchup_name)
        # print(matchup_list_values)
        bracket_entry[matchup_name] = matchup_list_values
        index += 1

    print(bracket_entry)
from csv import reader


with open('/Users/nathanmott/workspaces/nmott/nfl-playoff-bracket-contest/input/contest_form_data.csv',
          newline='') as form_data_file:
    csv_read = reader(form_data_file)
    tmp_list = list(csv_read)

header = tmp_list[0]
form_data = tmp_list[1:]

json_data = {}

for row in form_data:
    bracket_entry = {}
    entryname = row[1]
    index = 2
    previous_matchup_name = ''
    print(entryname)

    while index < len(row):
        header_split = header[index].split(' - ')
        matchup_name = header_split[0]
        value_type = header_split[1]
        # print(value_type)
        if matchup_name != previous_matchup_name:
            matchup = {matchup_name: 'placeholder'}
            matchup_list_values = []
            previous_matchup_name = matchup_name

        if matchup_name.startswith('Divisional 1') :
            matchuptype_string = "{'matchuptype':'Divisional'}"
            matchuptype = eval(matchuptype_string)
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

            print(matchup_list_values)
        index += 1

"""Module for entering and scoring NFL Playoff Brackets"""
import pandas as pd
import re

class Bracket:
    """A bracket entry that has a list of matchup picks"""

    def __init__(self, entryname, tiebreaker, matchups):
        self._entryname = entryname
        self._tiebreaker = tiebreaker # integer
        self._matchups = matchups # dictionary with key as matchup type, value is matchup object
        self._totalpoints = 0

    def __str__(self):
        return '{0}: {1}'.format(self._entryname, self._totalpoints)

    def entry_name(self):
        return self._entryname

    def tie_breaker(self):
        return self._tiebreaker

    def matchups(self):
        return self._matchups

    def total_points(self):
        return self._totalpoints

    def add_point_value(self, point_value):
        self._totalpoints += point_value
        return self._totalpoints

    def entry_html_rows(self):
        row1 = """
        <tr>
        <th>{0}</th><th>{1}</th><td>{2}</td>{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}
        </tr>""".format(self._entryname, self._totalpoints, self._tiebreaker,
                        self._matchups["WildCard 1"].away_team_html(),
                        self._matchups["WildCard 1"].home_team_html(), self._matchups["WildCard 1"].point_value(),
                        self._matchups["Divisional 1"].away_team_html(),
                        self._matchups["Divisional 1"].home_team_html(),
                        self._matchups["Divisional 1"].point_value(), self._matchups["Conference 1"].away_team_html(),
                        self._matchups["Conference 1"].home_team_html(), self._matchups["Conference 1"].point_value(),
                        self._matchups["Super Bowl"].away_team_html(), self._matchups["Super Bowl"].home_team_html(),
                        self._matchups["Super Bowl"].point_value()
                        )
        row2 = """
                <tr>
                <td></td><td></td><td></td>{0}{1}{2}{3}{4}{5}{6}{7}{8}<td></td><td></td><td></td>
                </tr>""".format(self._matchups["WildCard 2"].away_team_html(),
                                self._matchups["WildCard 2"].home_team_html(),
                                self._matchups["WildCard 2"].point_value(),
                                self._matchups["Divisional 2"].away_team_html(),
                                self._matchups["Divisional 2"].home_team_html(),
                                self._matchups["Divisional 2"].point_value(),
                                self._matchups["Conference 2"].away_team_html(),
                                self._matchups["Conference 2"].home_team_html(),
                                self._matchups["Conference 2"].point_value(),
                                )
        row3 = """
                <tr>
                <td></td><td></td><td></td>{0}{1}{2}{3}{4}{5}<td></td><td></td><td></td><td></td><td></td><td></td>
                </tr>""".format(self._matchups["WildCard 3"].away_team_html(),
                                self._matchups["WildCard 3"].home_team_html(),
                                self._matchups["WildCard 3"].point_value(),
                                self._matchups["Divisional 3"].away_team_html(),
                                self._matchups["Divisional 3"].home_team_html(),
                                self._matchups["Divisional 3"].point_value(),
                                )
        row4 = """
                <tr>
                <td></td><td></td><td></td>{0}{1}{2}{3}{4}{5}<td></td><td></td><td></td><td></td><td></td><td></td>
                </tr>""".format(self._matchups["WildCard 4"].away_team_html(),
                                self._matchups["WildCard 4"].home_team_html(),
                                self._matchups["WildCard 4"].point_value(),
                                self._matchups["Divisional 4"].away_team_html(),
                                self._matchups["Divisional 4"].home_team_html(),
                                self._matchups["Divisional 4"].point_value(),
                                )
        row5 = """
                <tr>
                <td></td><td></td><td></td>{0}{1}{2}<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                </tr>""".format(self._matchups["WildCard 5"].away_team_html(),
                                self._matchups["WildCard 5"].home_team_html(),
                                self._matchups["WildCard 5"].point_value(),
                                )
        row6 = """
                <tr>
                <td></td><td></td><td></td>{0}{1}{2}<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
                </tr>""".format(self._matchups["WildCard 6"].away_team_html(),
                                self._matchups["WildCard 6"].home_team_html(),
                                self._matchups["WildCard 6"].point_value(),
                                )

        return row1 + row2 + row3 + row4 + row5 + row6


class Matchup:
    """A game played between two NFL teams"""
    def __init__(self, matchuptype, awayteam, hometeam, winningteam, altwinningteam):
        self._matchuptype = str(matchuptype)
        self._awayteam = str(awayteam)
        self._hometeam = str(hometeam)
        self._winningteam = str(winningteam)
        self._altwinningteam = str(altwinningteam)
        self._pointvalue = 0
        self._matchuppoints = 0
        self._winningteampoints = 0
        self._matchupscoredYN = 'N'
        self._winningscoredYN = 'N'

    def away_team(self):
        return self._awayteam

    def home_team(self):
        return self._hometeam

    def winning_team(self):
        return self._winningteam

    def alt_winning_team(self):
        return self._altwinningteam

    def point_value(self):
        return '<td>' + str(self._pointvalue) + '</td>'

    def set_matchup_scored_y(self):
        self._matchupscoredYN = 'Y'

    def set_winning_scored_y(self):
        self._winningscoredYN = 'Y'

    def add_matchup_point_value(self, point_value):
        """Returns 0 if no points were added. Returns 1 if _pointvalue was increased"""
        if self._matchuptype == 'WildCard':
            return 0

        if self._matchuppoints == 0:
            self._matchuppoints += point_value

        if self._pointvalue < 2:
            self._pointvalue += point_value
            return 1

        return 0

    def add_winning_point_value(self, point_value):
        """Returns 0 if no points were added. Returns 1 if _pointvalue was increased"""
        if self._winningteampoints == 0:
            self._winningteampoints += point_value

        if self._pointvalue < 2:
            self._pointvalue += point_value
            return 1

        return 0

    def away_team_html(self):
        opentag = ''
        closetag = ''
        if self._matchupscoredYN == 'Y':
            if self._matchuppoints > 0:
                opentag += '<td bgcolor="#b3ffb3">'
            else:
                opentag += '<td bgcolor="#ffb3b3">'
        else:
            opentag += '<td>'

        if self._awayteam == self._winningteam:
            opentag += '<b><u>'
            closetag = closetag + '</u></b>'

            if self._winningscoredYN == 'Y':
                if self._winningteampoints > 0:
                    opentag += '<font color="#006600">'
                else:
                    opentag += '<font color="#cc0000">'

                closetag = '</font>' + closetag

        closetag = closetag + '</td>'

        return opentag + self._awayteam + closetag

    def home_team_html(self):
        opentag = ''
        closetag = ''
        if self._matchupscoredYN == 'Y':
            if self._matchuppoints > 0:
                opentag += '<td bgcolor="#b3ffb3">'
            else:
                opentag += '<td bgcolor="#ffb3b3">'
        else:
            opentag += '<td>'

        if self._hometeam == self._winningteam:
            opentag += '<b><u>'
            closetag = closetag + '</u></b>'

            if self._winningscoredYN == 'Y':
                if self._winningteampoints > 0:
                    opentag += '<font color="#006600">'
                else:
                    opentag += '<font color="#cc0000">'

                closetag = '</font>' + closetag

        closetag = closetag + '</td>'

        return opentag + self._hometeam + closetag


def print_entries(entries_list):
    """Simple console print of entries for easy debugging"""
    for entry in entries_list:
        print(entry)


def write_html_entries(entries_list):
    """Writs out an html file for displaying brackets and scores"""
    html_header = """<!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>NFL Playoff Bracket</title>
        <style>
        html {
          font-family: sans-serif;
        }
        table {
          border-collapse: collapse;
          border: 2px solid rgb(200,200,200);
          letter-spacing: 1px;
          font-size: 0.8rem;
        }
        td, th {
          border: 1px solid rgb(190,190,190);
          padding: 4px 16px;
        }
        td {
          text-align: center;
        }
        caption {
          padding: 10px;
        }
        </style>
      </head>
      <body>
     <table border=1>
          <tr>
          <th>Name</th><th>Final Points</th><th>Tiebrk</th><th colspan="2">WildCard Matchups</th><th>Pts</th>
          <th colspan="2">Divisional Matchups</th><th>Pts</th><th colspan="2">Conference Matchups</th><th>Pts</th>
          <th colspan="2">Super Bowl</th><th>Pts</th>         
          </tr>"""
    html_rows = ''
    html_footer = """</table>
                 </body>
                </html>"""

    entries_list = sorted(entries_list, key=lambda bracket: -bracket.total_points())  # sort by total points desc

    for entry in entries_list:
        html_rows += entry.entry_html_rows()

    with open(r'/Users/nathanmott/workspaces/nmott/nfl-playoff-bracket-contest/docs/index.html',
    # with open(r'/Users/nathanmott/Documents/NFL  Playoff Brackets/NFL_Brackets_22-23-scoringtest.html',
              mode='wt', encoding='utf-8') as wf:
        wf.write(html_header)
        wf.write(html_rows)
        wf.write(html_footer)


def score_entries(actual_entry, entries_list):
    """Calculates the scores of each entry in the list against the actual entry

    Args:
        actual_entry: The single Bracket object that represents the actual scores
        entries_list: A list of Bracket objects that have the entry info
    """
    # extract the dictionary of actual matchups
    actual_matchups = actual_entry.matchups()

    # for each matchup_type (dictionary key) in actual, compare to full list of entries comparing where matchup_types
    # are the same
    for matchup_type in actual_matchups:
        # entry is a Bracket object
        for entry in entries_list:
            # entry.matchups() returns a dictionary and we seek the exact matchup by key: matchup_type
            entry_matchup = entry.matchups()[matchup_type]
            actual_matchup = actual_matchups[matchup_type]

            if actual_matchup.winning_team() != 'nan':
                entry_matchup.set_winning_scored_y()

            if (entry_matchup.winning_team() == actual_matchup.winning_team() or \
                    entry_matchup.winning_team() == actual_matchup.alt_winning_team()) \
                    and actual_matchup.winning_team() != 'nan':
                bool_point_increased = entry_matchup.add_winning_point_value(1)
                if bool_point_increased == 1:
                    entry.add_point_value(1)

            if not matchup_type.startswith("WildCard"):
                if actual_matchup.away_team() != 'nan':
                    entry_matchup.set_matchup_scored_y()

                entry_team_list = [entry_matchup.away_team(), entry_matchup.home_team()]
                actual_team_list = [actual_matchup.away_team(), actual_matchup.home_team()]

                if sorted(entry_team_list) == sorted(actual_team_list):
                    bool_point_increased = entry_matchup.add_matchup_point_value(1)
                    if bool_point_increased == 1:
                        entry.add_point_value(1)


def create_bracket_from_sheet(bracket_row):
    """ Takes a pandas Series object and returns a Bracket object
    """
    # build the matchups dictionary first
    matchups = {}
    matchups['WildCard 1'] = Matchup('WildCard', bracket_row['wildcard1-team_1'], bracket_row['wildcard1-team_2'],
                                     bracket_row['wildcard1-winner'], 'x')
    matchups['WildCard 2'] = Matchup('WildCard', bracket_row['wildcard2-team_1'], bracket_row['wildcard2-team_2'],
                                     bracket_row['wildcard2-winner'], 'x')
    matchups['WildCard 3'] = Matchup('WildCard', bracket_row['wildcard3-team_1'], bracket_row['wildcard3-team_2'],
                                     bracket_row['wildcard3-winner'], 'x')
    matchups['WildCard 4'] = Matchup('WildCard', bracket_row['wildcard4-team_1'], bracket_row['wildcard4-team_2'],
                                     bracket_row['wildcard4-winner'], 'x')
    matchups['WildCard 5'] = Matchup('WildCard', bracket_row['wildcard5-team_1'], bracket_row['wildcard5-team_2'],
                                     bracket_row['wildcard5-winner'], 'x')
    matchups['WildCard 6'] = Matchup('WildCard', bracket_row['wildcard6-team_1'], bracket_row['wildcard6-team_2'],
                                     bracket_row['wildcard6-winner'], 'x')
    matchups['Divisional 1'] = Matchup('Divisional', bracket_row['divisional1-team_1'], bracket_row['divisional1-team_2'],
                                     bracket_row['divisional1-winner'], 'x')
    matchups['Divisional 2'] = Matchup('Divisional', bracket_row['divisional2-team_1'], bracket_row['divisional2-team_2'],
                                     bracket_row['divisional2-winner'], 'x')
    matchups['Divisional 3'] = Matchup('Divisional', bracket_row['divisional3-team_1'], bracket_row['divisional3-team_2'],
                                     bracket_row['divisional3-winner'], 'x')
    matchups['Divisional 4'] = Matchup('Divisional', bracket_row['divisional4-team_1'], bracket_row['divisional4-team_2'],
                                     bracket_row['divisional4-winner'], 'x')
    matchups['Conference 1'] = Matchup('Conference', bracket_row['conference1-team_1'], bracket_row['conference1-team_2'],
                                     bracket_row['conference1-winner'], 'x')
    matchups['Conference 2'] = Matchup('Conference', bracket_row['conference2-team_1'], bracket_row['conference2-team_2'],
                                     bracket_row['conference2-winner'], 'x')
    matchups['Super Bowl'] = Matchup('Super Bowl', bracket_row['superbowl-team_1'], bracket_row['superbowl-team_2'],
                                     bracket_row['superbowl-winner'], 'x')

    bracket = Bracket(bracket_row['email_address'],bracket_row['tie_breaker_points'], matchups)
    return bracket


def read_entries_sheet():
    """ reads Google sheet that has links to other Google sheets - each one an entry bracket

        Returns a list of entry brackets
    """
    entries = []
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

        bracket = create_bracket_from_sheet(bracket_row)
        entries.append(bracket)

        index += 1

    return entries

def get_actual():
    """ reads Google sheet that is my "actual bracket" - updated after game outcomes each round

        Returns a single bracket named "actual"
    """
    sheet_id = '17yVLdSgMs2fKbTOeq6XwSki29J4T6cD431UWVAvhnws'
    sheet_name = 'Data'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    bracket_row = df.iloc[0]

    matchups = {}
    matchups['WildCard 1'] = Matchup('WildCard', bracket_row['wildcard1-team_1'], bracket_row['wildcard1-team_2'],
                                     bracket_row['wildcard1-winner'], 'x')
    matchups['WildCard 2'] = Matchup('WildCard', bracket_row['wildcard2-team_1'], bracket_row['wildcard2-team_2'],
                                     bracket_row['wildcard2-winner'], 'x')
    matchups['WildCard 3'] = Matchup('WildCard', bracket_row['wildcard3-team_1'], bracket_row['wildcard3-team_2'],
                                     bracket_row['wildcard3-winner'], 'x')
    matchups['WildCard 4'] = Matchup('WildCard', bracket_row['wildcard4-team_1'], bracket_row['wildcard4-team_2'],
                                     bracket_row['wildcard4-winner'], 'x')
    matchups['WildCard 5'] = Matchup('WildCard', bracket_row['wildcard5-team_1'], bracket_row['wildcard5-team_2'],
                                     bracket_row['wildcard5-winner'], 'x')
    matchups['WildCard 6'] = Matchup('WildCard', bracket_row['wildcard6-team_1'], bracket_row['wildcard6-team_2'],
                                     bracket_row['wildcard6-winner'], 'x')
    matchups['Divisional 1'] = Matchup('Divisional', bracket_row['divisional1-team_1'], bracket_row['divisional1-team_2'],
                                     bracket_row['divisional1-winner'], bracket_row['divisional2-winner'])
    matchups['Divisional 2'] = Matchup('Divisional', bracket_row['divisional2-team_1'], bracket_row['divisional2-team_2'],
                                     bracket_row['divisional2-winner'], bracket_row['divisional1-winner'])
    matchups['Divisional 3'] = Matchup('Divisional', bracket_row['divisional3-team_1'], bracket_row['divisional3-team_2'],
                                     bracket_row['divisional3-winner'], bracket_row['divisional4-winner'])
    matchups['Divisional 4'] = Matchup('Divisional', bracket_row['divisional4-team_1'], bracket_row['divisional4-team_2'],
                                     bracket_row['divisional4-winner'], bracket_row['divisional3-winner'])
    matchups['Conference 1'] = Matchup('Conference', bracket_row['conference1-team_1'], bracket_row['conference1-team_2'],
                                     bracket_row['conference1-winner'], bracket_row['conference2-winner'])
    matchups['Conference 2'] = Matchup('Conference', bracket_row['conference2-team_1'], bracket_row['conference2-team_2'],
                                     bracket_row['conference2-winner'], bracket_row['conference1-winner'])
    matchups['Super Bowl'] = Matchup('Super Bowl', bracket_row['superbowl-team_1'], bracket_row['superbowl-team_2'],
                                     bracket_row['superbowl-winner'], 'x')

    actual = Bracket(bracket_row['email_address'],bracket_row['tie_breaker_points'], matchups)

    return actual

def main():
    e = read_entries_sheet()
    a = get_actual()
    # print(a)
    score_entries(a, e)
    # print_entries(a)
    write_html_entries(e)


if __name__ == '__main__':
    main()

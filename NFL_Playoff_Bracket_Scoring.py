"""Module for entering and scoring NFL Playoff Brackets"""


class Bracket:
    """A bracket entry that has a list of matchup picks"""

    def __init__(self, entryname, tiebreaker, matchups):
        self._entryname = entryname
        self._tiebreaker = tiebreaker
        self._matchups = matchups
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
        return row1 + row2 + row3 + row4


class Matchup:
    """A game played between two NFL teams"""
    def __init__(self, matchuptype, awayteam, hometeam, winningteam, altwinningteam):
        self._matchuptype = matchuptype
        self._awayteam = awayteam
        self._hometeam = hometeam
        self._winningteam = winningteam
        self._altwinningteam = altwinningteam
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
          <th>Name</th><th>Final Points</th><th>Tie Brk</th><th colspan="2">WildCard Matchups</th><th>Pts</th>
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

    with open(r'V:\KMO\AAA for now\Personal_Area\Nate\Stuff\NFL Playoff Brackets\NFL_Brackets_2017.html',
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

            if actual_matchup.winning_team() != 'x':
                entry_matchup.set_winning_scored_y()

            if entry_matchup.winning_team() == actual_matchup.winning_team() or \
                    entry_matchup.winning_team() == actual_matchup.alt_winning_team():
                bool_point_increased = entry_matchup.add_winning_point_value(1)
                if bool_point_increased == 1:
                    entry.add_point_value(1)

            if not matchup_type.startswith("WildCard"):
                if actual_matchup.away_team() != 'x':
                    entry_matchup.set_matchup_scored_y()

                entry_team_list = [entry_matchup.away_team(), entry_matchup.home_team()]
                actual_team_list = [actual_matchup.away_team(), actual_matchup.home_team()]

                if sorted(entry_team_list) == sorted(actual_team_list):
                    bool_point_increased = entry_matchup.add_matchup_point_value(1)
                    if bool_point_increased == 1:
                        entry.add_point_value(1)


def create_entries():
    # to make full color tracking - need to pass Matchup type as a param to Matchup()
    actual = Bracket('Actual', 0,
                     {"WildCard 1": Matchup('WildCard', 'Colts', 'Texans', 'Colts', 'x'),
                      "WildCard 2": Matchup('WildCard', 'Chargers', 'Ravens', 'Ravens', 'x'),
                      "WildCard 3": Matchup('WildCard', 'Vikings', 'Bears', 'Bears', 'x'),
                      "WildCard 4": Matchup('WildCard', 'Seahawks', 'Cowboys', 'Seahawks', 'x'),
                      "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'Jaguars'),
                      "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'Patriots'),
                      "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'Vikings'),
                      "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Vikings', 'Eagles'),
                      "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                      "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Eagles', 'x'),
                      "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Eagles', 'Eagles', 'x'), }
                     )

    entries_list = [
        Bracket('Actual', 74,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Eagles', 'Eagles', 'x'), }
                ),
        Bracket('Nathan Mott', 37,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Jaguars', 'x'),
                 "Conference 2": Matchup('Conference', 'Falcons', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Jaguars', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Ashley Mott', 52,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Bills', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Bills', 'Steelers', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Rams', 'Eagles', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Rams', 'Rams', 'x'), }
                ),
        Bracket('Vishu', 41,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Bills', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Panthers', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Jo Pugliese', 37,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Eagles', 'Patriots', 'x'), }
                ),
        Bracket('Jo Pugliese (M)', 45,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Chiefs', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Chiefs', 'Steelers', 'Chiefs', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Chiefs', 'Eagles', 'Eagles', 'x'), }
                ),
        Bracket('Jo Pugliese (3)', 49,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Lisa Maye', 52,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Falcons', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Cannon Maye', 41,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Vikings', 'Patriots', 'x'), }
                ),
        Bracket('Chase Maye', 60,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Panthers', 'Eagles', 'Panthers', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Vikings', 'Panthers', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Panthers', 'Panthers', 'x'), }
                ),
        Bracket('Marc Maye', 48,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Panthers', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Falcons', 'Falcons', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Falcons', 'Patriots', 'x'), }
                ),
        Bracket('Amanda Ambrose', 53,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Chiefs', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Saints', 'Saints', 'x'), }
                ),
        Bracket('Brandon Ambrose', 52,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Brandon Ambrose (2)', 45,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Bills', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Titans', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Panthers', 'x'),
                 "Conference 1": Matchup('Conference', 'Bills', 'Titans', 'Bills', 'x'),
                 "Conference 2": Matchup('Conference', 'Falcons', 'Panthers', 'Falcons', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Bills', 'Falcons', 'Bills', 'x'), }
                ),
        Bracket('Becky Grim', 42,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Eagles', 'Steelers', 'x'), }
                ),
        Bracket('Missi Miller', 36,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Rams', 'Patriots', 'x'), }
                ),
        Bracket('Kayla', 42,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Rams', 'Steelers', 'x'), }
                ),
        Bracket('Kayla (2)', 42,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Eagles', 'Steelers', 'x'), }
                ),
        Bracket('Mark Randolph', 46,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Cameron Randolph', 45,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Saints', 'Saints', 'x'), }
                ),
        Bracket('Karlo', 68,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Karlo (2)', 72,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Chiefs', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Chiefs', 'Patriots', 'Chiefs', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Chiefs', 'Saints', 'Chiefs', 'x'), }
                ),
        Bracket('Joy Grubb', 44,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Rams', 'Steelers', 'x'), }
                ),
        Bracket('Aaron C', 66,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Rams', 'Patriots', 'x'), }
                ),
        Bracket('Jes Cornbower', 60,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Vikings', 'Patriots', 'x'), }
                ),
        Bracket('Heather Laskowich', 64,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Falcons', 'Saints', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Saints', 'Patriots', 'x'), }
                ),
        Bracket('Cindy Smith', 24,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Bills', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Bills', 'Patriots', 'Bills', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Panthers', 'Eagles', 'Panthers', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Bills', 'Steelers', 'Bills', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Rams', 'Steelers', 'x'), }
                ),
        Bracket('Cindy Smith (2)', 31,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Vikings', 'Steelers', 'x'), }
                ),
        Bracket('Terri Krebs', 53,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Rams', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Eagles', 'Patriots', 'x'), }
                ),
        Bracket('Brian Cook', 61,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Chiefs', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Saints', 'Steelers', 'x'), }
                ),
        Bracket('Mandy Cook', 49,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Titans', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Vikings', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Eagles', 'Steelers', 'x'), }
                ),
        Bracket('Stef Martin', 41,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Jaguars', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Panthers', 'Eagles', 'Panthers', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Vikings', 'Vikings', 'x'), }
                ),
        Bracket('Stef Martin (2)', 37,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Panthers', 'Eagles', 'Panthers', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Rams', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Rams', 'Rams', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', 'Rams', 'Patriots', 'x'), }
                ),
        Bracket('Kim R', 43,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Jaguars', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Rams', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Panthers', 'x'),
                 "Conference 1": Matchup('Conference', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Panthers', 'Eagles', 'Panthers', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Panthers', '', 'x'), }
                ),
        Bracket('Kim R (2)', 45,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', '', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Chiefs', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Rams', 'Eagles', 'Rams', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Chiefs', '', 'Chiefs', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Rams', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Chiefs', 'Saints', 'Chiefs', 'x'), }
                ),
        Bracket('Kim R (3)', 38,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Titans', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Panthers', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Titans', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Rams', 'Eagles', 'Rams', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Panthers', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Patriots', 'x'),
                 "Conference 2": Matchup('Conference', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Patriots', '', '', 'x'), }
                ),
        Bracket('Kim R (4)', 45,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Jaguars', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Chiefs', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Rams', 'Eagles', 'Eagles', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Eagles', 'Eagles', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Eagles', 'Eagles', 'x'), }
                ),
        Bracket('Jo Pugliese (4)', 47,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Rams', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Saints', 'Eagles', 'Saints', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Rams', 'Vikings', 'Vikings', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Saints', 'Steelers', 'x'), }
                ),
        Bracket('Klay', 59,
                {"WildCard 1": Matchup('WildCard', 'Bills', 'Jaguars', 'Jaguars', 'x'),
                 "WildCard 2": Matchup('WildCard', 'Titans', 'Chiefs', 'Chiefs', 'x'),
                 "WildCard 3": Matchup('WildCard', 'Falcons', 'Rams', 'Falcons', 'x'),
                 "WildCard 4": Matchup('WildCard', 'Panthers', 'Saints', 'Saints', 'x'),
                 "Divisional 1": Matchup('Divisional', 'Chiefs', 'Patriots', 'Patriots', 'x'),
                 "Divisional 2": Matchup('Divisional', 'Jaguars', 'Steelers', 'Steelers', 'x'),
                 "Divisional 3": Matchup('Divisional', 'Falcons', 'Eagles', 'Falcons', 'x'),
                 "Divisional 4": Matchup('Divisional', 'Saints', 'Vikings', 'Saints', 'x'),
                 "Conference 1": Matchup('Conference', 'Steelers', 'Patriots', 'Steelers', 'x'),
                 "Conference 2": Matchup('Conference', 'Falcons', 'Saints', 'Saints', 'x'),
                 "Super Bowl": Matchup('Super Bowl', 'Steelers', 'Saints', 'Steelers', 'x'), }
                ), ]

    return actual, entries_list


def main():
    a, e = create_entries()
    score_entries(a, e)
    # print_entries(e)
    write_html_entries(e)


if __name__ == '__main__':
    main()


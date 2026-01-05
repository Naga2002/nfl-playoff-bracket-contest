# NFL Playoff Bracket Contest - AI Coding Agent Instructions

## Project Overview
A dual-mode NFL playoff bracket contest system:
1. **Snowflake/Streamlit mode** ([streamlit_bracket_entry.py](streamlit_bracket_entry.py)): User-facing bracket entry form with Snowflake backend
2. **Google Sheets mode** ([read_sheet_data.py](read_sheet_data.py), [NFL_Playoff_Bracket_Scoring.py](NFL_Playoff_Bracket_Scoring.py)): Legacy system reading from Google Sheets, scoring brackets, and generating HTML results

## Core Architecture

### Data Model - Playoff Structure
Brackets follow NFL playoff bracket structure:
- **6 Wild Card games** (3 AFC, 3 NFC) - no points awarded for predicting matchups
- **4 Divisional games** (2 AFC, 2 NFC) - 1 point for correct matchup + 1 point for correct winner
- **2 Conference games** (AFC, NFC) - 1 point for correct matchup + 1 point for correct winner  
- **1 Super Bowl** - 1 point for correct matchup + 1 point for correct winner
- **Tiebreaker**: Total points in Super Bowl

### Column Naming Convention
All bracket data uses hyphenated format: `wildcard1-team_1`, `divisional2-winner`, `conference1-team_2`, `superbowl-winner`
- Exception: Snowflake schema uses underscores (`wildcard1_team_1`) due to SQL conventions

### Scoring Logic ([NFL_Playoff_Bracket_Scoring.py](NFL_Playoff_Bracket_Scoring.py))
- `Matchup` class handles individual game scoring with HTML coloring for visual feedback
  - Green (`#b3ffb3`/`#006600`): Correct prediction
  - Red (`#ffb3b3`/`#cc0000`): Incorrect prediction
- `Bracket` class aggregates all matchup scores for an entry
- `score_entries()` compares each entry against the "actual" bracket from Google Sheets
- Wild Card games only award points for correct winners (no matchup points since matchups are predetermined)

### Alternate Winners
Divisional and Conference matchups support alternate winners (e.g., if team A beats team B in divisional round, either could appear in conference championship). See `get_actual()` function where `altwinningteam` is populated from other divisional/conference winners.

## Data Sources

### Google Sheets Integration
- **Entry aggregation sheet**: Contains links to individual participant brackets (sheet ID: `1_XZxUFkZK9hHQkqHxR8uKzEr-mT4myxWlB4B0m2d8ME`)
- **Actual results sheet**: Updated with real game outcomes (sheet ID in `get_actual()`)
- URL pattern: `https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}`
- Data is cached to [output/2025_entries_data.csv](output/2025_entries_data.csv) for reuse

### Snowflake Integration
[streamlit_bracket_entry.py](streamlit_bracket_entry.py) uses:
- `snowflake.snowpark.context.get_active_session()` - assumes Snowflake environment (Snowsight UI)
- Table: `NFL_PLAYOFF_CONTEST.PROD.NFL_BRACKET_ENTRIES`
- Edit key system: password-protected entries for later modifications

## Key Workflows

### Running Visualizations
```bash
streamlit run streamlit-charts.py
```
Reads [output/2025_entries_data.csv](output/2025_entries_data.csv), generates bar charts showing:
- Super Bowl predictions and team appearances
- Conference/Divisional/Wild Card winner distributions
- Uses NFL team color palette for brand consistency

### Scoring Entries
```bash
python NFL_Playoff_Bracket_Scoring.py
```
1. Fetches entries from CSV (`read_entries_csv()`)
2. Fetches actual results from Google Sheets (`get_actual()`)
3. Scores each entry (`score_entries()`)
4. Outputs HTML to [docs/index.html](docs/index.html) with color-coded results

### Team Configuration
When updating for new season, modify `AFC_TEAMS` and `NFC_TEAMS` dictionaries in [streamlit_bracket_entry.py](streamlit_bracket_entry.py) with current playoff seeds.

## File Organization
- `archive/` - Previous years' results (HTML outputs and entry CSVs)
- `docs/` - Generated HTML results (GitHub Pages ready)
- `output/` - Current year's aggregated entry data

## Dependencies
Minimal stack: pandas, plotly, streamlit. Snowflake integration only needed for [streamlit_bracket_entry.py](streamlit_bracket_entry.py).


# General Code Guidelines Copilot Instructions

- Always verify information before presenting it. Do not make assumptions or speculate without clear evidence.
- Make changes file by file and allow for review of mistakes.
- Never use apologies or give feedback about understanding in comments or documentation.
- Don't suggest whitespace changes or summarize changes made.
- Only implement changes explicitly requested; do not invent changes.
- Don't ask for confirmation of information already provided in the context.
- Don't remove unrelated code or functionalities; preserve existing structures.
- Provide all edits in a single chunk per file, not in multiple steps.
- Don't ask the user to verify implementations visible in the provided context.
- Don't suggest updates or changes to files when there are no actual modifications needed.
- Always provide links to real files, not context-generated files.
- Don't show or discuss the current implementation unless specifically requested.
- Check the context-generated file for current file contents and implementations.
- Prefer descriptive, explicit variable names for readability.
- Adhere to the existing coding style in the project.
- Prioritize code performance and security in suggestions.
- Suggest or include unit tests for new or modified code.
- Implement robust error handling and logging where necessary.
- Encourage modular design for maintainability and reusability.
- Ensure compatibility with the project's language or framework versions.
- Replace hardcoded values with named constants.
- Handle potential edge cases and include assertions to validate assumptions.

# Python Developer Copilot Instructions

## Role & Expertise
- Be an elite software developer with expertise in Python, command-line tools, and file system operations.
- Excel at debugging complex issues and optimizing code performance.

## Code Style
- Always use classes instead of standalone functions for Python code.

## Dependency Management
- Always use UV for installing dependencies to ensure consistency and efficiency.

## General Guidelines
- Apply best practices for Python development, debugging, and performance optimization.
- Reference project technology stack and requirements as needed.
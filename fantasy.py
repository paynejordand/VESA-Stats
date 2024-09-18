import requests
import pandas as pd

api = "https://overstat.gg/api/stats/"
urlPrefix = 'https://overstat.gg/'
leagues = {
    "scrim": [8621],
}

player_stats = ['name', 'playerId', 
                'damageDealt','knockdowns', 'kills',
                'assists', 'revivesGiven', 'respawnsGiven']
team_stats = ['name', 'score', 'position']

for league, weeks in leagues.items():
    player_data = []
    team_data = []
    for week in weeks:
        overall = (requests.get(f"{api}{week}/overall")).json()
        for team in overall['teams']:
            team_data.append(team['overall_stats'])
            for player in team['player_stats']:
                player_data.append(player)

    team_df = pd.DataFrame.from_dict(team_data)
    team_df = team_df[team_stats]
    team_df['name'] = team_df['name'].replace(to_replace="(.+)@.+", value=r"\1", regex=True)
    team_df.to_csv(f"{league}_fantasy_teams.csv")

    player_df = pd.DataFrame.from_dict(player_data)
    player_df = player_df[player_stats]

    newindexes = []
    for index in player_df.index:
        pid = player_df.loc[[index]]['playerId'].values[0]
        newindexes.append(f"{urlPrefix}{pid}")
    player_df.index = newindexes
    player_df.index.name = "url"
    
    player_df.to_csv(f"{league}_fantasy_players.csv")
import requests
import pandas as pd

api = "https://overstat.gg/api/stats/"
urlPrefix = 'https://overstat.gg/'
leagues = {
    "Pinnacle": [7723, 7819, 7917, 8060, 8175],
    "Ascendant": [7722, 7815, 7930, 8022, 8174],
    "Emergent": [7721, 7814, 7929, 7999, 8173],
    "Challengers": [7618, 7793, 7889, 8039, 8176],
    "Tendies": [7719, 7762, 7875, 7952, 8172]
}
summed_stats = ['damageDealt','knockdowns', 
                'kills', 'assists', 
                'hits', 'shots', 
                'revivesGiven', 'respawnsGiven', 
                'score']
mean_stats = ['accuracy']

for league, weeks in leagues.items():
    player_data = []
    for week in weeks:
        overall = (requests.get(f"{api}{week}/overall")).json()
        for team in overall['teams']:
            for player in team['player_stats']:
                player_data.append(player)

    df = pd.DataFrame.from_dict(player_data)
    
    df_final = df.groupby('playerId')[summed_stats].sum()
    df_final[mean_stats] = df.groupby('playerId')[mean_stats].mean()
    df_final['name'] = df.groupby('playerId')['name'].last()
    df_final['Days Played'] = df.groupby('playerId')['name'].count()
    df_final = df_final.rename(columns={'damageDealt': 'damage',
                                        'knockdowns': 'downs',
                                        'revivesGiven': 'revives',
                                        'respawnsGiven': 'respawns'})
    
    df_final = df_final.assign(accuracy=round(df_final['hits']/df_final['shots'], 3))
    df_final = df_final.assign(kp = df_final['kills'] + df_final['assists'])
    
    cols = list(df_final.columns)
    name, dp, kp, acc, score = cols.index('name'), cols.index('Days Played'), cols.index('kp'), cols.index('accuracy'), cols.index('score')
    cols = cols[name::name] + cols[dp::dp] + cols[score::score] + cols[0:4] + cols[kp::kp] + cols[4:6] + cols[acc::acc] + cols[6:8]
    df_final = df_final[cols]
    
    newindexes = []
    for index in df_final.index:
        newindexes.append(f"{urlPrefix}{index}")
    df_final.index = newindexes
    df_final.index.name = "url"
    
    df_final.to_csv(f"{league}.csv")
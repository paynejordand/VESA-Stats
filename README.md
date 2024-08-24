Simple Python script to cURL multiple [Overstat](https://overstat.gg/) pages to gather cumulative player stats by their playerId.  

'leagues' is a dict where the key is the name of the league/series (this will  be the name of the output csv) and the values are the unique IDs for the match pages.  
e.g. for the VESA S7 Challengers Day 5 match page (overstat.gg/tournament/virtualesports/___8176___.VESA_S7_Challengers_8_20_2024/standings/overall/scoreboard) the unique ID is 8176.

A couple notes on the player name:
1) If a player changed their in-game name(IGN) it will select the most recently used IGN.
2) If a player played on different accounts it will list them separately

If Overstat ever gets some of their additional stat lines like damage taken working, this should be easy to update to include those.  
Confirmed to work with Python3.10 and Pandas 2.2.2

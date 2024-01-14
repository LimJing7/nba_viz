# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 10:26:34 2024

@author: Lim Jing
"""

from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

from nba_api.stats.endpoints import CommonPlayerInfo, GameRotation, LeagueGameLog, playbyplay
import utils

sns.set_theme()

team_id = 1610612744
game_id = '0022300536'

game_log_df = LeagueGameLog().get_data_frames()[0]
game_log_df = game_log_df[(game_log_df['GAME_ID'] == game_id) & (game_log_df['TEAM_ID'] == team_id)]
pbp_df = playbyplay.PlayByPlay(game_id).get_data_frames()[0]

rot_dfs = GameRotation(game_id).get_data_frames()
if rot_dfs[0]['TEAM_ID'].iloc[0] == team_id:
    rot_df = rot_dfs[0]
else:
    rot_df = rot_dfs[1]

players = {}

end_time = 0
for i, row in rot_df.iterrows():
    try:
        players[row['PERSON_ID']].add_on_off(row['IN_TIME_REAL']/600, row['OUT_TIME_REAL']/600)
    except KeyError:
        player_info = CommonPlayerInfo(row['PERSON_ID']).get_data_frames()[0]
        jersey = player_info['JERSEY'].iloc[0]
        name = player_info['DISPLAY_FIRST_LAST'].iloc[0]
        players[row['PERSON_ID']] = utils.Player(name, jersey)

        players[row['PERSON_ID']].add_on_off(row['IN_TIME_REAL']/600, row['OUT_TIME_REAL']/600)
    if row['OUT_TIME_REAL'] > end_time:
        end_time = row['OUT_TIME_REAL']

players_list = list(players.values())

players = sorted(players_list)
n_players = len(players)

fig = plt.figure()
ax = fig.add_axes([0.1,0.1,.9,.7])

ax.set_title(f'{game_log_df["MATCHUP"].iloc[0]}: On Off Plot')
ax.set_xlabel('Game Time')
ax.set_ylabel('Player')

cp = sns.color_palette("dark:#5A9_r", n_players)

lines = []
colors = []

# for pos, player in enumerate(players):
#     y_pos = (1 - pos/n_players)
#     color = cp[pos]
#     for on, off in player.on:
#         lines.append([(on, y_pos), (off, y_pos)])
#         colors.append(color)

# lc = matplotlib.collections.LineCollection(lines, colors=colors, linewidths=2)
# ax.add_collection(lc)

for pos, player in enumerate(players):
    y_pos = (1 - pos/n_players)
    color = cp[pos]

    x = np.arange(0, end_time/600, 1/600)
    y = np.array([y_pos]*int(end_time))
    mask = player.create_mask(x)
    ax.plot(mask, y, label=player.name, color=color)

ax.autoscale()
ax.margins(0.1)
ax.legend()

fig.savefig('plot.pdf')

from entities import *
from gpt_analysis import *
from constants import TEAMS_DATA, STAT_EFFECTS, POSSESSIONS_STD_DEV

import pickle
import numpy as np
import pandas as pd
from collections import Counter
from tqdm import tqdm, trange
from IPython.display import clear_output

with open(TEAMS_DATA, 'rb') as f:
    teams = pickle.load(f)

with open(STAT_EFFECTS, 'rb') as f:
    stats = pickle.load(f)

SCALED_STATS = ['2PA', '3PA', 'FTA', 'STL', 'BLK', 'TOV', 'PF', 'ORB', 'DRB']
UNSCALED_STATS = ['2P%', '3P%', 'FT%']
MODELED_STATS = ['BLK', 'STL', 'TOV', 'ORB', 'DRB', 'PF']

def get_starters(team: Team):
    starters = list(team.df['GS'].sort_values(ascending=False).iloc[:5].index)
    starters.sort()
    return starters


def get_random_players(team: Team):
    pct_played = team.df['MP'] / (team.games * 40)
    players = np.array(pct_played.index)
    weights = np.array(pct_played) / np.array(pct_played).sum()

    sampled_players = list(np.random.choice(players, size=5, replace=False, p=weights))
    sampled_players.sort()
    return sampled_players


def get_player_stats(player: str, team: Team):
    return team.df.loc[player]


def get_number_of_possessions(team_1: Team, team_2: Team):
    μ = np.mean([team_1.pace, team_2.pace])
    σ = POSSESSIONS_STD_DEV
    
    p = np.random.normal(loc=μ, scale=σ)
    j = np.random.uniform(low=-1, high=1, size=2)

    p1 = float(p + j[0])
    p2 = float(p + j[1])
    return p1, p2


def simulate_game(team_1: Team, team_2: Team):
    output = {}
    game_log = []
    
    possessions = get_number_of_possessions(team_1, team_2)

    for i, t in enumerate([team_1, team_2]):
        simulated_stats = {}
        for player in get_random_players(t):
            event_log = {}
            tm_score = 0
            opp_score  = 0
            player_stats = get_player_stats(player, t)[SCALED_STATS] * (possessions[i] / 100)
            shooting_pct = get_player_stats(player, t)[UNSCALED_STATS]

            _2p = 2.0 * player_stats['2PA'] * shooting_pct['2P%']
            _3p = 3.0 * player_stats['3PA'] * shooting_pct['3P%']
            _pts = float(_2p + _3p)

            event_log['2P'] = float(_2p / 2.0)
            event_log['3P'] = float(_3p / 3.0)
            tm_score += _pts

            for event in ['BLK', 'STL', 'TOV', 'ORB', 'DRB', 'PF']:
                tm_score += player_stats[event] * stats[event]['Tm']
                opp_score  += player_stats[event] * stats[event]['Opp_Score']
                event_log[event] = float(player_stats[event])

            simulated_stats[player] = [float(tm_score), float(opp_score), event_log]
        game_log.append(simulated_stats)

    t1 = np.array(list(game_log[0].values()))
    t2 = np.array(list(game_log[1].values()))
    team_1_score = np.sum(t1[:, 0]) + np.sum(t2[:, 1])
    team_2_score = np.sum(t1[:, 1]) + np.sum(t2[:, 0])
    
    if team_1_score > team_2_score:
        output['Winner'] = team_1.name
        output['Winner Score'] = team_1_score
        output['Loser'] = team_2.name
        output['Loser Score'] = team_2_score

    elif team_1_score < team_2_score:
        output['Winner'] = team_2.name
        output['Winner Score'] = team_2_score
        output['Loser'] = team_1.name
        output['Loser Score'] = team_1_score

    elif np.nan in [team_1_score, team_2_score]:
        return simulate_game(team_1, team_2)
    
    else:
        return simulate_game(team_1, team_2)

    output['Game Log'] = game_log
    return output


def parse_game_log(log):
    
    team_1_log = log[0]
    team_2_log = log[1]

    team_1_players = list(team_1_log.keys())
    team_2_players = list(team_2_log.keys())
    players = [team_1_players, team_2_players]

    event_log = {}
    for player in (team_1_players + team_2_players):
        event_log[player] = {}

    for i, team_log in enumerate([team_1_log, team_2_log]):
        for player in players[i]:
            for event, count  in team_log[player][2].items():
                if not event_log.get(player).get(event):
                    event_log[player][event] = count
                else:
                    event_log[player][event] += count

    return event_log


def simulate_n_games(team_1, team_2, n: int, summary=False, viz=False):
    clear_output()
    tqdm.write(f'Simulating Game: {team_1.name} vs. {team_2.name}')

    team_1_win_counter = 0
    team_2_win_counter = 0
    game_results = {
        team_1.name: [],
        team_2.name: []
    }
    
    total_stats_log = {}
    player_games_count = Counter() # Specifically for "Games Played"

    for i in trange(n):
        game = simulate_game(team_1, team_2)
        
        # 2. Append Scores for statistical analysis
        # We match the score to the correct team name list
        if game['Winner'] == team_1.name:
            team_1_win_counter += 1
            game_results[team_1.name].append(game['Winner Score'])
            game_results[team_2.name].append(game['Loser Score'])
        else:
            team_2_win_counter += 1
            game_results[team_2.name].append(game['Winner Score'])
            game_results[team_1.name].append(game['Loser Score'])

        # 3. Parse and Update Stats
        game_log = parse_game_log(game['Game Log'])

        for player, stats in game_log.items():
            # Track participation
            player_games_count[player] += 1
            
            # Update cumulative stats
            if player not in total_stats_log:
                total_stats_log[player] = Counter(stats)
            else:
                total_stats_log[player].update(stats)

    # Final Processing
    team_1_players = list(team_1.df.index)

    df = pd.DataFrame(total_stats_log).T.fillna(0)
    df['Games Played'] = df.index.map(player_games_count)
    df.insert(loc=0, column='Team', value=[team_1.name if p in team_1_players else team_2.name for p in list(df.index)])

    # Converting numbers in the dataframe to integers
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col]).astype(int)

    overall_winner = team_1.name if team_1_win_counter > team_2_win_counter else team_2.name
    overall_loser = team_1.name if team_1_win_counter < team_2_win_counter else team_2.name
    record = f'{team_1.name}: {team_1_win_counter} - {team_2_win_counter} :{team_2.name}'

    tqdm.write('Preparing simulation analysis.')

    prompt = create_prompt(overall_winner, record, df)
    analysis = GPT_Game_Analysis(prompt)

    tqdm.write(f'{team_1.name} vs. {team_2.name} Complete!')
    tqdm.write(analysis)

    return {'Winner': overall_winner,
             'Loser': overall_loser, 
             'Contributions': df, 
             'Scores': game_results, 
             'Team 1': team_1,
             'Team 2': team_2,
             'Win Count 1': team_1_win_counter,
             'Win Count 2': team_2_win_counter, 
             'Record': record,
             'Analysis': analysis
            }

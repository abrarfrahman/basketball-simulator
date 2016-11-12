from collections import Counter
import numpy as np

import triple_triple.player_possession_habits as pph

from triple_triple.startup_data import (
    get_df_pos_dist,
    get_df_box_score
)
# From pph, we import known_player_possessions, play_pass, df_player_possession
df_pos_dist = get_df_pos_dist()
df_pos_dist_reg = pph.get_player_court_region_df(df_pos_dist)
df_box_score = get_df_box_score()


def number_from_court_region(reg):
    if reg == 'back court':
        return 0
    if reg == 'mid-range':
        return 1
    if reg == 'key':
        return 2
    if reg == 'out of bounds':
        return 3
    if reg == 'paint':
        return 4
    if reg == 'perimeter':
        return 5


def court_region_from_number(num):
    if num == 0:
        return 'back court'
    if num == 1:
        return 'mid-range'
    if num == 2:
        return 'key'
    if num == 3:
        return 'out of bounds'
    if num == 4:
        return 'paint'
    if num == 5:
        return 'perimeter'


def get_player_region_prob(player_name, df_pos_dist_reg, num_regions=6):
    df_player_region = list(df_pos_dist_reg[player_name].region)
    # remove None values
    df_player_region = [x for x in df_player_region if x is not None]
    total_moments = len(df_player_region)
    reg_prob_list = np.zeros(num_regions)
    reg_prob_dict = {}
    for region, count in Counter(df_player_region).items():
        reg_prob_dict[region] = count / float(total_moments)
        reg_prob_list[number_from_court_region(region)] = count

    return reg_prob_dict, reg_prob_list / float(total_moments)


def get_prob_possession_type(df_player_possession, num_outcomes=4):
    poss_type_to_num = {
        'pass': 0,
        'shot': 1,
        'assist': 2,
        'turnover': 3
    }
    poss_type_prob = np.zeros(num_outcomes)
    for outcome, count in Counter(df_player_possession.type).items():
        poss_type_prob[poss_type_to_num[outcome]] = count

    print poss_type_to_num
    return poss_type_prob / float(len(df_player_possession))


def count_player_court_movement(df_pos):
    start = df_pos['start_region'].apply(number_from_court_region)

    end = df_pos['end_region'].apply(number_from_court_region)

    movement_matrix = np.zeros((6, 6))
    # for each posession, count player movements
    # for different regions on the court
    # using only start (row) and end region (column) of possession
    for i in range(len(start)):
        movement_matrix[start[i], end[i]] += 1
    return movement_matrix


def cond_prob_player_court_movement(movement_matrix):
    # given start region, probability of end region is
    # each element divided by sum of its row
    return movement_matrix / movement_matrix.sum(axis=1)[:, None]


def get_possession_per_second(df_box_score, player_name):
    total_min = df_box_score.query('PLAYER_NAME == @player_name')['MIN']\
        .iloc[0].minute
    total_sec = df_box_score.query('PLAYER_NAME == @player_name')['MIN']\
        .iloc[0].second + total_min * 60
    touches = df_box_score.query('PLAYER_NAME == @player_name')['TCHS'].iloc[0]
    return touches / float(total_sec)


def count_outcome_per_region(play_list, reg_to_num):
    outcome_matrix = np.zeros((6, 6))
    # create a matrix with pass count
    # row = start region
    # column = end region
    for item in play_list:
        outcome_matrix[reg_to_num[item[2]], reg_to_num[item[3]]] += 1
    return outcome_matrix


def get_cond_prob_poss(known_player_possessions, play_pass, reg_to_num):
    pass_matrix = count_outcome_per_region(play_pass, reg_to_num)

    # shots = known_player_possessions[0]
    shots_matrix = count_outcome_per_region(known_player_possessions[0], reg_to_num)

    # assists = known_player_possessions[1]
    assist_matrix = count_outcome_per_region(known_player_possessions[1], reg_to_num)

    # turnovers = known_player_possessions[2]
    turnover_matrix = count_outcome_per_region(known_player_possessions[2], reg_to_num)

    # cond probabilities
    pass_prob = pass_matrix / pass_matrix.sum(axis=1)[:, None]
    shot_prob = shots_matrix / shots_matrix.sum(axis=1)[:, None]
    assist_prob = assist_matrix / assist_matrix.sum(axis=1)[:, None]
    turnover_prob = turnover_matrix / turnover_matrix.sum(axis=1)[:, None]

    print reg_to_num
    print 'Row = start region, '
    print 'Column = end region'

    return pass_prob, shot_prob, assist_prob, turnover_prob

##################################
##################################

player_name = 'Chris Bosh'
poss_type_to_num = {
    'pass': 0,
    'shot': 1,
    'assist': 2,
    'turnover': 3
}
reg_to_num = {
    'back court': 0,
    'mid-range': 1,
    'key': 2,
    'out of bounds': 3,
    'paint': 4,
    'perimeter': 5
}

df_player_region = list(df_pos_dist_reg[player_name].region)
reg_prob_dict, reg_prob_list = get_player_region_prob(player_name, df_pos_dist_reg)

prob_poss_type = get_prob_possession_type(pph.df_player_possession, num_outcomes=4)

poss_per_sec = get_possession_per_second(df_box_score, player_name)

movement_matrix = count_player_court_movement(pph.df_player_possession)

cond_prob_movement = cond_prob_player_court_movement(movement_matrix)

pass_prob, shot_prob, assist_prob, turnover_prob = get_cond_prob_poss(pph.known_player_possessions, pph.play_pass, pph.reg_to_num)

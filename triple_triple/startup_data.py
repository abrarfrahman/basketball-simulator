import cPickle as pickle
import json
import os

import pandas as pd

from triple_triple.config import DATASETS_DIR


def get_player_ids():
    filepath = os.path.join(DATASETS_DIR, 'player_ids.json')
    return json.load(open(filepath))


def get_game_id_dict():
    filepath = os.path.join(DATASETS_DIR, 'game_id_dict.json')
    return json.load(open(filepath))


def get_df_positions():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_positions.csv')
    return pd.read_csv(filepath, header=[0, 1]).sort_index().sort_index(axis=1)


def get_df_pos_dist():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_pos_dist.csv')
    return pd.read_csv(filepath, header=[0, 1]).sort_index().sort_index(axis=1)


def get_df_pos_dist_trunc():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_pos_dist_trunc.csv')
    return pd.read_csv(filepath, header=[0, 1]).sort_index().sort_index(axis=1)


def get_df_raw_position_data():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_rawposition.csv')
    return pd.read_csv(filepath)


def get_df_play_by_play():
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_nbaplaybyplay.csv')
    return pd.read_csv(filepath)


def get_df_box_score():
    parse_date = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    filepath = os.path.join(DATASETS_DIR, 'MIA_GSW_box_score.csv')
    return pd.read_csv(filepath, parse_dates=['MIN'], date_parser=parse_date)


def get_df_player_bio_info():
    filepath = os.path.join(DATASETS_DIR, 'player_bio_info.csv')
    return pd.read_csv(filepath)


def get_df_all_game_info():
    filepath = os.path.join(DATASETS_DIR, 'df_all_game_info.csv')
    dtype_dict = {
        'game_id': str,
        'hometeam_id': str,
        'awayteam_id': str
    }
    return pd.read_csv(filepath, dtype=dtype_dict)


def get_player_possession_dataframes(json_file_name):
    with open(os.path.join(DATASETS_DIR, json_file_name), 'rb') as json_file:
        return pickle.load(json_file)

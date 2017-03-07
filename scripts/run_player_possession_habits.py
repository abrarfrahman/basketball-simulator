import triple_triple.player_possession_habits as pph

from triple_triple.team_shooting_side import get_initial_shooting_sides
from triple_triple.data_generators.player_game_stats_data import parse_df_play_by_play
from triple_triple.class_player import create_player_class_instance

from triple_triple.startup_data import (
    get_df_play_by_play,
    get_df_raw_position_data,
    get_df_raw_position_region(),
    get_game_info_dict,
    get_game_player_dict
)

df_raw_position_data = get_df_raw_position_data()
game_info_dict = get_game_info_dict()
game_player_dict = get_game_player_dict()
df_play_by_play = get_df_play_by_play()
df_game_stats = parse_df_play_by_play(df_play_by_play)

initial_shooting_side = get_initial_shooting_sides(df_play_by_play, df_raw_position_data, game_info_dict)


if __name__ == '__main__':

    df_possession = pph.get_possession_df(
        dataframe=df_raw_position_data,
        has_ball_dist=2.0,
        len_poss=15
    )

    df_possession = pph.add_regions_to_df(df_possession, initial_shooting_side)

    game_id_list = [21500568]
    player_id_list = [2547, 2548, 203110, 201939]

    player_class_dict = create_player_class_instance(
        player_list=player_id_list,
        game_player_dict=game_player_dict,
    )

    for player_class in player_class_dict.values():
        df_possession = pph.characterize_player_possessions(
            game_id=game_id_list[0],
            player_class=player_class,
            df_possession=df_possession,
            df_game_stats=df_game_stats
        )

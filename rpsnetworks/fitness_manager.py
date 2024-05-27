from rpsnetworks import battle_manager, schema_templates
import json

def getHighestScoringPlayer(generation: list[tuple[int, any]]) -> tuple[int, any]:
    biggest = 0
    for i in range(0, len(generation)):
        if generation[i][0] > generation[biggest][0]: biggest = i
    return generation.pop(biggest)

# universal fitness function
def scorePlayer(manager: battle_manager.Manager, player_id: str):
    score = 0
    for game_id in manager.results.keys():
        # only judge the model if it survives the game (0 points for losing)
        if player_id in manager.results[game_id]:
            # severely punish stalling out games (a.k.a. at least one other player survived with it)
            if len(manager.results[game_id]) != 1: score -= 5
            # reward winning games (a.k.a. only it survived)
            else: score += 1
    return score

# count up the moves made by the model
def countMoves(manager: battle_manager.Manager, player_id: str, schema: schema_templates.Schema):
    moves = {}
    total_player_moves = 0
    for type in schema.types.keys():
        moves[type] = 0
    for game_n in manager.history:
        for turn_n in range(0, len(manager.history[game_n])):
            turn_history = manager.history[game_n][turn_n]
            players_before_turn = json.loads(turn_history["players_before_turn"])
            player_index = -1
            for i in range(0, len(players_before_turn)):
                if players_before_turn[i]["id"] == player_id:
                    player_index = i
                    break

            if player_index >= 0:
                player_move_type_this_turn = turn_history["moves"][player_index]
                moves[player_move_type_this_turn] += 1
                total_player_moves += 1

    for type in moves.keys():
        moves[type] = round(moves[type] / total_player_moves, 4)
    return moves
from rpsnetworks import network, battle_manager, player_templates, schema_templates, fitness_manager
import time
import pandas

from importlib import reload
reload(battle_manager)
reload(player_templates)
reload(network)
reload(fitness_manager)

# runs many training simulations and returns statistics to help determine error rates in training
def evalutateNetworkTrainingEfficacy(generations: int,
                                generation_size: int,
                                tests_per_child: int,
                                final_selection_size: int,
                                layer_sizes: list[int],
                                network_player_template,
                                opponents: list[player_templates.Player],
                                network_hit_points: int,
                                schema: schema_templates.Schema,
                                sample_size = 10,
                                time_limit = 60):
    start_time = time.time()
    samples = []
    while len(samples) < sample_size:
        sample = trainNetwork(generations,
                                generation_size,
                                tests_per_child,
                                final_selection_size,
                                layer_sizes,
                                network_player_template,
                                opponents,
                                network_hit_points,
                                schema)
        samples.append(sample)
        if time.time() - start_time > time_limit: break
    end_time = time.time()

    sample_frame = pandas.DataFrame(samples)

    mean = sample_frame[0].mean()
    q0 = sample_frame[0].quantile(0)
    q05 = sample_frame[0].quantile(0.05)
    q25 = sample_frame[0].quantile(0.25)
    q50 = sample_frame[0].quantile(0.5)
    q75 = sample_frame[0].quantile(0.75)
    q95 = sample_frame[0].quantile(0.95)
    q100 = sample_frame[0].quantile(1)
    train_time = end_time - start_time
    avg_train_time = train_time/len(samples)

    print("RESULTS:")
    print("Mean winrate: %.4f" %(mean))
    print("Worst: %.4f" %(q0))
    print("Q1: %.4f" %(q25))
    print("Q2: %.4f" %(q50))
    print("Q3: %.4f" %(q75))
    print("Best: %.4f" %(q100))
    print("-------------------")
    print("IQR: %.4f" %(q75 - q25))
    print("90 Percent Range %.4f" %(q95 - q05))
    print("Range: %.4f" %(q100 - q0))
    print("-------------------")
    print("Time taken for this test: %.4fs" %(train_time))
    print("Average time per train: %.4fs" %(avg_train_time))
    print("Models trained: %d" %(len(samples)))
    print("-------------------")
    print("IQR-time: %.4f" %((q75 - q25)*avg_train_time))
    print("90 Percent Range-time %.4f" %((q95 - q05)*avg_train_time))
    print("Range-time: %.4f" %((q100 - q0)*avg_train_time))

    return sample_frame

def debugNetworkWeightSum(network: network.Network):
    sum = 0
    for a in network.weights:
        for b in a:
            for c in b:
                sum += abs(c)
    return sum

def testNetwork(manager: battle_manager.Manager,
             number_of_games: int,
             network: network.Network,
             network_player_template,
             opponents: list[player_templates.Player],
             network_hit_points: int,
             schema: schema_templates.Schema,
             options: dict) -> int:
    manager.wipeHistory()
    manager.wipeResults()

    player = network_player_template("test_network", network_hit_points, "test_controller", network)
    players = opponents.copy()
    players.append(player)

    battle_manager.runGames(manager, number_of_games, players, schema, options)
    return fitness_manager.scorePlayer(manager, "test_network")

def trainNetwork(generations: int,
                    generation_size: int,
                    tests_per_child: int,
                    fine_selection_size: int,
                    layer_sizes: list[int],
                    network_player_template,
                    opponents: list[player_templates.Player],
                    network_hit_points: int,
                    schema: schema_templates.Schema,
                    debug = False) -> tuple[float, network.Network, dict, dict]:
    manager = battle_manager.Manager()
    seed = (0, network.Network(len(layer_sizes), layer_sizes))

    for i in range(1, generations + 1):
        generation = []
        for j in range(0, (10 * generation_size if i == 1 else generation_size)):
            score = 0
            while score == 0:
                child_network = network.Network(3, layer_sizes)
                child_network.setWeights(seed[1].weights)
                child_network.jostleSelf(((j/10 if i==1 else j)/i)**0.5)
                
                score = testNetwork(manager, tests_per_child, child_network, network_player_template, opponents, network_hit_points, schema, {})
            generation.append((score, child_network))

        # if we have the fine selection step enabled, do it
        if fine_selection_size > 1:
            final_generation = []
            for k in range(1, fine_selection_size + 1):
                # pop the highest-scoring player off of our generation
                temp_seed = fitness_manager.getHighestScoringPlayer(generation)
                # give them a more accurate rescore
                temp_score = testNetwork(manager, tests_per_child*2, temp_seed[1], network_player_template, opponents, network_hit_points, schema, {})
                final_generation.append((temp_score, temp_seed[1]))

                # debug code to gain insight into training effectiveness
                if debug:
                    real_score = testNetwork(manager, 1000, temp_seed[1], network_player_template, opponents, network_hit_points, schema, {})
                    print("seed %d score: " %(k) + str(temp_seed[0]/tests_per_child),
                          "revised score: " + str(temp_score/(tests_per_child*2)),
                          "actual proficiency: " + str(real_score/1000),
                          "absolute network weight: " + str(debugNetworkWeightSum(temp_seed[1])))
                    if k == fine_selection_size: print("---------------")
            generation = final_generation

        # get our seed and loop back
        seed = fitness_manager.getHighestScoringPlayer(generation)

        # alternative debug code for if we're not doing a fine selection round
        if debug and fine_selection_size <= 1:
            real_score = testNetwork(manager, 1000, seed[1], network_player_template, opponents, network_hit_points, schema, {})
            print("seed score: " + str(seed[0]/tests_per_child),
                  "actual proficiency: " + str(real_score/1000),
                  "absolute network weight: " + str(debugNetworkWeightSum(seed[1])))
            print("---------------")

    # get a final result to test the effectiveness of the model
    score = testNetwork(manager, 10000, seed[1], network_player_template, opponents, network_hit_points, schema, {"record_players": True})
    moves = fitness_manager.countMoves(manager, "test_network", schema)

    return (score/10000, seed[1], manager.results, moves)
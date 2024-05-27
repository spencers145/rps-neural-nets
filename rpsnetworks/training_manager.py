from rpsnetworks import network, battle_manager, player_templates, schema_templates, fitness_manager

def debugNetworkWeightSum(network: network.Network):
    sum = 0
    for a in network.weights:
        for b in a:
            for c in b:
                sum += abs(c)
    return sum

# run a number of games to test the effectiveness of the network we've trained
# return a score: the number of games won
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

    # make a new player from the template
    player = network_player_template("test_network", network_hit_points, "test_controller", network)

    # do some housekeeping to get our player list ready
    players = opponents.copy()
    players.append(player)

    battle_manager.runGames(manager, number_of_games, players, schema, options)
    return fitness_manager.scorePlayer(manager, "test_network")

def trainNetwork(generations: int,
                    generation_size: int,
                    base_tests_per_child: int,
                    layer_sizes: list[int],
                    network_player_template,
                    opponents: list[player_templates.Player],
                    network_hit_points: int,
                    schema: schema_templates.Schema,
                    verbose = False,
                    debug = False) -> tuple[float, network.Network, dict, dict]:
    manager = battle_manager.Manager()
    # set our seed
    seed = (0, network.Network(len(layer_sizes), layer_sizes))

    for i in range(1, generations + 1):
        generation = []
        # first, generate a lot of randomly jostled networks
        # if this is the first generation, make 10x more than usual
        for j in range(0, (10*generation_size if i == 1 else generation_size)):
            child_score = 0
            while child_score <= 0:
                # make a new network based on the seed
                child_network = network.Network(3, layer_sizes)
                child_network.setWeights(seed[1].weights)
                # jostle amount as a function of how many generations (i) and which child (j)
                # effectively, i increase precision over time
                # and every generation, j produce more networks close to the seed, and less far away  
                magnitude = (j/10 if i == 1 else j)/i
                child_network.jostleSelf(magnitude**0.5)
                
                # perform a very quick test of the network
                # if it loses 5 times in a row, the while loop continues
                # -> aka we make a new one because this one sucks!
                # we don't want to consider useless candidates, that's wasteful!
                child_score = testNetwork(manager, 5, child_network, network_player_template, opponents, network_hit_points, schema, {})

                # always allow the seed network through
                if j == 0: break
            # serviceable networks get added to the generation
            generation.append((child_score, child_network))

        step = 0
        while len(generation) > 1:
            step += 1
            # list for networks and their scores during this step
            step_generation = []
            target_survivor_count = len(generation)/(2*step)

            # test each network. give them a score.
            # the # of tests increases as we refine our selection
            tests = 5 if step == 1 else round(base_tests_per_child * 2**(step - 2))
            for child in generation:
                child_score = testNetwork(manager, tests, child[1], network_player_template, opponents, network_hit_points, schema, {})
                # add this score to score from previous rounds
                # don't want to waste any of our testing data
                step_generation.append((child_score + child[0], child[1]))
            generation = []

            # debug code that activates if verbose is on
            # tells about the scores of contestants in the training process for each round
            if debug and verbose:
                debug_scores = []
                for child in step_generation:
                    debug_scores.append(child[0])
                debug_scores.sort(reverse=True)
                print(debug_scores)

            # pop off the best math.ceil(len(generation)/(2*step)) players
            while len(generation) < target_survivor_count:
                best = fitness_manager.getHighestScoringPlayer(step_generation)
                generation.append(best)

        # get our new seed and loop back
        seed = generation[0]

        # optional debug info about the seed we just trained
        # keeps track of the networks between generations
        if debug:
            real_score = testNetwork(manager, 1000, seed[1], network_player_template, opponents, network_hit_points, schema, {})
            print("actual proficiency: " + str(real_score/1000),
                  "absolute network weight: " + str(debugNetworkWeightSum(seed[1])))
            print("---------------")

    # get a final result to test the effectiveness of the model
    score = testNetwork(manager, 10000, seed[1], network_player_template, opponents, network_hit_points, schema, {"record_players": True})
    moves = fitness_manager.countMoves(manager, "test_network", schema)

    # explicitly print results if we are verbose
    if verbose:
        print("TRAINING PARAMETERS:")
        print("Generations: %d" %(generation_size))
        print("Children tested per generation: %d" %(generation_size))
        print("Base # of test-games per child: %d" %(base_tests_per_child))
        print("---------------")
        print("Schema used: %s" %(schema.NAME))
        print("Opponent count: %d" %(len(opponents)))
        print("---------------")
        print("RESULTS:")
        print("Network proficiency: %.3f" %(score/10000))
        print("Move distribution:")
        for move in moves.keys():
            print("%s: %.3f" %(move, moves[move]))

    return (score/10000, seed[1], manager.results, moves)
# if __name__ == '__main__':
#     import player_templates
#     import schema_templates
#     import legacy_training_manager
#     import time
#     import pandas
#     import multiprocessing

#     generations = 10
#     generation_size = 20
#     tests_per_child = 20
#     final_selection_size = 2
#     layer_sizes = [3, 2, 5]
#     network_player_template = player_templates.playerAwareNetworkPlayer
#     opponents = [
#         player_templates.mixedStrategyPlayer("player1", 4, [0.2, 0.2, 0.2, 0.2, 0.2]),
#     ]
#     network_hit_points = 4
#     schema = schema_templates.RPGFascimile()
#     sample_size = 200

#     start_time = time.time()
#     with multiprocessing.Pool(10) as pool:
#         results = [pool.apply_async(training_manager.trainNetwork,
#                                     (generations,
#                                     generation_size,
#                                     tests_per_child,
#                                     final_selection_size,
#                                     layer_sizes,
#                                     network_player_template,
#                                     opponents,
#                                     network_hit_points,
#                                     schema))
#                     for i in range(0, sample_size)]
        
#         samples = [rs.get() for rs in results]
#     end_time = time.time()

#     sample_frame = pandas.DataFrame(samples)

#     mean = sample_frame[0].mean()
#     q0 = sample_frame[0].quantile(0)
#     q05 = sample_frame[0].quantile(0.05)
#     q25 = sample_frame[0].quantile(0.25)
#     q50 = sample_frame[0].quantile(0.5)
#     q75 = sample_frame[0].quantile(0.75)
#     q95 = sample_frame[0].quantile(0.95)
#     q100 = sample_frame[0].quantile(1)
#     train_time = end_time - start_time
#     avg_train_time = train_time/len(samples)

#     print("RESULTS:")
#     print("Mean winrate: %.4f" %(mean))
#     print("Worst: %.4f" %(q0))
#     print("Q1: %.4f" %(q25))
#     print("Q2: %.4f" %(q50))
#     print("Q3: %.4f" %(q75))
#     print("Best: %.4f" %(q100))
#     print("-------------------")
#     print("IQR: %.4f" %(q75 - q25))
#     print("90 Percent Range %.4f" %(q95 - q05))
#     print("Range: %.4f" %(q100 - q0))
#     print("-------------------")
#     print("Time taken for this test: %.4fs" %(train_time))
#     print("Average time per train: %.4fs" %(avg_train_time))
#     print("Models trained: %d" %(len(samples)))
#     print("-------------------")
#     print("IQR-time: %.4f" %((q75 - q25)*avg_train_time))
#     print("90 Percent Range-time %.4f" %((q95 - q05)*avg_train_time))
#     print("Range-time: %.4f" %((q100 - q0)*avg_train_time))

#     while True: pass

if __name__ == '__main__':
    import player_templates
    import schema_templates
    import training_manager
    import time
    import pandas
    import multiprocessing

    generations = 10
    generation_size = 20
    tests_per_child = 20
    layer_sizes = [3, 2, 5]
    network_player_template = player_templates.playerAwareNetworkPlayer
    opponents = [
        player_templates.mixedStrategyPlayer("player1", 4, [0.2, 0.2, 0.2, 0.2, 0.2]),
    ]
    network_hit_points = 3
    schema = schema_templates.RPGFascimile()
    sample_size = 200

    start_time = time.time()
    with multiprocessing.Pool(10) as pool:
        results = [pool.apply_async(training_manager.trainNetwork,
                                    (generations,
                                    generation_size,
                                    tests_per_child,
                                    layer_sizes,
                                    network_player_template,
                                    opponents,
                                    network_hit_points,
                                    schema))
                    for i in range(0, sample_size)]
        
        samples = [rs.get() for rs in results]
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

    while True: pass

# no final selection, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.6973
# Worst: 0.4108
# Q1: 0.4794
# Q2: 0.7563
# Q3: 0.8319
# Best: 0.8941
# -------------------
# IQR: 0.3525
# 90 Percent Range 0.4156
# Range: 0.4833
# -------------------
# Time taken for this test: 144.1962s
# Average time per train: 1.4420s
# Models trained: 100
# -------------------
# IQR-time: 0.5083
# 90 Percent Range-time 0.5993
# Range-time: 0.6969

# final selection enabled, size 2, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.7594
# Worst: 0.4000
# Q1: 0.7058
# Q2: 0.8326
# Q3: 0.8564
# Best: 0.8946
# -------------------
# IQR: 0.1506
# 90 Percent Range 0.4116
# Range: 0.4946
# -------------------
# Time taken for this test: 163.2360s
# Average time per train: 1.6324s
# Models trained: 100
# -------------------
# IQR-time: 0.2459
# 90 Percent Range-time 0.6720
# Range-time: 0.8074

# final selection enabled, size 3, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.7630
# Worst: 0.4522
# Q1: 0.7318
# Q2: 0.8360
# Q3: 0.8592
# Best: 0.8990
# -------------------
# IQR: 0.1274
# 90 Percent Range 0.4232
# Range: 0.4468
# -------------------
# Time taken for this test: 169.3246s
# Average time per train: 1.6932s
# Models trained: 100
# -------------------
# IQR-time: 0.2158
# 90 Percent Range-time 0.7166
# Range-time: 0.7565

# no final selection, 10-20-60, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.7705
# Worst: 0.4594
# Q1: 0.6987
# Q2: 0.8311
# Q3: 0.8675
# Best: 0.8937
# -------------------
# IQR: 0.1688
# 90 Percent Range 0.4197
# Range: 0.4343
# -------------------
# Time taken for this test: 233.9675s
# Average time per train: 2.3397s
# Models trained: 100
# -------------------
# IQR-time: 0.3949
# 90 Percent Range-time 0.9820
# Range-time: 1.0161

# no final selection, 10-40-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.7900
# Worst: 0.4658
# Q1: 0.7636
# Q2: 0.8301
# Q3: 0.8608
# Best: 0.8979
# -------------------
# IQR: 0.0972
# 90 Percent Range 0.4022
# Range: 0.4321
# -------------------
# Time taken for this test: 218.9080s
# Average time per train: 2.1891s
# Models trained: 100
# -------------------
# IQR-time: 0.2128
# 90 Percent Range-time 0.8803
# Range-time: 0.9459

# final selection, size 2, 10-40-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.7865
# Worst: 0.4336
# Q1: 0.7819
# Q2: 0.8435
# Q3: 0.8607
# Best: 0.8959
# -------------------
# IQR: 0.0788
# 90 Percent Range 0.4201
# Range: 0.4623
# -------------------
# Time taken for this test: 209.1966s
# Average time per train: 2.0920s
# Models trained: 100
# -------------------
# IQR-time: 0.1650
# 90 Percent Range-time 0.8789
# Range-time: 0.9671

# final selection, size 2, 10-40-40, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8179
# Worst: 0.4628
# Q1: 0.8270
# Q2: 0.8555
# Q3: 0.8722
# Best: 0.8954
# -------------------
# IQR: 0.0452
# 90 Percent Range 0.4122
# Range: 0.4326
# -------------------
# Time taken for this test: 299.4333s
# Average time per train: 2.9943s
# Models trained: 100
# -------------------
# IQR-time: 0.1355
# 90 Percent Range-time 1.2342
# Range-time: 1.2953

# big starting-round enabled, no final selection, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8151
# Worst: 0.4698
# Q1: 0.8066
# Q2: 0.8448
# Q3: 0.8681
# Best: 0.8981
# -------------------
# IQR: 0.0615
# 90 Percent Range 0.2375
# Range: 0.4283
# -------------------
# Time taken for this test: 203.5779s
# Average time per train: 2.0358s
# Models trained: 100
# -------------------
# IQR-time: 0.1252
# 90 Percent Range-time 0.4835
# Range-time: 0.8719

# big starting-round enabled, final selection, size 2, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8345
# Worst: 0.6603
# Q1: 0.8117
# Q2: 0.8425
# Q3: 0.8688
# Best: 0.8932
# -------------------
# IQR: 0.0571
# 90 Percent Range 0.1886
# Range: 0.2329
# -------------------
# Time taken for this test: 210.4144s
# Average time per train: 2.1041s
# Models trained: 100
# -------------------
# IQR-time: 0.1201
# 90 Percent Range-time 0.3969
# Range-time: 0.4901

# retest:
# RESULTS:
# Mean winrate: 0.8226
# Worst: 0.4714
# Q1: 0.8173
# Q2: 0.8435
# Q3: 0.8626
# Best: 0.8912
# -------------------
# IQR: 0.0453
# 90 Percent Range 0.1931
# Range: 0.4198
# -------------------
# Time taken for this test: 205.7562s
# Average time per train: 2.0576s
# Models trained: 100
# -------------------
# IQR-time: 0.0932
# 90 Percent Range-time 0.3973
# Range-time: 0.8638

# big starting-round enabled, final selection, size 3, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8293
# Worst: 0.4621
# Q1: 0.8189
# Q2: 0.8467
# Q3: 0.8722
# Best: 0.8923
# -------------------
# IQR: 0.0534
# 90 Percent Range 0.1971
# Range: 0.4302
# -------------------
# Time taken for this test: 206.1964s
# Average time per train: 2.0620s
# Models trained: 100
# -------------------
# IQR-time: 0.1100
# 90 Percent Range-time 0.4065
# Range-time: 0.8871

# non-zero big starting-round enabled, final selection, size 2, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8453
# Worst: 0.6658
# Q1: 0.8295
# Q2: 0.8501
# Q3: 0.8707
# Best: 0.8916
# -------------------
# IQR: 0.0412
# 90 Percent Range 0.1025
# Range: 0.2258
# -------------------
# Time taken for this test: 215.5502s
# Average time per train: 2.1555s
# Models trained: 100
# -------------------
# IQR-time: 0.0888
# 90 Percent Range-time 0.2210
# Range-time: 0.4867

# non-zero big starting-round enabled, final selection, size 2, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8431
# Worst: 0.6919
# Q1: 0.8233
# Q2: 0.8523
# Q3: 0.8740
# Best: 0.8993
# -------------------
# IQR: 0.0507
# 90 Percent Range 0.1191
# Range: 0.2074
# -------------------
# Time taken for this test: 442.4083s
# Average time per train: 2.2120s
# Models trained: 200
# -------------------
# IQR-time: 0.1122
# 90 Percent Range-time 0.2634
# Range-time: 0.4588

# non-zero ALL (as opposed to non-zero for just the big starting round),
# big starting-round enabled, final selection, size 2, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8399
# Worst: 0.4649
# Q1: 0.8260
# Q2: 0.8512
# Q3: 0.8740
# Best: 0.9069
# -------------------
# IQR: 0.0479
# 90 Percent Range 0.1403
# Range: 0.4420
# -------------------
# Time taken for this test: 462.6505s
# Average time per train: 2.3133s
# Models trained: 200
# -------------------
# IQR-time: 0.1109
# 90 Percent Range-time 0.3245
# Range-time: 1.0225

# big start round enabled, progressive selection, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8451
# Worst: 0.7407
# Q1: 0.8271
# Q2: 0.8486
# Q3: 0.8651
# Best: 0.9029
# -------------------
# IQR: 0.0380
# 90 Percent Range 0.1019
# Range: 0.1622
# -------------------
# Time taken for this test: 408.0616s
# Average time per train: 2.0403s
# Models trained: 200
# -------------------
# IQR-time: 0.0776
# 90 Percent Range-time 0.2078
# Range-time: 0.3309

# non-zero results enforced, big start round enabled, progressive selection, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8486
# Worst: 0.6622
# Q1: 0.8317
# Q2: 0.8565
# Q3: 0.8734
# Best: 0.8980
# -------------------
# IQR: 0.0417
# 90 Percent Range 0.0930
# Range: 0.2358
# -------------------
# Time taken for this test: 450.7231s
# Average time per train: 2.2536s
# Models trained: 200
# -------------------
# IQR-time: 0.0940
# 90 Percent Range-time 0.2096
# Range-time: 0.5314

# carry-over scores, non-zero results enforced, big start round enabled, progressive selection, 10-20-20, 0.2 spread RPG, player-aware
# RESULTS:
# Mean winrate: 0.8527
# Worst: 0.7312
# Q1: 0.8374
# Q2: 0.8593
# Q3: 0.8760
# Best: 0.9043
# -------------------
# IQR: 0.0387
# 90 Percent Range 0.1043
# Range: 0.1731
# -------------------
# Time taken for this test: 442.8340s
# Average time per train: 2.2142s
# Models trained: 200
# -------------------
# IQR-time: 0.0856
# 90 Percent Range-time 0.2308
# Range-time: 0.3833
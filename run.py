import neat
import pickle
import os
from game import withAI, withoutAI



config_path = "assets/config.txt"
winner_path = "winner.pkl"
if(os.path.exists(winner_path)):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    with open(winner_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    withAI(genomes, config)
else:
    withoutAI()

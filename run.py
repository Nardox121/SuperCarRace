import neat
import pickle
from game import withAI, withoutAI



config_path = "assets/config.txt"
winner_path = "winner.pkl"
try:
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    with open(winner_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    withAI(genomes, config)
except:
    withoutAI()

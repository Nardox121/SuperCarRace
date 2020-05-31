import numpy
import GeneticAlgorithm
import pickle
import NeuralNetwork

class AI(self):
    def __init__(self, data_inputs, data_outputs):
        self.sol_per_pop = 8
        self.num_parents_mating = 4
        self.num_generations = 1000
        self.mutation_percent = 10
        self.initial_pop_weights = []
        for curr_sol in numpy.arange(0, self.sol_per_pop):
            self.HL1_neurons = 6
            self.input_HL1_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                                    size=(data_inputs.shape[1], HL1_neurons))

            self.HL2_neurons = 5
            self.HL1_HL2_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                                    size=(self.HL1_neurons, self.HL2_neurons))

            self.output_neurons = 4
            self.HL2_output_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                                    size=(self.HL2_neurons, self.output_neurons))

            self.initial_pop_weights.append(numpy.array([self.input_HL1_weights, 

                                                        self.HL1_HL2_weights, 

                                                       self.HL2_output_weights]))

        self.pop_weights_mat = numpy.array(self.initial_pop_weights)
        self.pop_weights_vector = GeneticAlgorithm.mat_to_vector(self.pop_weights_mat)
        self.best_outputs = []
        self.accuracies = numpy.empty(shape=(self.num_generations))

        for generation in range(self.num_generations):
            print("Generation : ", generation)

            # converting the solutions from being vectors to matrices.
            self.pop_weights_mat = GeneticAlgorithm.vector_to_mat(self.pop_weights_vector, 
                                            self.pop_weights_mat)

            # Measuring the fitness of each chromosome in the population.
            self.fitness = NeuralNetwork.fitness(self.pop_weights_mat, 
                                data_inputs, 
                                data_outputs, 
                                activation="sigmoid")

            self.accuracies[generation] = self.fitness[0]

f = open("dataset_features.pkl", "rb")
data_inputs2 = pickle.load(f)
f.close()
features_STDs = numpy.std(a=data_inputs2, axis=0)
data_inputs = data_inputs2[:, features_STDs>50]


f = open("outputs.pkl", "rb")
data_outputs = pickle.load(f)
f.close()

#Genetic algorithm parameters:
#    Mating Pool Size (Number of Parents)
#    Population Size
#    Number of Generations
#    Mutation Percent

sol_per_pop = 8
num_parents_mating = 4
num_generations = 1000
mutation_percent = 10

#Creating the initial population.
initial_pop_weights = []
for curr_sol in numpy.arange(0, sol_per_pop):
    HL1_neurons = 6
    input_HL1_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                             size=(data_inputs.shape[1], HL1_neurons))

    HL2_neurons = 5
    HL1_HL2_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                             size=(HL1_neurons, HL2_neurons))

    output_neurons = 4
    HL2_output_weights = numpy.random.uniform(low=-0.1, high=0.1, 

                                              size=(HL2_neurons, output_neurons))

    initial_pop_weights.append(numpy.array([input_HL1_weights, 

                                                HL1_HL2_weights, 

                                                HL2_output_weights]))

pop_weights_mat = numpy.array(initial_pop_weights)
pop_weights_vector = GeneticAlgorithm.mat_to_vector(pop_weights_mat)

best_outputs = []
accuracies = numpy.empty(shape=(num_generations))

for generation in range(num_generations):
    print("Generation : ", generation)

    # converting the solutions from being vectors to matrices.
    pop_weights_mat = GeneticAlgorithm.vector_to_mat(pop_weights_vector, 
                                       pop_weights_mat)

    # Measuring the fitness of each chromosome in the population.
    fitness = NeuralNetwork.fitness(pop_weights_mat, 
                          data_inputs, 
                          data_outputs, 
                          activation="sigmoid")

    accuracies[generation] = fitness[0]
    print("Fitness")
    print(fitness)

    # Selecting the best parents in the population for mating.
    parents = GeneticAlgorithm.select_mating_pool(pop_weights_vector, 

                                    fitness.copy(), 

                                    num_parents_mating)
    print("Parents")
    print(parents)

    # Generating next generation using crossover.
    offspring_crossover = GeneticAlgorithm.crossover(parents,

                                       offspring_size=(pop_weights_vector.shape[0]-parents.shape[0], pop_weights_vector.shape[1]))

    print("Crossover")
    print(offspring_crossover)

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = GeneticAlgorithm.mutation(offspring_crossover, 

                                     mutation_percent=mutation_percent)
    print("Mutation")
    print(offspring_mutation)

    # Creating the new population based on the parents and offspring.
    pop_weights_vector[0:parents.shape[0], :] = parents
    pop_weights_vector[parents.shape[0]:, :] = offspring_mutation

pop_weights_mat = GeneticAlgorithm.vector_to_mat(pop_weights_vector, pop_weights_mat)
best_weights = pop_weights_mat [0, :]
acc, predictions = NeuralNetwork.predict_outputs(best_weights, data_inputs, data_outputs, activation="sigmoid")
print("Accuracy of the best solution is : ", acc)

f = open("weights_"+str(num_generations)+"_iterations_"+str(mutation_percent)+"%_mutation.pkl", "wb")
pickle.dump(pop_weights_mat, f)
f.close()
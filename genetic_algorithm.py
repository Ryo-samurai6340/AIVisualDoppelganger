import random
import numpy as np
from PIL import Image
from skimage import exposure

class GeneticAlgorithm:
    # constructor to initialize the objs
    def __init__(self, population_size, chromosome_length):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.population = self.initialize_population()

    # Initialize the population with random individuals
    def initialize_population(self):
        return [self.generate_random_individual() for _ in range(self.population_size)]

    # Generate a random individual
    def generate_random_individual(self):
        return [random.randint(0, 1) for _ in range(self.chromosome_length)]

    # Decode an individual into an img with a camouflaged pattern
    def decode_individual(self, individual, original_image):
        # convert binary to an img with colors mapped from the original img
        decoded_image = np.zeros(original_image.shape, dtype=np.uint8)
        
        # Reshape the individual into the same shape as the original img
        reshaped_individual = np.array(individual).reshape(original_image.shape)
        
        # Define the intensity threshold for the camouflage pattern
        threshold = 0.5 

        # create the camouflage pattern by thresholding the individual
        camouflage_pattern = (reshaped_individual > threshold) * 255

        # apply the camouflage pattern to each channel of the original image
        decoded_image = original_image * (1 - camouflage_pattern / 255)
    
        return decoded_image
    
    # def map_binary_to_colors(self, binary_representation, original_image):
    #     unique_colors = np.unique(original_image)
    #     color_mapping = {0: unique_colors[0], 1: unique_colors[-1]}
    #     color_indices = np.array(binary_representation)
    #     colors = np.array([color_mapping[value] for value in color_indices])
    #     decoded_image = np.resize(colors, original_image.shape)
    #     return decoded_image

    # def transfer_patterns(self, decoded_image, original_image):
    #     decoded_image = exposure.equalize_hist(decoded_image)
    #     transferred_image = (decoded_image + original_image) / 2
    #     return transferred_image

    # crate a fitness function to evaluate the fitness of an individual
    def fitness_function(self, individual, original_image):
        decoded_image = self.decode_individual(individual, original_image)
        fitness = self.calculate_fitness(decoded_image, original_image)
        return fitness

    def calculate_fitness(self, evolved_image, original_image):
        evolved_array = np.array(evolved_image)  # Convert the binary to a numpy array
        
        # calculate the absolute difference btw the evolved & original img
        absolute_difference = np.abs(evolved_array - original_image) 
        fitness = np.sum(absolute_difference) # calculat teh fitness based on the sum of absolute difference 
        return fitness

    # Crossover operation to create a child from two parents
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.chromosome_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    # Mutatation operation to implement the random changes into an individual 
    def mutate(self, individual, mutation_rate):
        mutated_individual = [bit ^ 1 if random.random() < mutation_rate else bit for bit in individual]
        return mutated_individual

    # Evolve the population over a specific number of generations
    def evolve(self, original_image, generations, mutation_rate):
        for generation in range(generations):
            fitness_scores = [self.fitness_function(individual, original_image) for individual in self.population]
            parents = self.select_parents(fitness_scores)

            # Create the next generation w crossover and mutation
            new_population = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = parents[i], parents[i + 1]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, mutation_rate)
                child2 = self.mutate(child2, mutation_rate)
                new_population.extend([child1, child2])

            self.population = new_population

            # Display the info of the current generation
            best_fitness = min(fitness_scores)
            print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

        # Return the best individual right after the specified number of generations
        best_individual = self.select_best_individual(original_image)
        return best_individual

    # select parents based on fitness scores
    def select_parents(self, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [score / total_fitness for score in fitness_scores]

        # Select parents with probabilities proportional to their fitness
        parents_indices = np.random.choice(range(self.population_size), size=self.population_size, p=probabilities)
        parents = [self.population[index] for index in parents_indices]
        
        return parents

    # select the individual w the best individual
    def select_best_individual(self, original_image):
        best_index = np.argmin([self.fitness_function(individual, original_image) for individual in self.population])
        return self.population[best_index]

if __name__ == "__main__":
    # define the img as a binary array that shows the desired camouflaged pattern
    original_image = np.array([0, 1, 0, 1, 0, 1, 0, 1])

    # Set parametes for the genetic algo
    population_size = 20
    chromosome_length = len(original_image)
    generations = 1
    mutation_rate = 0.5

    # create an instance of the genetic algo class w specified parameters
    genetic_algorithm = GeneticAlgorithm(population_size, chromosome_length)
    
    # evolve the population to fine the best individual
    best_individual = genetic_algorithm.evolve(original_image, generations, mutation_rate)

    # decode tne best individual to get the generated image 
    decoded_best_individual = genetic_algorithm.decode_individual(best_individual, original_image)
    
    print("Decoded Best Individual:", decoded_best_individual)

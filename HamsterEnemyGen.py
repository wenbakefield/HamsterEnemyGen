import random
import statistics
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
from numpy import diff
from collections import Counter

class Trait:
    def __init__(self, name, attack, defense, vulnerability):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.vulnerability = vulnerability
    def __repr__(self):
        return "%s" % (self.name)
        # return "<Trait | Name:%s Attack:%s Defense:%s Vulnerability:%s>" % (self.name, self.attack, self.defense, self.vulnerability)
    def __str__(self):
        return "%s" % (self.name)
    def __eq__(self, other):
        if isinstance(other, Trait):
            return self.name == other.name and self.attack == other.attack and self.defense == other.defense and self.vulnerability == other.vulnerability

class Enemy:
    def __init__(self, species, trait, health):
        self.species = species
        self.trait = trait
        self.health = health
    def __repr__(self):
        return "<Enemy | Species:%s Trait:%s Health:%s = %s>" % (self.species, self.trait, self.health, sum(self.health) + self.trait.vulnerability)
    def __str__(self):
        return "%s %s with %s health" % (self.trait, self.species, sum(self.health) + self.trait.vulnerability)
    def __eq__(self, other):
        if isinstance(other, Enemy):
            return self.species == other.species and self.trait == other.trait and self.health == other.health


def pick_random(health_deck):
  r, s = random.random(), 0
  for num in health_deck:
    s += num[1]
    if s >= r:
      return num[0]

def generate_enemies(species_list, traits_pool, health_pool, num_enemies):
    enemies = []
    for i in range(num_enemies):
        current_enemy_species = random.choice(species_list)
        current_enemy_trait = pick_random(traits_pool)
        current_enemy_health = []
        current_enemy_health.append(pick_random(health_pool))
        current_enemy_health.append(pick_random(health_pool))
        current_enemy = Enemy(current_enemy_species, current_enemy_trait, current_enemy_health)
        enemies.append(current_enemy)
    return enemies

def get_enemy_fitness(enemy):
    target = 7
    return abs(target - (sum(enemy.health) + enemy.trait.vulnerability))

def get_enemies_fitness(enemies):
    fitness = 0
    for enemy in enemies:
        fitness += get_enemy_fitness(enemy)
    return fitness

def get_fit_percentage(enemies):
    num_fit = sum((get_enemy_fitness(enemy) == 0) for enemy in enemies)
    return num_fit / len(enemies)

def sort_by_fitness(enemies):
    return sorted(enemies, key=get_enemy_fitness)

def get_fit_enemies(enemies, cutoff):
    fit_enemies = []
    for enemy in enemies:
        if get_enemy_fitness(enemy) < cutoff:
            fit_enemies.append(enemy)
    return fit_enemies

def get_popular_trait(enemies):
    traits = []
    for enemy in enemies:
        traits.append(enemy.trait.name)
    return statistics.mode(traits)

def mutate_traits_pool(enemies, traits_pool):
    trait_names = []
    for enemy in enemies:
        trait_names.append(enemy.trait.name)
    trait_frequencies = Counter(trait_names)
    num_traits = len(trait_names)
    mutated_traits_pool = []
    for trait in traits_pool:
        trait_frequency = statistics.mean([(trait_frequencies[trait[0].name] / num_traits), trait[1]])
        mutated_traits_pool.append([trait[0], trait_frequency])
    return mutated_traits_pool

def mutate_health_pool(enemies, health_pool):
    health_components = []
    for enemy in enemies:
        health_components.append(enemy.health[0])
        health_components.append(enemy.health[1])
    health_component_frequencies = Counter(health_components)
    num_components = len(health_components)
    mutated_health_pool = []
    for num in health_pool:
        health_component_frequency = statistics.mean([(health_component_frequencies[num[0]] / num_components), num[1]])
        mutated_health_pool.append([num[0], health_component_frequency])
    return mutated_health_pool

def get_popular_health_component(enemies):
    components = []
    for enemy in enemies:
        components.append(enemy.health[0])
        components.append(enemy.health[1])
    return statistics.mode(components)

def buff_trait(trait_name, buff_factor, traits_pool):
    if buff_factor == 0:
        return traits_pool
    buffed_traits_pool = []
    nerf_factor = buff_factor / (len(traits_pool) - 1)
    for trait in traits_pool:
        if trait[0].name == trait_name:
            if trait[1] >= 1:
                return traits_pool
            else: 
                buffed_traits_pool.append([trait[0], trait[1] + buff_factor])
        else:
            buffed_traits_pool.append([trait[0], trait[1] - nerf_factor])
    return buffed_traits_pool

def buff_health_component(health_num, buff_factor, health_pool):
    if buff_factor == 0:
        return health_pool
    buffed_health_pool = []
    nerf_factor = buff_factor / (len(health_pool) - 1)
    for health_component in health_pool:
        if health_component[0] == health_num:
            if health_component[1] >= 1:
                return health_pool
            else: 
                buffed_health_pool.append([health_component[0], health_component[1] + buff_factor])
        else:
            buffed_health_pool.append([health_component[0], health_component[1] - nerf_factor])
    return buffed_health_pool

def species_list_init():
    return ["Bullfrog", 
            "Rat", 
            "Bat", 
            "Spider", 
            "Meerkat", 
            "Lizard", 
            "Snake", 
            "Rabbit", 
            "Owl", 
            "Pomeranian"]

def traits_pool_init():
    return [[Trait("Reserved", -1, 2, 0), 0.1],
            [Trait("Brave", 1, 0, -1), 0.1],
            [Trait("Reckless", 2, 0, -1), 0.1],
            [Trait("Cocky", 0, -2, 0), 0.1],
            [Trait("Buff", 1, 1, 2), 0.1],
            [Trait("Cheerful", 0, 0, 0), 0.1],
            [Trait("Lonely", -1, -1, 0), 0.1],
            [Trait("Desperate", 2, 0, -2), 0.1],
            [Trait("Weird", 0, 0, 0), 0.1],
            [Trait("Aloof", -1, 0, 1), 0.1]]

def health_pool_init():
    return [[1, 0.1],
            [2, 0.1],
            [3, 0.1],
            [4, 0.1],
            [5, 0.1],
            [6, 0.1],
            [7, 0.1],
            [8, 0.1],
            [9, 0.1],
            [10, 0.1]]

# Genetic Evolution Program

# Initial Conditions
species_list = species_list_init()
traits_pool = traits_pool_init()
health_pool = health_pool_init()

wb = openpyxl.Workbook()
ws = wb.active
ws.cell(1, 1, "Generation")
ws.cell(1, 2, "Overall Fitness")
col = 3
for trait in traits_pool:
    ws.cell(1, col, trait[0].name)
    col += 1
for num in health_pool:
        ws.cell(1, col, num[0])
        col += 1

percent_fit = 0
num_current_generation = 0
fitness_history = []
num_generation_history = []

# trait frequency tracking
reserved_freq = []
brave_freq = []
reckless_freq = []
cocky_freq = []
buff_freq = []
cheerful_freq = []
lonely_freq = []
desperate_freq = []
weird_freq = []
aloof_freq = []

# health frequency tracking
health_1_freq = []
health_2_freq = []
health_3_freq = []
health_4_freq = []
health_5_freq = []
health_6_freq = []
health_7_freq = []
health_8_freq = []
health_9_freq = []
health_10_freq = []

# setup graphs
plt.ion()
fig=plt.figure()
plt.xlabel('Generation')
plt.ylabel('Percentage')
plt.title('Health Component Frequency')

generation_reset_counter = 0

# Main Loop
print("Welcome to the Creature Evolver!")

generation_size = int(input("Generation Size: "))
generation_limit = int(input("Generation Limit: "))
desired_overall_fitness = int(input("Desired Fitness: "))

while percent_fit < desired_overall_fitness:

    num_generation_history.append(num_current_generation)
    current_generation = generate_enemies(species_list, traits_pool, health_pool, generation_size)
    percent_fit = get_fit_percentage(current_generation)
    fitness_history.append(percent_fit)
    

    # fittest_individuals = get_fit_enemies(current_generation, 2)
    fittest_individuals = sort_by_fitness(current_generation)
    fittest_individuals = fittest_individuals[:generation_size // 2]
    best_trait = get_popular_trait(fittest_individuals)
    best_health_component = get_popular_health_component(fittest_individuals)

    print("Generation: ", end="")
    print(num_current_generation, end=" | ")

    print("Overall Fitness: ", end="")
    print("{:.3f}".format(percent_fit), end=" | ")

    print("Best Health Componenent: ", end="")
    print(best_health_component, end=" | ")

    print("Best Trait: ", end="")
    print(best_trait)

    print("Trait Probabilities: ", end="")
    for trait in traits_pool:
        trait_name = trait[0].name
        trait_freq = trait[1]

        if trait_name == "Reserved":
            reserved_freq.append(trait_freq)
        if trait_name == "Brave":
            brave_freq.append(trait_freq)
        if trait_name == "Reckless":
            reckless_freq.append(trait_freq)
        if trait_name == "Cocky":
            cocky_freq.append(trait_freq)
        if trait_name == "Buff":
            buff_freq.append(trait_freq)
        if trait_name == "Cheerful":
            cheerful_freq.append(trait_freq)
        if trait_name == "Lonely":
            lonely_freq.append(trait_freq)
        if trait_name == "Desperate":
            desperate_freq.append(trait_freq)
        if trait_name == "Weird":
            weird_freq.append(trait_freq)
        if trait_name == "Aloof":
            aloof_freq.append(trait_freq)

        print(trait_name, end=" = ")
        print("{:.3f}".format(trait_freq, 3), end=" | ")
    print("")

    print("Health Probabilities: ", end="")
    for num in health_pool:
        health_name = num[0]
        health_freq = num[1]
        if health_name == 1:
            health_1_freq.append(health_freq)
        if health_name == 2:
            health_2_freq.append(health_freq)
        if health_name == 3:
            health_3_freq.append(health_freq)
        if health_name == 4:
            health_4_freq.append(health_freq)
        if health_name == 5:
            health_5_freq.append(health_freq)
        if health_name == 6:
            health_6_freq.append(health_freq)
        if health_name == 7:
            health_7_freq.append(health_freq)
        if health_name == 8:
            health_8_freq.append(health_freq)
        if health_name == 9:
            health_9_freq.append(health_freq)
        if health_name == 10:
            health_10_freq.append(health_freq)

        print(num[0], end=" = ")
        print("{:.3f}".format(num[1], 3), end=" | ")
    print("\n")


    # export to graphs
    plt.stackplot(num_generation_history, health_1_freq, health_2_freq, health_3_freq, health_4_freq, health_5_freq, health_6_freq, health_7_freq, health_8_freq, health_9_freq, health_10_freq)
    plt.pause(0.01)

    # export to excel
    ws.cell(num_current_generation + 2, 1, num_current_generation)
    ws.cell(num_current_generation + 2, 2, percent_fit)
    col = 3
    for trait in traits_pool:
        ws.cell(num_current_generation + 2, col, trait[1])
        col += 1
    for num in health_pool:
        ws.cell(num_current_generation + 2, col, num[1])
        col += 1

    traits_pool = mutate_traits_pool(fittest_individuals, traits_pool)
    health_pool = mutate_health_pool(fittest_individuals, health_pool)
    num_current_generation += 1
    generation_reset_counter += 1

    if num_current_generation >= 10:
        fitness_rate_of_change = statistics.mean(diff(fitness_history[num_current_generation - 10 : num_current_generation]))

        print("Fitness Rate of Change: ", end="")
        print("{:.3f}".format(fitness_rate_of_change))
        print("\n")

        print("Generation Reset Counter: ", end="")
        print(generation_reset_counter)
        print("\n")

        if abs(fitness_rate_of_change) < 0.001 and generation_reset_counter > 100:
            generation_reset_counter = 0
            traits_pool = traits_pool_init()
            health_pool = health_pool_init()

    if num_current_generation >= generation_limit:
        break

plt.show()

print("\n")
print("The Chosen Ones")
print("Generation: ", end="")
print(num_current_generation)
print("\n")

for enemy in current_generation:
    print(enemy)
print("\n")

wb.save("output.xlsx")
print("Data saved to output.xlsx")




"""
test_enemies = generate_enemies(species_list, traits_pool, health_pool, 100)
test_sorted = sort_by_fitness(test_enemies)
test_fittest = get_fit_enemies(test_enemies)

print(get_fit_percentage(test_enemies))
print(get_popular_trait(test_enemies))
print(get_popular_health_component(test_enemies))

for enemy in test_fittest:
    print(enemy)

for enemy in test_sorted:
    print(enemy)

"""
import gym
import gym_pull
import random
import json

model = 50
largo = 6
num =1000
pressure = 20
mutation_chance = 0.4

def individual(min,max):

    return[random.randint(min,max) for i in range(largo)]

def create_poblation():

    poblacion = []
    for i in range(num):
        individuo = dict()
        individuo['movimientos'] = []
        individuo['fitness'] = 0
        for j in range(largo):
            individuo['movimientos'].append(individual(0,1))
        poblacion.append(individuo)
    return poblacion

def calcularFitness(dist):

    for i in range(len(individual)):
        fitness=0
        if dist == model and model <= 3253:
            model += random.randint(0,50)
            fitness += 1
            print fitness
    return fitness

def selection_and_reproduction(population):
    puntuados = [ [i['fitness'], i] for i in population]
    puntuados = [i[1] for i in sorted(puntuados)]
    population = puntuados


    selected =  puntuados[(len(puntuados)-pressure):]
    best = []
    #best.append(selected)
    datos = json.dumps(selected)
    f = open('best_generation.json', 'w')
    f.write(datos)
    f.close()

    #print selected

    for i in range(len(population)-pressure):
        punto = random.randint(1,largo-1)
        padre = random.sample(selected, 2)
        population[i]['movimientos'][:punto] = padre[0]['movimientos'][:punto]
        population[i]['movimientos'][punto:] = padre[1]['movimientos'][punto:]
    #print "nueva poblacion"

    #print len(population)
    return population

def mutation(population):
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance:
            punto = random.randint(1,largo-1)



            population[i]['movimientos'][punto] = individual(0,1)

    return population

def evaluar_poblacion(env, poblacion):

    for individuo in poblacion:


        for action in individuo['movimientos']:
            env.render()
            #print action
            #[up,down,left,right,a,b]
            observation, reward, done, info = env.step(action)
            if done:
                break
            individuo['fitness'] = info['distance']
        print individuo['fitness']
    return poblacion


env = gym.make('ppaquette/SuperMarioBros-1-1-v0')
#fitness = 0
poblacion = create_poblation()
for i in range(1000):
    observation = env.reset()
    poblacion = evaluar_poblacion(env, poblacion)
    #media_fitness = calcular_fitness_max(poblacion)
    poblacion = selection_and_reproduction(poblacion)
    #population = mutation(population)
    #print len(poblacion[0])
    poblacion = mutation(poblacion)

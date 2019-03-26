import random
import os
import time
#import pyautogui

N = 12;  # Matris Boyutu 11*11'lik matris için 12
K = 30;  # Popülasyon Sayısı
M = int((N * N) / 2 + 1)    # Yol Sayısı
#food = [[1,1], [1,2], [1,3] , [9,9], [4,5]] # Yemeklerin Bulunduğu Yerler
food = [[3,4], [6,4], [8,1] , [8,9], [5,5]]
food_number = len(food)                             # yemek sayısı
location = [6, 6]                           # başlangıç konumu

def reproduce(individual1, individual2):  # crossover fonksiyonu
    ratio = int(len(individual1[0]) / 4)
    child = []
    tmp = []
    k = 0
    for i in range(0, ratio):
        tmp.append(individual1[0][k])
        k += 1
    for i in range(ratio, len(individual1[0])):
        tmp.append(individual2[0][k])
        k += 1
    child.append(tmp)
    child.append(0)
    return child


def selection(population):  # Olasılığa göre birey döndüren fonksiyon
    sum = 0
    pr = []
    p = 0
    for i in population:
        sum += i[1] + 1
        pr.append(sum);

    p = random.randint(1, sum)
    c = 0
    while pr[c] < p:
        c += 1
    return population[c]


def mutation(child):                    # Mutasyona uğratıp birey döndürüyor
    a = int(len(child) / 5) + 1

    for i in range(a):
        p = random.randint(1, 4)
        k = random.randint(0, len(child[0]) - 1)
        child[0][k] = p
    return child


def initialize(K, M):                   # ilk durum için rasgele kromozomlu bireylerin popülasyonunu
    population = []                     # oluşturur
    path = []
    individual = []
    for j in range(K):
        for i in range(M):
            path.append(random.randint(1, 4))
        individual.append(path)
        individual.append(0)
        population.append(individual)
        individual = []
        path = []
    return population


def fitness(individual, location, food, N):     # Uygunluk fonksiyonu bireyin yolunun kaç yemek
    this_food = list(food)                      # yediğini buluyor
    this_location = list(location)
    eaten_food = 0
    for i in individual[0]:
        if i == 1:
            this_location[1] -= 1
        elif i == 2:
            this_location[0] -= 1
        elif i == 3:
            this_location[1] += 1
        else:
            this_location[0] += 1
        if (this_location[0] not in list(range(1, N))) or (this_location[1] not in list(range(1, N))):
            individual[1] = 0
            return individual
        for yum in this_food:
            if this_location == yum:
                eaten_food += 1
                individual[1] = eaten_food
                this_food.remove(yum)
    return individual

def fitnessAll(population, location, food, N):  # tüm popülasyon için fitness fonksiyonunu çağırır
    for individual in population:
        fitness(individual, location, food, N)


def check(population, food):                    # Tüm yiyecekleri yiyen bulundu mu
    a = True
    for individual in population:
        if individual[1] == len(food):
            a = individual
            print("Found")
            return a

    return False


def bestindividual(population):                 # Popülasyondaki En iyi bireyi döndürür
    max = population[0][1]
    best = population[0]
    for i in population:
        if (i[1] > max):
            max = i[1]
            best = i
    return best


def path_to_indices(path,food,location,text):       # Yazdırma Animasyonu
    indices = []
    indices.append(list(location))
    this_location = list(location)
    this_food = list(food)
    for i in path[0]:
        #        print(i)
        if i == 1:
            this_location[1] -= 1
            indices.append(list(this_location))
            print_path2(this_location,N,this_food,'◄',text)

        elif i == 2:
            this_location[0] -= 1
            indices.append(list(this_location))
            print_path2(this_location, N, this_food, '▲',text)
        elif i == 3:
            this_location[1] += 1
            indices.append(list(this_location))
            print_path2(this_location, N, this_food,'►',text)
        else:
            this_location[0] += 1
            indices.append(list(this_location))
            print_path2(this_location, N, this_food, '▼', text)
        if this_location in this_food:
            this_food.remove(this_location)
        if (this_location[0] not in list(range(1, 12))) or (this_location[1] not in list(range(1, 12))):
            print("Dead")
            return;
        if(len(this_food) == 0):
            print_path2(this_location, N, this_food, '*', text)
            print("End Of Animation")
            time.sleep(5)
            return
    time.sleep(5)
    return indices

def print_path2(one_location,N, food,arrow,text):       # Yazdırma Animasyonu
    time.sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')

    print(text, '\n')
    print ('-', end='')
    for i in range(N):
        print ('-', end='')
    for i in range(N+1):
        for j in range(N+1):
            if [i,j]  in food :
                print ("Ф", end='');
            elif ([i,j] ==  one_location):
                print(arrow, end='')
            else:
                print (" ", end='')
        print('\n')
    for i in range(N):
        print ('-', end='')
   



def genetic_algorithm(population, food):        # işi yapan algoritma
    found = False
    k = 0
    bestindividuals = []
    while (found == False and k < 100000):
        k += 1
        if k % 100 == 0:
            print("Generation Count : " + str(k))
            bestindiv = bestindividual(population)
            bestindividuals.append(bestindiv)
        new_population = []
        for i in population:
            x = selection(population)
            y = selection(population)
            child = reproduce(x, y)
            if (random.randint(1, 100) < 20):
                child = mutation(child)
            new_population.append(child)

        population = new_population
        fitnessAll(population, location, food, N)
        found = check(population, food)
        
    print("Genetation Count" + str(k))
    print("Best individual : ")
    print(found)
        
population = initialize(K, M)
genetic_algorithm(population, food)

















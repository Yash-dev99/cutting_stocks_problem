import random
import copy
# problem input
items=[
    {
    "id": "0",
    "L" : 5,
    "W" : 7,
    "n" : 1,
    },
    {
    "id": "1",
    "L" : 7,
    "W" : 0,
    "n" : 1,
    },
    {
    "id": "2",
    "L" : 3,
    "W" : 2,
    "n" : 1,
    },
    {
    "id": "3",
    "L" : 6,
    "W" : 0,
    "n" : 1,
    },
    {
    "id": "4",
    "L" : 8,
    "W" : 3,
    "n" : 1,
    },
    {
    "id": "5",
    "L" : 9,
    "W" : 4,
    "n" : 1,
    },
    {
    "id": "6",
    "L" : 7,
    "W" : 8,
    "n" : 1,
    },
    {
    "id" : "7",
    "L" : 8,
    "W" : 9,
    "n" : 1,
    }
]

max_we=7
min_we=4

max_block=4
num_block=len(items)


# Genetic constant
pop=1000


population=[]
orentation=[]



def fitness_num(people,ore):
    global items
    global max_block
    global max_we
    global min_we
    score=0
    # constrain 1 sum of num < n
    for i in range(num_block):
        for j in range(num_block):
            if people[i][j]<0:
                score+= -9999
    for i in items:
        id=int(i["id"])
        if sum(people[id])>i['n']:
            score+= -9999
    if score<0:
        return score
    for i in people:
        score+=sum(i)
    for i in people:
        flag=True
        for j in i:
            flag=flag and (j==0)
        score+=int(flag)

    # constrain 2 min max for each block
    for j in range(num_block):
        su=0
        c=0
        for i in range(num_block):
            if ore[i][j]==0:
                swi='W'
            else:
                swi='L'
            if items[i][swi]==0 :
                #print(ore[i],swi,items[i][swi],i)
                score+= -9
            su+=items[i][swi]*people[i][j]
            if people[i][j]>0:
                c+=1
        if  su>max_we or c>max_block:
            if c>max_block:
                score+= -1*c*10
            score +=-1*(min(abs(su-min_we),abs(su-max_we)))

    return score



fitness=[]
for _ in range(pop):
    people=[[0 for _ in range(num_block)]
            for j in range(num_block)] # [items][box]
    ori=[]
    for id,i in enumerate(items):
        run=i['n']
        ori_i=[]
        for b in range(num_block):
            people[id][b]=random.randint(0,run)
            run-=people[id][b]
            if items[id]['L']!=0:
                ori_i.append(random.randint(0,1))
            else:
                ori_i.append(0)

        ori.append(ori_i)
    population.append(copy.deepcopy(people))
    orentation.append(copy.deepcopy(ori[:]))
    fitness.append(fitness_num(people,ori[:]))


best=list(range(pop))
best.sort(reverse=True,key=lambda x: fitness[x])
print(population[best[0]])
print(population[best[-1]])
print("fitness : ", max(fitness))

while True:
    fitness=[]
    new_1_population=[]
    new_1_orentation=[]
    for i in range(pop):
        fitness.append(fitness_num(population[i],orentation[i]))


    for _ in range(pop):
        # Tornament based selection
        first=random.choice(range(pop))
        second=random.choice(range(pop))
        if fitness[first]>fitness[second]:
            new_1_population.append(copy.deepcopy(population[first]))
            new_1_orentation.append(copy.deepcopy(orentation[first]))
        else:
            new_1_population.append(copy.deepcopy(population[second]))
            new_1_orentation.append(copy.deepcopy(orentation[second]))

    # elitism
    best=list(range(pop))
    best.sort(reverse=True,key=lambda x: fitness[x])
    print(best)
    print(population[best[0]])
    print(population[best[-1]])
    print("fitness : ", max(fitness))
    new_population=[]
    new_orentation=[]
    for i in best[:int(pop*0.25)]: # 5 percent elitism
        new_population.append(population[i])
        new_orentation.append(orentation[i])


    #mating
    for _ in range(pop-int(pop*0.25)):
        # Tornament based selection
        first=random.choice(range(pop))
        second=random.choice(range(pop))
        child=[]
        ori=[]
        for i in range(num_block):
            if random.random()<0.45:
                child.append(new_1_population[first][i])
                ori.append(new_1_orentation[first][i])
            elif random.random()<0.9:
                child.append(new_1_population[second][i])
                ori.append(new_1_orentation[second][i])
            else:
                child.append([random.randint(0,num_block) for _ in range(num_block)])
                ori.append([random.randint(0,1) for _ in range(num_block)])
        new_population.append(copy.deepcopy(child))
        new_orentation.append(copy.deepcopy(ori))


    population=copy.deepcopy(new_population)
    orentation=copy.deepcopy(new_orentation)
print(population[best[0]])

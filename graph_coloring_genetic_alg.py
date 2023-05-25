import random
from random import choices

neighbors = {
    0:[1,2,3,12,14,15],
    1:[0,2,4,7,8,13,14,15],
    2:[0,1,4,5,3],
    3:[0,2,5,12],
    4:[1,2,5,6,8,9],
    5:[2,4,6,10,12,3],
    6:[4,5,9,10],
    7:[1,8,13],
    8:[1,4,9,11,13,7],
    9:[4,6,10,11,8],
    10:[6,5,12,11,9],
    11:[9,10,12,14,13,8],
    12:[10,5,3,0,14,11],
    13:[7,8,11,14,1],
    14:[11,12,0,15,1,13],
    15:[0,14,1]
}


def fitness(coloring):  
    '''
    Apply a score to each solution , giving a point whenever 2 neighbors have different colors,and deducting 2 points when colors match.
    This means that in the accumulative score a solution gets +2 if two neighbors have different colors and -4 when they have the same,
    since the iteration happens for both neighbors.
    Max score is 84.
    '''
    score=0             
    for i in range(0,16):
        color=coloring[2*i:2*i+2]
        for neighbor in neighbors.get(i):
            neighbor_color=coloring[2*neighbor:2*neighbor+2]
            if color!=neighbor_color:
                score+=1
            else:
                score-=2
    return score

def generate_population(samples_num):   
    '''
    We have 16 graphs and 4 color choices.We represent a coloring by a 32 bit string , with each 2 consecutive bits 
    in i index symbolizing the color of graph i.This function generates (samples_num) random 32 bit strings.
    '''
    
    samples=[]                          
    for i in range(samples_num):
        coloring=f'{random.getrandbits(32):=032b}'
        samples.append(coloring)
        
    return samples

def single_point_crossover(parent_1,parent_2):
    '''
    Gets two samples-colorings as input and crosses them at a single index point (crossover point) , creating two offspring.
    '''  
    crossover_point=random.randint(1,30)
    return (parent_1[0:crossover_point]+parent_2[crossover_point:],parent_2[0:crossover_point]+parent_1[crossover_point:])

def mutate_gene(sample):
    '''
    Reverses a random bit of a sample.
    '''
    point=random.randint(0,31)
    s=sample[point]
    
    if s=='0':
        s='1'
    else:
        s='0'
    return sample[0:point]+s+sample[point+1:]

def start_genetic_alg(epochs,samples_num):
    samples=sorted(generate_population(samples_num),key=lambda genome: fitness(genome),reverse=True)
    weights=[fitness(sample) for sample in samples]
    print(f"Initial population sample has been created,best solution is: {samples[0]} with a score of {weights[0]}")
    for i in range(epochs):
        if fitness(samples[0])>82:
            print(f"Worst solution is {samples[0]} with a score of {fitness(samples[-1])}")
            print(f"A good approximation has been found,its the solution: {samples[0]} which took {i} epochs to be found with a score of {fitness(samples[0])}.")
            print("The coloring is the following:")
            print(result_to_color(samples[0]))
            return
        
        next_samples=[]
        for i in range(int(samples_num/2-1)):
            parents=choices(samples,weights,k=2)
            offspring_1,offspring_2=single_point_crossover(parents[0],parents[1])
            next_samples+=[offspring_1,offspring_2]

        next_samples=sorted(next_samples,key=lambda genome: fitness(genome))
        for i in range(int(samples_num/10)):    #mutate gene on the 10% of the worst solutions
           next_samples[i]=mutate_gene(next_samples[i])
        
        samples=sorted(next_samples,key=lambda genome: fitness(genome),reverse=True)
        weights=[fitness(sample) for sample in samples]

    print(f"Worst solution is {samples[0]} with a score of {fitness(samples[-1])}")
    print(f"A good approximation has been found,its the solution: {samples[0]} which took {epochs} epochs to be found with a score of {fitness(samples[0])}.")
    print("The coloring is the following:")
    print(result_to_color(samples[0]))

def result_to_color(coloring):
    for i in range(0,16):
        if coloring[2*i:2*i+2]=='00':
            print(f"Graph {i} has color blue")
        elif coloring[2*i:2*i+2]=='01':
            print(f"Graph {i} has color red")
        elif coloring[2*i:2*i+2]=='10':
            print(f"Graph {i} has color yellow")
        else: 
            print(f"Graph {i} has color green")

start_genetic_alg(100,1000)


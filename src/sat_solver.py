from z3 import *
import sys
import time
import numpy as np
import argparse

def read_txt(if_name):
    """read instance from input"""
    n = 0
    paper_shape = []
    present_shape = []
    input_file = open(if_name,'r')
    i = 0

    for line in input_file:

        if i > 1:

            i += 1
            line = line.strip().split(' ')
            if len(line) < 2:
                break
            present_shape.append([int(e) for e in line])

        if i == 1:
            i += 1
            line = line.strip()
            n = int(line)

        if i == 0:
            i += 1
            line = line.strip().split(' ')
            paper_shape = [int(e) for e in line]

    input_file.close()
    return n, paper_shape, present_shape

parser = argparse.ArgumentParser(description='Present wrapping problem SAT solver')
parser.add_argument('input_file', help='input instance file in txt format')
args = parser.parse_args()
if_name = args.input_file

n, paper_shape, present_shape = read_txt(if_name)
print(n, paper_shape, present_shape)

present_area = np.sum([present_shape[i][0] * present_shape[i][1] for i in range(n)])
paper_area = paper_shape[0] * paper_shape[1]
print('present area:',present_area,'paper area:',paper_area)
t_start = time.time()
s = Solver()

# use a numpy 3d array to store the Z3 boolean variables
# the first dimension represents a complete 2d layer for each present
# the last 2 dimensions are the 2d coordinates of each available position

pos = np.empty((n, paper_shape[0], paper_shape[1]), dtype=object)

# model variables definition
for i in range(paper_shape[0]):
    for j in range(paper_shape[1]):
        for k in range(n): # layers
            pos[k,i,j] = Bool('p'+str(k)+str(i)+str(j))
        # non-overlapping constraint
        # at most one layer is occupied in i,j for each 2d position

        notoverlap = Not(Or(*[And(pos[k1,i,j], pos[k2,i,j]) for k1 in range(n) for k2 in range(k1+1,n)]))
        s.add(notoverlap)

        # total area occupation assumption:
        # at least one layer is occupied for each 2d position
        if present_area == paper_area:
            o = Or([pos[k,i,j] for k in range(n)])
            s.add(o)

# the convolutions

# for each layer
# exactly one set of variables representing that rectangular present must be true
# meaning that the layer effectively represents the present

for k in range(n):
    conj = []
    for i in range(paper_shape[0]-present_shape[k][0]+1):
        for j in range(paper_shape[1]-present_shape[k][1]+1):
            # for each possible present position in its layer

            occupations = []
            for x in range(paper_shape[0]):
                for y in range(paper_shape[1]):
                    if (i <= x < i+present_shape[k][0] and j<= y < j+present_shape[k][1]):
                        occupations.append(pos[k,x,y])
                    else:
                        occupations.append(Not(pos[k,x,y]))

            conj.append(And(*occupations))

    # at least one
    disj = Or(*conj)
    s.add(disj)

    # at most
    conj_pairs = [And(conj[i],conj[j]) for i in range(len(conj)) for j in range(i) if i != j]
    s.add((Not(Or(*conj_pairs))))


print("compiled in:", time.time()-t_start)
print("traversing model...")
t_start = time.time()
print(s.check())
for k, v in s.statistics():
    print(k, v)
print("solved in:", time.time()-t_start)

# visualize solution
pos_vis = np.zeros((n, paper_shape[0], paper_shape[1]), dtype=int)
m = s.model()
for k in range(n):
    for i in range(paper_shape[0]):
        for j in range(paper_shape[1]):
            if m[pos[k,i,j]]:
                pos_vis[k,i,j] = 1
            else:
                pos_vis[k,i,j] = 0

def visual(pos):
    for i in range(paper_shape[0]):
        row = ''
        for j in range(paper_shape[1]):
            if pos[j,paper_shape[0]-i-1] == 1:
                row += "# "
            elif pos[j,paper_shape[0]-i-1] == 0:
                row += ". "
            else:
                row += 'o '
        print(row)
    print()

for p in pos_vis:
    visual(p)

print('sum to:')
visual(np.sum(pos_vis, axis = 0))
print('legend:')
print('. - empty', '# - occupied', 'o - overlap', sep = '\n')

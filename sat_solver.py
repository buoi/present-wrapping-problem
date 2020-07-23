from z3 import *
import sys
import time
import numpy as np
from PIL import Image, ImageDraw

t_start = time.time()
def read_txt(if_name):

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

if_name = sys.argv[1]
n, paper_shape, present_shape = read_txt(if_name)
print(n, paper_shape, present_shape)

s = Solver()

pos = np.empty((n, paper_shape[0], paper_shape[1]), dtype=object)


# variable creation
for i in range(paper_shape[0]):
    for j in range(paper_shape[1]):
        for k in range(n):
            #print(k,i,j)
            pos[k,i,j] = Bool('p'+str(k)+str(i)+str(j))
        # non-overlapping constraint
        # at most one layer is occupied for each 2d position

        notoverlap = Not(Or(*[And(pos[k1,i,j], pos[k2,i,j]) for k1 in range(n) for k2 in range(k1)]))
        #print(notoverlap)
        s.add(notoverlap)

        # total area occupation assumption: ===>  NO VALID FOR PERIMETER
        # at least one layer is occupied for each 2d position
        #s.add(Or([pos[k,i,j] for k in range(n)]))


# the convolutions
# for each layer/shape
# at least one set of variables representing one rect present must be all ture
# meaning that the layer represents effectively a present
# here the at most is mandatory

for k in range(n):
    conj = []
    for i in range(paper_shape[0]-present_shape[k][0]+1): # +1 perchè l'occupazione deve arrivare in fondo!
        for j in range(paper_shape[1]-present_shape[k][1]+1):
            # at least
            tmp = []
            tmp += [pos[k,x,j] for x in range(i,i+present_shape[k][0])]
            tmp += [pos[k,x,j+present_shape[k][1]-1] for x in range(i,i+present_shape[k][0])]
            tmp += [pos[k,i,y] for y in range(j+1,j+present_shape[k][1])]
            tmp += [pos[k,i+present_shape[k][0]-1,y] for y in range(j+1,j+present_shape[k][1])]
            conj.append(And(*tmp))

    # at least
    disj = Or(*conj)
    s.add(disj)

    # at most
    cc = [And(conj[i],conj[j]) for i in range(len(conj)) for j in range(i) if i != j]
    print(cc)
    s.add((Not(Or(*cc))))


print("compiled in:", time.time()-t_start)
print("traversing model...")
t_start = time.time()
print(s.check())
print(s.unsat_core())
print("solved in:", time.time()-t_start)

m = s.model()
for k in range(n):
    for i in range(paper_shape[0]):
        for j in range(paper_shape[1]):
            print('#',end = '') if m[pos[k,i,j]] else print('.',end = '')
        print()
    print()




"""
for d in sorted(m.decls(), key=lambda x: (int(x.name()[1:]), x.name()[0])):
    print("%s = %s" % (d.name(), m[d]))
    solution.append(m[d].as_long())

solution = [(solution[i*2],solution[i*2+1]) for i in range(len(solution)//2)]
print(solution)
print(present_shape)

scale = 20
img = Image.new("RGB", (scale * paper_shape[0], scale *paper_shape[1]))

import random
number_of_colors = n

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

for i,s in enumerate(solution):
    img1 = ImageDraw.Draw(img)
    img1.rectangle([(scale*s[0],scale*(paper_shape[1]- s[1])),(scale*(s[0]+ present_shape[i][0])-1, scale*(paper_shape[1] - present_shape[i][1]- s[1]))],
    fill = color[i])

img.show()


"""
"""
rects = []
for i,coord in enumerate(solution):
    rects.append(patches.Rectangle((coord[0],coord[1]),
    present_shape[i][0],present_shape[i][1], linewidth = 3))

# Create figure and axes
fig,ax = plt.subplots(1)

#ax.add_patch(patches.Rectangle((0,0), paper_shape[0],paper_shape[1]))

plt.Line2D((0,0),(paper_shape[0],paper_shape[1]))
# Add the patch to the Axes
for rect in rects:
    ax.add_patch(rect)

plt.show()
"""

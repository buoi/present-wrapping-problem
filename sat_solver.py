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
present_pos = []

# variable creation
for i in range(paper_shape[0]):
    for j in range(paper_shape[1]):
        for k in range(n):
            pos[k,i,j] = Bool('p'+str(k)+str(i)+str(j))
        # non-overlaping constraint
        s.add(Not(Or(*[And(pos[k1,i,j],pos[k2,i,j]) for k1 in range(k) for k2 in range(k1)])))

# the convolutions
for k in range(n):
    a = []
    for i in range(paper_shape[0]-present_shape[k][0]):
        for j in range(paper_shape[1]-present_shape[k][1]):
            print(k,i,j)
            a.append(And([And(pos[k,i,j],pos[k,x,y]) for x in range(i+1,i+present_shape[k][0]) for y in range(j+1,j+present_shape[k][1])]))
    print(a)
    s.add([Or(ai) for ai in a])


print("compiled in:", time.time()-t_start)

t_start = time.time()
print(s.check())
print("solved in:", time.time()-t_start)

m = s.model()
for k in range(n):
    for i in range(paper_shape[0]):
        for j in range(paper_shape[1]):
            print('#',end = '') if m[pos[k,i,j]] else print('.',end = '')
        print()
    print()

print("traversing model...")
solution = []

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

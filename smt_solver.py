from z3 import *
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw

import time

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
present_pos = []

for i in range(n):
    present_pos.append((Int('x'+str(i)), Int('y'+str(i))))
    for j in range(2):
        s.add(0 <= present_pos[i][j], present_pos[i][j] <= paper_shape[j] - present_shape[i][j])

# per ogni pezzo: x di uno non nell'intervallo x di un altro di cui condivide al y
for i in range(n):
    for j in range(i):
        s.add(Or(Or(present_pos[i][0] + present_shape[i][0] <= present_pos[j][0],
        present_pos[i][0] >= present_pos[j][0] + present_shape[j][0]),
        Or(present_pos[i][1] + present_shape[i][1] <= present_pos[j][1],
        present_pos[i][1] >= present_pos[j][1] + present_shape[j][1])))

print("compiled in:", time.time()-t_start)

t_start = time.time()
print(s.check())
print("solved in:", time.time()-t_start)
m = s.model()

print("traversing model...")
solution = []
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

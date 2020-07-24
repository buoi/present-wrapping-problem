from z3 import *
import sys
import numpy as np
import time, datetime


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

if_name = sys.argv[1]
if sys.argv[-1] == 'y':
    vis_image_out = True
else:
    vis_image_out = False

n, paper_shape, present_shape = read_txt(if_name)
print(n, paper_shape, present_shape)

# model description
t_start = time.time()

s = Solver()
present_pos = []

# add present_pos variables to the model
# constraint coordinates to not exceed the available paper
for i in range(n):
    present_pos.append((Int('x'+str(i)), Int('y'+str(i))))
    for j in range(2):
        s.add(0 <= present_pos[i][j], present_pos[i][j] <= paper_shape[j] - present_shape[i][j])

# non-overlapping constraint: each pair of presents must not overlap
for i in range(n):
    for j in range(i): # does not repeat pairs ij, ji

        s.add(Or(present_pos[i][0] + present_shape[i][0] <= present_pos[j][0],
        present_pos[i][0] >= present_pos[j][0] + present_shape[j][0],
        present_pos[i][1] + present_shape[i][1] <= present_pos[j][1],
        present_pos[i][1] >= present_pos[j][1] + present_shape[j][1]))

# implied constraint for each row and column
for k in (0,1):
    for j in range(paper_shape[k]):
        partial_sum = []
        for i in range(n): # check present column/row occupation
            inc = If(And(present_pos[i][k] <= j, present_pos[i][k] + present_shape[i][k] > j), present_shape[i][1-k], 0)
            partial_sum.append(inc)

        s.add(sum(partial_sum) <= paper_shape[k])

print("compiled in:", time.time()-t_start)

# solving
print("traversing model...")
t_start = time.time()
print(s.check())

for k, v in s.statistics():
    print(k, v)

print("solved in:", time.time()-t_start)
m = s.model()

solution = []

# sort decision variables by name
for d in sorted(m.decls(), key=lambda x: (int(x.name()[1:]), x.name()[0])):
    #print("%s = %s" % (d.name(), m[d]))
    solution.append(m[d].as_long())

# transform in list of (x,y) pairs
solution = [[solution[i*2], solution[i*2+1]] for i in range(len(solution)//2)]

print("solution:",solution)
print("shapes:  ",present_shape)

# visualization by numpy array
pos = np.zeros((n, paper_shape[0], paper_shape[1]), dtype=int)

for i,s in enumerate(solution):
    pos[i, s[0]:s[0] + present_shape[i][0], s[1]:s[1] + present_shape[i][1]] = 1

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

for p in pos:
    visual(p)

# save result to output file
"""
of_name = if_name.strip('.txt')+'-out.txt'

with open(of_name,'w') as f:
    f.write(str(paper_shape[0])+' '+str(paper_shape[1])+'\n')
    f.write(str(n)+'\n')
    for shape, sol in zip(present_shape,solution):
        f.write(f"{shape[0]} {shape[1]}\t{sol[0]} {sol[1]}\n")
"""

print('sum to:')
visual(np.sum(pos, axis = 0))
print('legend:')
print('. - empty', '# - occupied', 'o - overlap', sep = '\n')

# visualization by image
if vis_image_out:
    from PIL import Image, ImageDraw
    scale = 1
    img = Image.new("RGB", (scale * paper_shape[0], scale *paper_shape[1]))

    rgb = [(0*i//n,100*i//n,255*i//n) for i in range(1,n+1)]

    for i,s in enumerate(solution):

        print(s)
        img1 = ImageDraw.Draw(img)
        img1.rectangle([
        (s[0], paper_shape[1] - s[1]-1), # left-top from 0 to paper_shape
        (s[0] + present_shape[i][0]-1, paper_shape[1] - (s[1] + present_shape[i][1]))], fill = rgb[i])

    img.show()

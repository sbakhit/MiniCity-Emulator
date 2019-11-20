import csv
import random

routes = {}
for i in range(10):
    routes[i] = [(random.randrange(0, 1024), random.randrange(0, 1024))]
    #print(routes[i])

# points = routes[0]
# points.append(((points[0][0]+5),(points[0][1]+5)))
# print(points)

for obj, pts in routes.items():
    for i in range(5):
        r = random.randrange(0, 2)

        i, j = pts[-1]
        pts.append((i + (1 - r), j + r))

# for i in range(50):
#     '''
#     4 options
#         1. (i+1, j)
#         2. (i, j+1)
#     '''
#     points.append(((points[i][0]+5),(points[i][1]+5)))
points = routes[0]
print(points)

with open('config.tsv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in routes.items():
       writer.writerow([key, value])

print(routes)

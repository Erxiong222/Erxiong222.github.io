
n, m, x, y, z = map(int, input().split(' '))
map = []
pos = {}
for i in range(n):
    map.append(input())
    for j in range(m):
        pos[map[i][j]] = (i, j)

target = input()
cur = (0, 0)
cost = 0
for s in target:
    px, py = pos[s]
    cost += (0 if (cur[0] == px or cur[1]== py) else y) + x*(abs(py-cur[1])))
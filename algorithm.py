from collections import deque
import random
import time
import numpy as np


#Генератор случайного графа

def r_graph(n):
    g = [0 for i in range(n)]
    for i in range(n):
        g[i] = []
    for i in range(n):
        for j in range(i + 1, n):
            if (random.random() > 0.5):
                g[i] += [j]
                g[j] += [i]
    return g


def least_common_ancestor(a, b):
    global used
    global base
    global match
    global p
    used = np.zeros(n)
    # от вершины a до корня, помечая все чётные вершины
    while (1):
        a = base[int(a)]
        used[a] = True
        if (match[a] == -1):
            break
        a = p[int(match[a])]
    # Поднимаемся от вершины до нахождения помеченной вершины
    while (1):
        b = base[int(b)]
        if (used[b]):
            return b
        b = p[int(match[b])]


def mark_path(v, b, children):
    global base
    global blossom
    global match
    global p
    while (base[int(v)] != b):
        blossom[int(base[int(v)])] = blossom[int(base[int(match[int(v)])])] = True
        p[int(v)] = children
        children = match[int(v)]
        v = p[int(match[int(v)])]


def path_finding_function(root):
    global used
    global base
    global match
    global p
    global g
    global blossom
    used = np.zeros(n)
    p = np.ones(n) * (-1)
    for i in range(n):
        base[i] = i

    used[root] = True
    q = deque()
    q.append(root)
    while (len(q) != 0):
        v = int(q.popleft())
        for i in range(len(g[v])):
            to = g[v][i]
            if ((base[v] == base[to]) or (match[v] == to)):
                continue
            if ((to == root) or (match[int(to)] != -1) and (p[int(match[int(to)])] != -1)):
                curbase = least_common_ancestor(v, to)
                blossom = np.zeros(n)
                mark_path(v, curbase, to)
                mark_path(to, curbase, v)
                for i in range(n):
                    if (blossom[base[i]]):
                        base[i] = curbase
                        if (not(used[i])):
                            used[i] = True
                            q.append(i)
            else:
                if (p[to] == -1):
                    p[to] = v
                    if (match[to] == -1):
                        return to
                    to = match[to]
                    used[int(to)] = True
                    q.append(to)
    return -1


def edmonds_function(g):
    global p
    global match
    for i in range(n):
        if (match[i] == -1):
            v = path_finding_function(i)
            while (v != -1):
                pv = p[int(v)]
                ppv = match[int(pv)]
                match[int(v)] = pv
                match[int(pv)] = v
                v = ppv
    #print("Максимальное паросочетание: ")
    #for ind, item in enumerate(match):
     #   print("{}:{}".format(ind, int(item)))


if __name__ == '__main__':
    n = 10
    while n <= 510:
        mid = []
        for j in range(10):
            #print("Списки смежности:")
            #print(g)
            g = r_graph(n)
            p = np.empty(n)
            match = np.ones(n) * (-1)
            base = [i for i in range(n)]
            used = np.empty(n)
            blossom = np.empty(n)
            time_start = time.time()
            edmonds_function(g)
            mid.append(time.time() - time_start)
        t = sum(mid)/10
        print("n: ", n, "Time: ", t)
        n += 20
        j = 0
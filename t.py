import numpy as np
from random import choice, random, shuffle
from collections import Counter
import re

if 0:
    words = "000 11111 2222222".split()
    chars = set()
    for w in words:
        chars.update(w)
    chars = "".join(chars)
    data = "".join(choice(words) for _i in range(100))
    print data
else:
    data = file('alice.txt').read()
    data = data.lower()
    data = re.sub("[^a-z]+", " ", data)
    chars = set(data)
    chars = "".join(chars)


class Node(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.children = [None] * len(chars)
        self.words = [0] * len(chars)
        self.stop = 0
        self.through = 0
        self.ncount = 0
        self.ntable = 0  # ??
        self.id = 0  # need?

    def prob_stop(self):
        return np.random.beta(self.stop + 1, self.through + 1)

def char2int(c):
    return chars.index(c)

root = Node()
order = [0] * len(data)

def add_cunstomer(index):
    cur = root
    customer = char2int(data[index])
    i = index
    o = 0
    while True:
        if i < 0 or cur.prob_stop() > random() or o > 8:
            # stop here
            cur.stop += 1
            cur.words[customer] += 1
            cur.ncount += 1
            order[index] = o
            # ntable?
            # add proxy
            cur = cur.parent
            while cur:
                cur.through += 1
                cur.words[customer] += 1
                cur = cur.parent
            break
        x = char2int(data[i - 1])
        child = cur.children[x]
        if not child:
            child = cur.children[x] = Node(cur)
        i -= 1
        cur = child
        o += 1

def remove_cunstomer(index):
    o = order[index]
    customer = char2int(data[index])
    cur = root
    for i in range(o):
        cur.through -= 1
        cur.words[customer] -= 1
        c = data[index - i - 1]
        cur = cur.children[char2int(c)]

    cur.stop -= 1
    cur.words[customer] -= 1
    order[index] = 0

for i in range(10, len(data)):
    add_cunstomer(i)

print Counter(order)

for j in range(100):
    indexes = range(10, len(data))
    shuffle(indexes)
    for i in indexes:
        remove_cunstomer(i)
        add_cunstomer(i)
    print Counter(order)

print Counter(order)

# TODO: find d, theta, thw, th

def get_prob(w, h):
    raise NotImplemented  # find node
    prob = float(cur.words[w] - d * thw) / (theta + cur.ncount)
    if cur.parent:
        parent_prob = cur.parent.get_prob()
    else:
        parent_prob = 1.0 / len(chars)
    prob += float(theta + d * th) / (theta + cur.ncount) * parent_prob
    return prob

def get_perplexity():
    raise NotImplemented



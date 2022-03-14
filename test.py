import math

max = 19
min = 8

l1 = list(range(min, max+1))
l2 = []
while l1:
    l2.append(l1.pop(int(len(l1)/2)))

print(l2)



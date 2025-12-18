import random
min = 10
max = 0
for i in range(15):
    x= random.gauss(3, 0.4)
    if x > max:
        max = x
    if x < min:
        min = x

print("min : "+str(min))
print("max : "+str(max))

list1 = [0]*10000 # Creates a list with 10 000 zeros

# Print something
def printSomething(something):
    print(something)

# Sum all the numbers from 0 to 100
sum = 0
for num1 in range(0, 100, 10):
    for num2 in range(10):
        sum+=num1+num2

# Loops until it reaches a non zero number in the list
list1[3422]=1
index = 0
while not list1[index]:
    index+=1

printSomething(tuple(list1[0:5]))
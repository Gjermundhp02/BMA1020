 	
def counter(someList):
    return len([n for index, n in enumerate(someList[1:-1]) if someList[index]<n and someList[index+2]<n])

manyLists = [[3, 7, 3, 9, 7, 8, 5, 4, 10, 1, 5, 9, 1, 2, 9, 5, 9, 2, 10, 8], [8, 10, 3, 1, 2, 1, 8, 2, 1, 6, 3, 6, 6, 10, 8, 10, 10, 8, 5, 2], [10, 2, 9, 1, 1, 5, 1, 4, 9, 7, 7, 9, 7, 7, 9, 7, 8, 5, 5, 2], [6, 1, 6, 9, 10, 6, 8, 8, 1, 2, 3, 5, 10, 2, 5, 2, 2, 1, 4, 4], [2, 7, 1, 8, 1, 4, 2, 8, 1, 6, 2, 10, 2, 4, 2, 7, 8, 7, 7, 3], [2, 2, 9, 8, 3, 7, 8, 8, 3, 9, 5, 1, 9, 5, 2, 5, 6, 1, 1, 6], [6, 4, 10, 2, 1, 5, 5, 7, 3, 4, 1, 1, 3, 6, 7, 9, 3, 1, 1, 2], [4, 7, 10, 7, 2, 4, 1, 5, 1, 3, 8, 10, 3, 8, 9, 4, 10, 4, 6, 2], [5, 10, 7, 9, 5, 5, 8, 3, 5, 8, 6, 7, 9, 2, 8, 8, 1, 3, 4, 8], [7, 3, 4, 8, 5, 4, 7, 4, 4, 6, 10, 5, 10, 9, 6, 9, 10, 10, 10, 7], [5, 8, 3, 2, 9, 6, 6, 1, 7, 2, 3, 9, 1, 1, 1, 4, 9, 2, 4, 8], [6, 7, 3, 3, 2, 2, 10, 9, 10, 10, 9, 5, 2, 2, 1, 7, 1, 4, 7, 8], [8, 7, 3, 5, 6, 2, 10, 5, 6, 9, 10, 9, 2, 6, 6, 6, 6, 1, 5, 8], [1, 5, 5, 5, 1, 8, 8, 4, 9, 9, 10, 10, 4, 9, 2, 7, 2, 10, 7, 7], [10, 4, 1, 7, 8, 1, 9, 5, 6, 2, 7, 5, 4, 2, 10, 10, 7, 6, 10, 6], [8, 2, 4, 6, 2, 1, 5, 7, 6, 3, 2, 1, 3, 5, 5, 4, 5, 9, 1, 10], [5, 9, 5, 3, 4, 4, 2, 8, 2, 2, 9, 7, 9, 10, 10, 3, 4, 3, 10, 10], [8, 2, 3, 6, 9, 6, 6, 5, 8, 7, 10, 3, 4, 10, 10, 2, 5, 9, 3, 7], [4, 4, 10, 4, 9, 7, 3, 8, 8, 1, 4, 1, 1, 4, 2, 1, 7, 8, 2, 5], [5, 9, 9, 9, 5, 9, 6, 5, 1, 7, 6, 3, 1, 3, 7, 7, 2, 4, 3, 5]]
answer = [counter(l) for l in manyLists]
print(answer)
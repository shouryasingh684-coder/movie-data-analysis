import numpy as np

ratings = np.array([8.8, 6.7, 8.9, 7.3, 4.5, 9.2, 8.6, 5.6])
print("Shape: ", ratings.shape)
print("Mean: ", ratings.mean(), "Max: ", ratings.max())
print(ratings + 1)
print(ratings * 10)
# counts the number of film that have rating above 7
print((ratings > 7).sum()) 
print(ratings[ratings > 7])

money = np.array([[100,450],
                  [20,15],
                  [40,45],
                  [56,78]])

print(money[:, 0])
profit = money[:, 1] - money[:, 0]
print("Profit: ", profit)
print("Column mean: ", money.mean(axis = 0))
print("Row mean: ", money.mean(axis = 1))
print(profit[profit > 0])

# checking what i learned 

import time
big = np.random.rand(1_000_000)
start = time.time()
result = [x * 2 for x in big]
print("Loop: " , time.time() - start)
start = time.time()
result = big * 2
print("Numpy: ", time.time() - start)
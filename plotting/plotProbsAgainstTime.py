import matplotlib.pyplot as plt

xs = [2016, 2018, 2019, 2020, 2021, 2022, 2023]
ys = [0.8816, 0.8131, 0.6616, 0.8629, 0.8510, 0.8463, 0.6067]

plt.figure()
plt.ylim(0, 1)
plt.xlabel('year')
plt.ylabel('$p_{success}$')
plt.grid()
plt.plot(xs, ys, 'ko')
plt.plot([2016, 2022], [0.8816, 0.8463], 'r:')
plt.show()














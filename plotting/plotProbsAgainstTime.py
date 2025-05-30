import matplotlib.pyplot as plt

xs = [2016, 2018, 2019, 2020, 2021, 2022, 2023]
ys = [0.8023, 0.8071, 0.6921, 0.8311, 0.8619, 0.8668, 0.6306]

plt.figure()
plt.ylim(0, 1)
plt.xlabel('year')
plt.ylabel('$p_{success}$')
plt.grid()
plt.plot(xs, ys, 'ko')
# plt.plot([2016, 2022], [0.8816, 0.8463], 'r:')
# plt.hlines(0.8332, 2016, 2023, 'r', 'dashed')
plt.show()














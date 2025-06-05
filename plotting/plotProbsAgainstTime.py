import matplotlib.pyplot as plt

xs = [2016, 2018, 2019, 2020, 2021, 2022, 2023]
ys = [0.5501, 0.5557, 0.4718, 0.5817, 0.6111, 0.6269, 0.3996]

plt.figure()
plt.ylim(0, 1)
plt.xlabel('year')
plt.ylabel('$p_{success}$')
plt.grid()
plt.plot(xs, ys, 'ko')
# plt.plot([2016, 2022], [0.8816, 0.8463], 'r:')
# plt.hlines(0.8332, 2016, 2023, 'r', 'dashed')
plt.show()














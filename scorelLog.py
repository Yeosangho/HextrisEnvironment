import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('./log/score_log.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x,y, label='score')
plt.xlabel('game episode')
plt.ylabel('score')
plt.title('Score of Hextris Web Game')
plt.legend()
plt.show()
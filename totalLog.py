import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('./log/total_log.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[2]))

plt.plot(x,y, label='reward')
plt.xlabel('game episode')
plt.ylabel('reward')
plt.title('The Sum of Reward of DRQN Agent')
plt.legend()
plt.show()
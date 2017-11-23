import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('./log/total_log.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    sumScore = 0
    for row in plots:
        sumScore = sumScore + float(row[1])
        if(int(row[0])%1== 0):
            x.append(row[0])
            y.append(float(sumScore))
            sumScore = 0


plt.plot(x,y, label='reward')
plt.xlabel('game episode')
plt.ylabel('reward')
plt.title('The Sum of Reward of DRQN Agent')
plt.legend()
plt.show()
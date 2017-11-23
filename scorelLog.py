import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('./log/score_log.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    sumScore = 0
    for row in plots:
        sumScore = sumScore + int(row[1])
        if(int(row[0])%2000== 0):
            x.append(int(row[0]))
            y.append(sumScore)
            sumScore = 0

plt.plot(x,y, label='score')
plt.xlabel('game episode')
plt.ylabel('score')
plt.title('Score of Hextris Web Game')
plt.legend()
plt.show()
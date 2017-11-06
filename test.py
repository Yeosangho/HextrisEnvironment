import env
import random
from threading import Timer
import time

#env.test()

env.openGame()
env.startGame()
env.step(0)
doneDoubled = 0;
combo = 0
count = 0
episode = 0

def resetCombo():
    global combo
    print( 'combo reset')
    combo = 0
comboTimer = Timer(3, resetCombo)

while(True):
    startTime = time.time()
    count = count + 1
    action = int(random.random() * 3)
    env.render()
    state, reward, done = env.step(0)

    if done:
        print("game over!!")
        combo = 0
        if comboTimer.is_alive:
            comboTimer.cancel()
        env.startGame()
        doneDoubled = doneDoubled + 1
    else :
        doneDoubled = 0
    if(doneDoubled > 1):
        print('done error!!')

    if(count%200 == 0):
        episode = episode + 1
        print("##########", episode, "episode ################")
        print("score :", env.getScore())
        env.printGrid(state)

    if reward:
        combo = combo +1
        if(combo >= 1):
            #if(combo > 1) :
                #print(combo, 'combo!!')
            if comboTimer.is_alive :
                comboTimer.cancel()
            comboTimer = Timer(3, resetCombo)
            comboTimer.start()

    endTime = time.time()
    if(count % 100 == 0):
        print(endTime - startTime)



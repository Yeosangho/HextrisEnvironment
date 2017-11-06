import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt
import scipy.misc
import os
import csv
import itertools
import tensorflow.contrib.slim as slim


# This is a simple function to reshape our game frames.
def processState(state1):
    return np.reshape(state1, [2304])


# These functions allows us to update the parameters of our target network with those of the primary network.
def updateTargetGraph(tfVars, tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx, var in enumerate(tfVars[0:total_vars // 2]):
        op_holder.append(tfVars[idx + total_vars // 2].assign(
            (var.value() * tau) + ((1 - tau) * tfVars[idx + total_vars // 2].value())))
    return op_holder


def updateTarget(op_holder, sess):
    for op in op_holder:
        sess.run(op)
    total_vars = len(tf.trainable_variables())
    a = tf.trainable_variables()[0].eval(session=sess)
    b = tf.trainable_variables()[total_vars // 2].eval(session=sess)
    if a.all() == b.all():
        print("Target Set Success")
    else:
        print("Target Set Failed")


# Record performance metrics and episode logs for the Control Center.
def saveToCenter(i, rList, jList, bufferArray, summaryLength, h_size, sess, mainQN, time_per_step):
    with open('./log/total_log.csv', 'a') as myfile:
        state_display = (np.zeros([1, h_size]), np.zeros([1, h_size]))
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([i, np.mean(jList[-100:]), np.mean(rList[-summaryLength:])])
        myfile.close()
    with open('./log/frames/log' + str(i) + '.csv', 'w') as myfile:
        state_train = (np.zeros([1, h_size]), np.zeros([1, h_size]))
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(["ACTION", "REWARD", "A0", "A1", 'A2', 'V'])
        a, v = sess.run([mainQN.Advantage, mainQN.Value], \
                        feed_dict={mainQN.scalarInput: np.vstack(bufferArray[:, 0]) / 6.0,
                                   mainQN.trainLength: len(bufferArray), mainQN.state_in: state_train,
                                   mainQN.batch_size: 1})
        wr.writerows(zip(bufferArray[:, 1], bufferArray[:, 2], a[:, 0], a[:, 1], a[:, 2], v[:, 0]))



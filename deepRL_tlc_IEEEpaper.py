"""
Katie Rouse - 12/12/2019
Compiled code for DeepRL example with Testbed Experience Buffer
"""
from __future__ import division

import numpy as np
import pandas as pd
import random
import tensorflow as tf
import tensorflow.contrib.slim as slim
#import matplotlib.pyplot as plt
import scipy.misc
import os
import scipy.stats as ss
import math
from experience import Experience
#matplotlib inline

var1 = 100
var2 = 100
mult = var1 * var2
#csv_buffer = pd.read_csv('filled_buffer.csv',engine = "python")
#print(csv_buffer)

# Class of dueling DQN with three convolutional layers
class Qnetwork():
    # receives a state from the sumo, flattenes into an array
    # then resizes it and process through 3 conv layers
   
    def __init__(self,h_size,action_num):
        # the number of grids at an intersection is 60 x 60
        # input data become 60 x 60 x 2 w/ both positon and speed info
        
        # tf.placeholder inserts a placeholder for a tensor that will always be fed
        # returns a Tensor that may be used as a handle for feeding a value, not evaluated directly
        self.scalarInput = tf.placeholder(shape=[None,mult,2],dtype=tf.float32)
        self.legal_actions = tf.placeholder(shape=[None,action_num], dtype=tf.float32)
        
        self.imageIn = tf.reshape(self.scalarInput, shape=[-1,var1,var2,2])
        
        # first conv layer contains: 32 filters, filter size 4x4, stride 2x2
        self.conv1 = slim.conv2d(inputs=self.imageIn,num_outputs=32,kernel_size=[4,4],stride=[2,2],padding='VALID', activation_fn=self.relu, biases_initializer=None)
        
        # second conv layer contains: 64 filters, size 2x2, stride 2x2
        ### in the paper it says stride 2x2 but in the sample code it has stride 1,1 ???
        self.conv2 = slim.conv2d(inputs=self.conv1,num_outputs=64,kernel_size=[2,2],stride=[1,1],padding='VALID', activation_fn=self.relu, biases_initializer=None)
       
        # size of the output after 2 convolution layers is 15 x 15 x 64
        # third conv layer has 128 filters, filter size 2x2, and stride size 1x1
        self.conv3 = slim.conv2d(inputs=self.conv2,num_outputs=128,kernel_size=[2,2],stride=[1,1],padding='VALID', activation_fn=self.relu, biases_initializer=None)
       
        
        # third conv layer output is 15 x 15 x 128 tensor
        # a fully-connected layer transfers the tensor into a 128x1 matrix
       
        # it is split into Value and Advantage w/ same size 64x1
        self.stream = slim.flatten(self.conv3)
        self.stream0 = slim.fully_connected(self.stream, 128, activation_fn=self.relu)
        
        self.streamA = self.stream0
        self.streamV = self.stream0
        
        # part one, used to calculate value
        self.streamA0 = slim.fully_connected(self.streamA,h_size, activation_fn=self.relu)
        # part two, used to for the advantage (advantage of an action means how well it can achieve by taking an action over all the other actions)
        self.streamV0 = slim.fully_connected(self.streamV, h_size, activation_fn = self.relu)
        
        xavier_init = tf.contrib.layers.xavier_initializer()
        # returns an initializer performing "Xavior" initiatlization for weights
        action_num = np.int32(action_num)
        self.AW = tf.Variable(xavier_init([h_size,action_num]))
        self.VW = tf.Variable(xavier_init([h_size,1]))
        
        # tf.matmul multiplies matrix a by matrix b producing a*b
        # Q value is estimated by the value at hte current state and each action's advantage compared to other actions
        # The VALUE of a state denotes overall expected rewards by taking probabiliistic actions ink the future steps
        # the ADVANTAGE corresponds to every actions 
        
        self.Advantage = tf.matmul(self.streamA0,self.AW)

        self.Value = tf.matmul(self.streamV0,self.VW)
        
        ##### If the A value of an action is positive, it means the actions shows a better performance of all possible actions
        ##### otherwise if hte value of an action is neative it means actions potential reward is less than average
        
        # number of possible actions in our system is 9, size of advantage is 9x1
        # combined again to get the Q value (archiecture of the deueling Deep Q Network (DQN))
        
        #Then combine them together to get our final Q-values.
        
        ##########
        #### Check out =equation (7) in the paper for the explanation of below
        ##########
        self.Qout0 = self.Value  + tf.subtract(self.Advantage,tf.reduce_mean(self.Advantage,axis=1,keep_dims=True))
        #The final Q value is the addition of the Q value and penelized value for illegal actions
        self.Qout = tf.add(self.Qout0, self.legal_actions)
        #The predicted action
        self.predict = tf.argmax(self.Qout,1)
        
        
        #Below we obtain the loss by taking the mean square error between the target and prediction Q values.
        
        ### to update the parameters in the neural network, a target value is defined to help guide the update process
        ### NN is updated via MSE and is considered a loss function to guide the updating process of primary network
        ## to provide a stable update in each iteration, a separate target network ( same arch. nuy diff params) is usually employed to generate target value
        #############
        ####### Calculation of target Q value presented in double DQN part of paper ( see equation 10)
        #############
        self.targetQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,np.int32(action_num),dtype=tf.float32)
        
        self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), axis=1)
        #self.Q = tf.reduce_sum(self.Qout, axis=1)
        
        self.td_error = tf.square(self.targetQ - self.Q)
        self.loss = tf.reduce_mean(self.td_error)
        self.trainer = tf.train.AdamOptimizer(learning_rate=0.0001)
        self.updateModel = self.trainer.minimize(self.loss)
        
        
    def relu(self, x, alpha=0.01, max_value=None):
        '''ReLU.
        alpha: slope of negative section.
        '''
        negative_part = tf.nn.relu(-x)
        x = tf.nn.relu(x)
        if max_value is not None:
            x = tf.clip_by_value(x, tf.cast(0., dtype=tf.float32),
                                 tf.cast(max_value, dtype=tf.float32))
        x -= tf.constant(alpha, dtype=tf.float32) * negative_part
        return x

#The normal experience buffer
class experience_buffer():
    def __init__(self, buffer_size = 50000):
        self.buffer = []
        self.buffer_size = buffer_size
    
    ## For some reason in the source code they didn't have parentheses around
    ## the print statements...not sure what thats about
     ## if the size of memory m > M (replay memory size total input) then remove
        # oldest experiences in memory
   
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
        print ("ADDED", len(self.buffer))
            
    def sample(self,size):
        print ("BUFFer:", len(self.buffer))
        return np.reshape(np.array(random.sample(self.buffer,size)),[size,6])


#The target update functions
def updateTargetGraph(tfVars,tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx,var in enumerate(tfVars[0:total_vars//2]):
        op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
    return op_holder

def updateTarget(op_holder,sess):
    for op in op_holder:
        sess.run(op)

#The parameters
batch_size = 16 #How many experiences to use for each training step.
update_freq = 1 #How often to perform a training step.
y = .99 #Discount factor on the target Q-values
startE = 1 #Starting chance of random action
endE = 0.01 #Final chance of random action
anneling_steps = 100#00. #How many steps of training to reduce startE to endE.
num_episodes = 150#0#000 #How many episodes of game environment to train network with.
pre_train_steps = 200#0#0000 #How many steps of random actions before training begins.
max_epLength = 50#0 #The max allowed length of our episode.
load_model = False #Whether to load a saved model.
action_num = 9 #total number of actions
path = "./dqn" #The path to save our model to.
h_size = 64 #The size of the final convolutional layer before splitting it into Advantage and Value streams.
tau = 0.001 #Rate to update target network toward primary network

import math
class priorized_experience_buffer():
    def __init__(self, buffer_size = 20000):
        self.buffer = []
        self.prob = []
        self.err = []
        self.buffer_size = buffer_size
        self.alpha = 0.2
    
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.err[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
            self.prob[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
        self.err.extend([10000]*len(experience))
        self.prob.extend([1]*len(experience))
            
    def updateErr(self, indx, error):
        for i in range(0, len(indx)):
            self.err[indx[i]] = math.sqrt(error[i])
        r_err = ss.rankdata(self.err)  #rank of the error from smallest (1) to largest
        self.prob = [1/(len(r_err)-i+1) for i in r_err]

        
    def priorized_sample(self,size):
        prb = [i**self.alpha for i in self.prob]
        t_s = [prb[0]]
        for i in range(1,len(self.prob)):
            t_s.append(prb[i]+t_s[i-1])
        batch = []
        mx_p = t_s[-1]
        
        smp_set = set()
        
        while len(smp_set)<batch_size:
            tmp = np.random.uniform(0,mx_p)
            for j in range(0, len(t_s)):
                if t_s[j] > tmp:
                    smp_set.add(max(j-1,0))
                    break;
        for i in smp_set:
            batch.append([self.buffer[i], i])
        return np.array(batch)
#         return np.reshape(np.array(random.sample(self.buffer,size)),[size,6])

#The code for the SUMO environment
import os, sys
#if 'SUMO_HOME' in os.environ:
    

#The path of SUMO-tools to get the traci library
sys.path.append(os.path.join('/usr/share/sumo/', 'tools'))
import traci
import traci.constants as tc

import numpy as np

import datetime

#Environment Model
sumoBinary = "/usr/bin/sumo"
sumoCmd = [sumoBinary, "-c", "/usr/share/sumo/tools/game/cross.sumocfg"]  #The path to the sumo.cfg file
#sumoCmd = [sumoBinary, "-c","/Users/krouse/Documents/CUIP/deepq_example/sumo-1.3.1/tools/game/douglas.sumocfg"]


#sumoCmd = ["/Users/krouse/Documents/CUIP/RL/double-dueling-dqn/sumo-1.3.1/tools/game/cross.sumocfg"]
#reset the environment
def reset():
    traci.start(sumoCmd)
    tls = traci.trafficlight.getIDList()
    return tls

 
#get the starting state
def state():

    for veh_id in traci.vehicle.getIDList():
        traci.vehicle.subscribe(veh_id, (tc.VAR_POSITION, tc.VAR_SPEED))
    p = traci.vehicle.getAllSubscriptionResults()
    p_state = np.zeros((var1,var2,2))
    for x in p:
        ps = p[x][tc.VAR_POSITION]
        spd = p[x][tc.VAR_SPEED]
        #print("pos:", int(ps[0]/5))
        #print("speed", int(ps[1]/5))
        p_state[int(ps[0]/6), int(ps[1]/6)] = [1, int(round(spd))]
    #       v_state[int(ps[0]/5), int(ps[1]/5)] = spd
    p_state = np.reshape(p_state, [-1, mult , 2])
    return p_state #, v_state]

#get the legal actions at the current phases of the traffic light
def getLegalAction(phases):
    legal_action = np.zeros(9)-1
    i = 0
    for x in phases:
        if x>5:
            legal_action[i] = i
        if x<60:
            legal_action[i+5] = i+5
        i +=1
    legal_action[4] = 4
    return legal_action
    
#get the new phases after taking action from the current phases
def getPhaseFromAction(phases, act):
    if act<4:
        phases[int(act)] -= 5
    elif act>4:
        phases[int(act)-5] += 5
    return phases

#the process of the action
#input: traffic light; new phases; waiting time in the beginning of this cycle
#output: new state; reward; End or not(Bool); new waiting time at the end of the next cycle
def action(tls, ph, wait_time):  #parameters: the phase duration in the green signals
    tls_id = tls[0]
    init_p = traci.trafficlight.getPhase(tls_id) 
    wait_time = wait_time
    prev = -1
    changed = False
    current_phases = ph
   
    p_state = np.zeros((var1, var2,2))

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        c_p = traci.trafficlight.getPhase(tls_id)
        if c_p != prev and c_p%2==0:
            traci.trafficlight.setPhaseDuration(tls_id, ph[int(c_p/2)]-0.5)
            prev = c_p
        if init_p != c_p:
            changed = True
        if changed:
            if c_p == init_p:
                break
        traci.simulationStep()
        step += 1
        if step%10==0:
            for veh_id in traci.vehicle.getIDList():
                wait_time_map[veh_id] = traci.vehicle.getAccumulatedWaitingTime(veh_id)
    for veh_id in traci.vehicle.getIDList():
        traci.vehicle.subscribe(veh_id, (tc.VAR_POSITION, tc.VAR_SPEED, tc.VAR_ACCUMULATED_WAITING_TIME))
    #p = traci.vehicle.getSubscriptionResults()

    p =  traci.vehicle.getAllSubscriptionResults()
    
    #print(p)
    
    #print(p_state.shape)
    wait_temp = dict(wait_time_map)
    for x in p:
        ps = p[x][tc.VAR_POSITION]
        spd = p[x][tc.VAR_SPEED]
        #print("pos2:", int(ps[0]/5))
        #print("speed2:", int(ps[1]/5))
        p_state[int(ps[0]/5), int(ps[1]/7)] = [1, int(round(spd))]

    wait_t = sum(wait_temp[x] for x in wait_temp)
        
    d = False
    if traci.simulation.getMinExpectedNumber() == 0:
        d = True
            
    r = wait_time-wait_t
    p_state = np.reshape(p_state, [-1, mult, 2])
    return p_state,r,d,wait_t

#close the environment after every episode
def end():
    traci.close()


tf.reset_default_graph()
#define the main QN and target QN
mainQN = Qnetwork(h_size,np.int32(action_num))
targetQN = Qnetwork(h_size,np.int32(action_num))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

trainables = tf.trainable_variables()
targetOps = updateTargetGraph(trainables,tau)

#define the memory
myBuffer0 = priorized_experience_buffer()
test_bed_data = Experience()
myBuffer0.add(test_bed_data)
# put the testbed data
# muBuffer0.add(testbed.data)

#Set the rate of random action decrease. 
e = startE
stepDrop = (startE - endE)/anneling_steps

#create lists to contain total rewards and steps per episode
jList = []  #number of steps in one episode
rList = []  #reward in one episode
wList = []  #the total waiting time in one episode
awList = []  #the average waiting time in one episode
tList = []   #thoughput in one episode (number of generated vehicles)
nList = []   #stops' percentage (number of stopped vehicles divided by the total generated vehicles)
total_steps = 0

#Make a path for our model to be saved in.
if not os.path.exists(path):
    os.makedirs(path)

init_phases = [20,20,20,20]

sess = tf.InteractiveSession()

#record the loss 
tf.summary.scalar('Loss', mainQN.loss)

rfile = open(path+'/reward-rl.txt', 'w')
wfile = open(path+'/wait-rl.txt', 'w')
awfile = open(path+'/acc-wait-rl.txt', 'w')
tfile = open(path+'/throput-rl.txt', 'w')


merged = tf.summary.merge_all()
s_writer = tf.summary.FileWriter(path+'/train', sess.graph)
s_writer.add_graph(sess.graph)
    
sess.run(init)
tf.global_variables_initializer().run()
if load_model == True:
    print('Loading Model...')
    ckpt = tf.train.get_checkpoint_state(path)
    saver.restore(sess,ckpt.model_checkpoint_path)
updateTarget(targetOps,sess) #Set the target network to be equal to the primary network.


#the running process of the total number of episodes
for i in range(1,num_episodes):
    episodeBuffer0 = priorized_experience_buffer()
    #Reset environment and get first new observation
    tls = reset()
    s = state()#np.random.rand(1,10000)
    current_phases = list(init_phases)
    wait_time = 0
    wait_time_map = {}
    d = False
    rAll = 0
    j = 0
    
    print ("III:", i, e)
    while j < max_epLength:
        j+=1
        
        #get the legal actions at the current state
        legal_action = getLegalAction(current_phases) #np.random.randint(1,action_num,size=action_num) #[1,2,-1,4,5]
        
        #Choose an action (0-8) by greedily (with e chance of random action) from the Q-network
        if np.random.rand(1) < e or total_steps < pre_train_steps:
            a_cnd = [x for x in legal_action if x!=-1]
            a_num = len(a_cnd)
            a = np.random.randint(0, a_num)
            a = a_cnd[a]
        else:
            np.reshape(s, [-1,mult,2])
            legal_a_one = [0 if x!=-1 else -99999 for x in legal_action]
            a = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:s,mainQN.legal_actions:[legal_a_one]})[0]
        
        ph = getPhaseFromAction(current_phases,a)        
        s1, r, d, wait_time = action(tls, ph, wait_time)
        current_phases = ph

        total_steps += 1
        legal_a_one = [0 if x!=-1 else -99999 for x in legal_action] #the penalized Q value for illegal actions
        legal_act_s1 = getLegalAction(ph)
        legal_a_one_s1 = [0 if x!=-1 else -99999 for x in legal_act_s1]
        episodeBuffer0.add(np.reshape(np.array([s,a,r,s1,d,legal_a_one, legal_a_one_s1]),[1,7])) #Save the experience to our episode buffer.

        if total_steps > pre_train_steps:
            if e > endE:
                e -= stepDrop
            if total_steps % (update_freq) == 0:
                trainBatch = myBuffer0.priorized_sample(batch_size) #Get a random batch of experiences.
                indx = np.reshape(np.vstack(trainBatch[:,1]), [batch_size])
                indx = indx.astype(int)
                trainBatch = np.vstack(trainBatch[:,0])

                #Below we perform the Double-DQN update to the target Q-values 
                #action from the main QN
                Q1 = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,3]),mainQN.legal_actions:np.vstack(trainBatch[:,5])}) 
                #Q value from the target QN
                Q2 = sess.run(targetQN.Qout,feed_dict={targetQN.scalarInput:np.vstack(trainBatch[:,3]), targetQN.legal_actions:np.vstack(trainBatch[:,6])})
                # get targetQ at s'
                end_multiplier = -(trainBatch[:,4] - 1)  #if end, 0; otherwise 1
                doubleQ = Q2[range(batch_size),Q1]
                targetQ = trainBatch[:,2] + (y*doubleQ * end_multiplier)

                #Update the network with our target values.
                summry, err, ls, md = sess.run([merged, mainQN.td_error, mainQN.loss, mainQN.updateModel],  \
                    feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,0]),mainQN.targetQ:targetQ, mainQN.actions:trainBatch[:,1],mainQN.legal_actions:np.vstack(trainBatch[:,5])})

                s_writer.add_summary(summry, total_steps)
                #update the target QN and the memory's prioritization
                updateTarget(targetOps,sess) #Set the target network to be equal to the primary network.
                myBuffer0.updateErr(indx, err)
                
        rAll += r
        s = s1

        if d == True:
            break
    end()    

    #save the data into the myBuffer
    myBuffer0.add(episodeBuffer0.buffer)
    
    jList.append(j)
    rList.append(rAll)
    rfile.write(str(rAll)+'\n')
    wt = sum(wait_time_map[x] for x in wait_time_map)
    wtAve = wt/len(wait_time_map)
    wList.append(wtAve)
    wfile.write(str(wtAve)+'\n')
    awList.append(wt)
    awfile.write(str(wt)+'\n')
    tList.append(len(wait_time_map))
    tfile.write(str(len(wait_time_map))+'\n')
    tmp = [x for x in wait_time_map if wait_time_map[x] > 1]
    nList.append(len(tmp)/len(wait_time_map))
    print ("Total Reward---------------",  rAll)
    #Periodically save the model. 
    if i % 100 == 0:
        saver.save(sess,path+'/model-'+str(i)+'.cptk')
        print("Saved Model")
#         if len(rList) % 10 == 0:
#             print(total_steps,np.mean(rList[-10:]), e)
saver.save(sess,path+'/model-'+str(i)+'.cptk')
print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")
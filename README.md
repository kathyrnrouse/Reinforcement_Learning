# RL_CUIP
RL based on the DQN paper by Liang and Du for the Douglas Traffic Light (https://arxiv.org/pdf/1803.11115.pdf )

This is for the taffic light at the Douglas/ MLK intersection and applies the code derived from the paper above.

# Testbed Data
In order to make use of "real time" events in an Reinforcment Learning environment, we have decided to implement an
Experience Replay Buffer (like that used in teh Liang and Du paper), however, rather than initializing the buffer to
zero, we have filled it with historic data. 

This is done from the "experience.py" file which takes in the json file of the intersection, the csv file for the
traffic data with that intersection, and fills the initial buffer in the main code which is: "deepRl_tlc_IEEEpaper.py"

# Sumo Environment
I am currently editing a SUMO environment that emulates the Douglas/ MLK interesection. There are currently a few bugs when running
This will then be used for the training in addition to the experience buffer

# Literature Review:
The following papers are useful in the understaning of this topic


# Further Research
Logically, the next move would be to implement this in multiple traffic intersections. 

One thing to note is the idea that RL may or may not benefit from historical data, and if so, how can this be implemented. 
This could be the subject of future research. 

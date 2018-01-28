import tensorflow
import math
from Agent import Agent
from utils import *

#init variables
agent_group_size = 20
agent_array = []
neighbor_radius = 350

#CONSTANTS
DEFAULT_SPEED = 10
ALIGNMENT_WEIGHT = 1.5
COHESION_WEIGHT = 1.5
SEPERATION_WEIGHT = 1.5

def computeAlignment(myAgent):
    compute_vel = [0,0]
    neighbors_cnt = 0

    for agent in agent_array:
        if agent != myAgent and myAgent.distanceFrom(agent) < neighbor_radius:
            compute_vel[0] += agent.vel[0]
            compute_vel[1] += agent.vel[1]
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel[0] /= neighbors_cnt
    compute_vel[1] /= neighbors_cnt

    return getUnitVector(compute_vel)

def computeCohesion(myAgent):
    compute_vel = [0,0]
    neighbors_cnt = 0

    for agent in agent_array:
        if agent != myAgent and myAgent.distanceFrom(agent) < neighbor_radius:
            compute_vel[0] += agent.pos[0]
            compute_vel[1] += agent.pos[1]
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel[0] /= neighbors_cnt
    compute_vel[1] /= neighbors_cnt
    new_v = [compute_vel[0] - myAgent.pos[0], compute_vel[1] - myAgent.pos[1]]

    return getUnitVector(new_v)

def computeSeperation(myAgent):
    compute_vel = [0,0]
    neighbors_cnt = 0

    for agent in agent_array:
        if agent != myAgent and myAgent.distanceFrom(agent) < neighbor_radius:
            compute_vel[0] += agent.pos[0] - myAgent.pos[0]
            compute_vel[1] += agent.pos[1] - myAgent.pos[0]
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel[0] /= -neighbors_cnt
    compute_vel[1] /= -neighbors_cnt

    return getUnitVector(compute_vel)



#init agent
for i in xrange(0,agent_group_size):
    agent_array.append(Agent())

#MAIN Loop
for agent in agent_array:

    temp_vel = [0,0]

    alignment_v = computeAlignment(agent)
    cohesion_v = computeCohesion(agent)
    seperation_v = computeSeperation(agent)

    print "cohesion_v[0]: {}".format(cohesion_v[0])

    temp_vel[0] += (alignment_v[0] * ALIGNMENT_WEIGHT +
                    cohesion_v[0] * COHESION_WEIGHT +
                    seperation_v[0] * SEPERATION_WEIGHT)

    temp_vel[1] += (alignment_v[1] * ALIGNMENT_WEIGHT +
                    cohesion_v[1] * COHESION_WEIGHT +
                    seperation_v[1] * SEPERATION_WEIGHT)

    agent.vel = getUnitVector(temp_vel, DEFAULT_SPEED)
    agent.updatePos()

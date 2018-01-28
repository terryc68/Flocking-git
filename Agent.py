from math import *
import utils

DEFAULT_SPEED = 6

class Agent(object):

    def __init__(self,pos = (1,1), vel=(DEFAULT_SPEED,0)):
        self.pos = (pos[0],pos[1])
        self.vel = vel

    def distanceFrom(self,other_agent):
        return sqrt((other_agent.pos[0] - self.pos[0])**2 + (other_agent.pos[1] - self.pos[1]) **2)

    def updatePos(self):
        self.pos = utils.v_add(self.pos,self.vel)

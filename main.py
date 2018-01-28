import math
import utils
from utils import v_sub, v_add, v_mul, v_div, v_array_sum, agent_degree_rotation
import sys
import pygame as pyg
from operator import neg
from Agent import *
from Obstacle import *
from random import randrange

#init variables
agent_array = []
obstacle_array = []

#CONSTANTS
ALIGNMENT_WEIGHT = [15,5]
COHESION_WEIGHT = [3,3]
SEPERATION_WEIGHT = [10,5]
OBSTACLE_DOGDGE_WEIGHT = 50

ALIGNMENT_RADIUS = 200
COHESION_RADIUS = 170
SEPERATION_RADIUS = 30
OBSTACLE_DOGDGE_RADIUS = 250

MAX_FORCE = 0.03


def computeAlignment(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in xrange(0,len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < ALIGNMENT_RADIUS and t == i%2:
            compute_vel = v_add(compute_vel,agent.vel)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return utils.limit(compute_vel,0.05)

def computeCohesion(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in xrange(0,len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < COHESION_RADIUS and t == i%2:
            compute_vel = v_sub(agent.pos,myAgent.pos)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return utils.limit(compute_vel, 0.05)

def computeSeperation(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in xrange(0,len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < SEPERATION_RADIUS and t == i%2:
            temp_vel = v_sub(myAgent.pos,agent.pos)
            temp_vel = utils.getUnitVector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distanceFrom(agent)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def computeObscatleDodge(myAgent):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for obs in obstacle_array:
        if obs.distanceFrom(myAgent) < OBSTACLE_DOGDGE_RADIUS:
            temp_vel = v_sub(myAgent.pos,obs.pos)
            temp_vel = utils.getUnitVector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distanceFrom(obs)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def check_agent_inbound():
    for agent in agent_array:
        if agent.pos[0] > WIDTH:
            agent.pos = (0,agent.pos[1])
        if agent.pos[0] < 0:
            agent.pos = (WIDTH,agent.pos[1])
        if agent.pos[1] > HEIGHT:
            agent.pos = (agent.pos[0],0)
        if agent.pos[1] < 0:
            agent.pos = (agent.pos[0],HEIGHT)

def agent_update():
    global agent_array
    temp_agent_array = []

    for i in xrange(0,len(agent_array)):
        agent = agent_array[i]
        temp_vel = (0,0)
        cohesion_v = computeCohesion(agent,i%2)
        alignment_v = computeAlignment(agent,i%2)
        seperation_v = computeSeperation(agent,i%2)
        obstacle_dodge_v = computeObscatleDodge(agent)

        v_array = [agent.vel,
                   utils.v_mul(cohesion_v,COHESION_WEIGHT[i%2]),
                   utils.v_mul(alignment_v,ALIGNMENT_WEIGHT[i%2]),
                   utils.v_mul(seperation_v,SEPERATION_WEIGHT[i%2]),
                   utils.v_mul(obstacle_dodge_v, OBSTACLE_DOGDGE_WEIGHT)
                   ]

        temp_vel = utils.v_array_sum(v_array)
        a = Agent(agent.pos, temp_vel)
        if i%2:
            a.vel = utils.limit(temp_vel, DEFAULT_SPEED *1.4)
        else:
            a.vel = utils.limit(temp_vel, DEFAULT_SPEED)
        # utils.change_vel_if_zero(a)
        a.updatePos()
        temp_agent_array.append(a)

    agent_array = temp_agent_array

def randomize_position():
    for agent in agent_array:
        agent.pos = randrange(0,WIDTH,1), randrange(0,HEIGHT,1)

def clear_all_item():
    agent_array = []
    obstacle_array = []

#pygame variables
WIDTH = 1300
HEIGHT = 680
TITLE = "FLOCKING"
FPS = 30
BACKGROUND = (0,0,0)
AGENT_COLOR = [(116,175,173),(222,27,26)]
OBSTACLE_COLOR = (162,171,88)
TRI_BASE = 12
TRI_HEIGHT = 18

pyg.init()
clock = pyg.time.Clock()
clock.tick(FPS)

screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption(TITLE)

def make_agent_inbound():
    for agent in agent_array:
        agent.pos = agent.pos[0] % WIDTH, agent.pos[1] % HEIGHT

def draw_agent():
    for i in xrange(0,len(agent_array)):
        agent = agent_array[i]
        make_agent_inbound()
        pointlist = utils.boid_pointlist(TRI_BASE,TRI_HEIGHT)
        surface = pyg.Surface((TRI_BASE, TRI_HEIGHT), pyg.SRCALPHA).convert_alpha()
        pyg.draw.polygon(surface,AGENT_COLOR[i%2],pointlist, 0)
        rotate = pyg.transform.rotate(surface,-agent_degree_rotation(agent))
        center = v_sub(agent.pos,(TRI_BASE/2, TRI_HEIGHT / 2))
        screen.blit(rotate, center)

def draw_obstacle():
    for obs in obstacle_array:
        pyg.draw.circle(screen,OBSTACLE_COLOR,obs.pos,obs.radius,0)

def run():
    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif pyg.mouse.get_pressed()[0]:
                agent_array.append(Agent(pyg.mouse.get_pos()))
            elif pyg.mouse.get_pressed()[2]:
                obstacle_array.append(Obstacle(pyg.mouse.get_pos()))
            elif pyg.key.get_pressed()[pyg.K_r]:
                randomize_position()

        screen.fill(BACKGROUND)
        draw_agent()
        draw_obstacle()
        agent_update()
        pyg.display.update()

run()

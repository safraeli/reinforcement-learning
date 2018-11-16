# Base Data Science snippet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm_notebook
from scipy.spatial.distance import cdist

plt.style.use("seaborn-dark")




class DeliveryEnvironment(object):
    def __init__(self,n_stops = 10,max_box = 10,method = "distance"):

        print(f"Initialized Delivery Environment with {n_stops} random stops")
        print(f"Target metric for optimization is {method}")

        # Initialization
        self.n_stops = n_stops
        self.action_space = self.n_stops
        self.observation_space = self.n_stops
        self.max_box = max_box
        self.stops = []

        # Generate stops
        self._generate_stops()
        self._generate_q_values(method = method)
        self.render()

        # Initialize first point
        self.reset()



    def _generate_stops(self):

        # Generate geographical coordinates
        xy = np.random.rand(self.n_stops,2)*self.max_box
        self.x = xy[:,0]
        self.y = xy[:,1]


    def _generate_q_values(self,method="distance"):

        # Generate actual Q Values corresponding to time elapsed between two points
        if method=="distance":
            xy = np.column_stack([self.x,self.y])
            self.q_stops = cdist(xy,xy)
        elif method=="time":
            self.q_stops = np.random.rand(self.n_stops,self.n_stops)*self.max_box
            np.fill_diagonal(self.q_stops,0)
        else:
            raise Exception("Method not recognized")
    

    def render(self):
        
        fig = plt.figure(figsize=(7,7))
        ax = fig.add_subplot(111)
        plt.title("Delivery Stops")

        # Show stops
        plt.scatter(self.x,self.y,c = "red",s = 50)

        # Show START
        if len(self.stops)>0:
            xy = self._get_xy(initial = True)
            xytext = xy[0]+0.1,xy[1]-0.05
            ax.annotate("START",xy=xy,xytext=xytext,weight = "bold")

        # Show itinerary
        if len(self.stops) > 1:
            plt.plot(self.x[self.stops],self.y[self.stops],c = "blue",linewidth=1,linestyle="--")
            
            # Annotate END
            xy = self._get_xy(initial = False)
            xytext = xy[0]+0.1,xy[1]-0.05
            ax.annotate("END",xy=xy,xytext=xytext,weight = "bold")

        plt.xticks([])
        plt.yticks([])
        plt.show()



    def reset(self):

        # Stops placeholder
        self.stops = []

        # Random first stop
        first_stop = np.random.randint(self.n_stops)
        self.stops.append(first_stop)


    def step(self,destination):

        # Get current state
        state = self._get_state()
        new_state = destination

        # Get reward for such a move
        reward = self._get_reward(state,new_state)

        # Append new_state to stops
        self.stops.append(destination)
        done = len(self.stops) == self.n_stops

        return new_state,reward,done
    

    def _get_state(self):
        return self.stops[-1]


    def _get_xy(self,initial = False):
        state = self.stops[0] if initial else self._get_state()
        x = self.x[state]
        y = self.y[state]
        return x,y


    def _get_reward(self,state,new_state):
        return self.q_stops[state,new_state]

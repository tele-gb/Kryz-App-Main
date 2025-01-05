#imports
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint # just a handy printing function
from datetime import datetime, timedelta
import pandas as pd
import math
import time
import json
import matplotlib.pyplot as plt
import datetime
from datetime import datetime,timedelta
import calendar




class DancingGame:
    def __init__(self, bpm=120, population=50):
        # Initialize variables
        self.bpm = bpm
        self.base_bpm = 120
        self.population = population
        self.start_infected = 1
        self.start_cal = 100
        self.reduction = -10
        self.base_reduction = -10
        self.infection_period = 5
        self.base_infection_period = 5
        self.infection_rt = 0.5
        self.base_infection_rate = 0.5
        self.death_point = 0
        self.tick = 0

    def adjust_rates(self):
        # Use self attributes for the calculation
        scale_factor = self.bpm / self.base_bpm

        adjusted_infection_rate = self.base_infection_rate * scale_factor
        adjusted_reduction = self.base_reduction * (scale_factor ** 3)
        adjusted_infection_period = math.floor(max(1, self.base_infection_period / (scale_factor * 0.9)))

        return adjusted_infection_rate, adjusted_reduction, adjusted_infection_period

    def create_list(self):
        infected_calories = [self.start_cal] * self.start_infected
        return infected_calories

    def cal_reduction(self, input_list, adjusted_reduction):
        return [cal + adjusted_reduction for cal in input_list]

    def remove_dead(self, input_list):
        died_this_tick = sum(1 for cal in input_list if cal <= self.death_point)
        input_list = [cal for cal in input_list if cal > self.death_point]
        return died_this_tick, input_list

    def new_infections(self, tick, adjusted_infection_period, remaining_pop, input_list):
        if tick % adjusted_infection_period == 0 and remaining_pop > 0:
            new_infected = min(math.ceil(len(input_list) * self.infection_rt), remaining_pop)
            input_list.extend([self.start_cal] * new_infected)
        else:
            new_infected = 0
        return new_infected

    def initialise_df(self):
        return pd.DataFrame(columns=[
            "Tick", "Infected Count", "Average Calories", "New Infected",
            "Died This Tick", "Total Infected", "Remaining Population",
            "Total Alive", "Total Dead"
        ])
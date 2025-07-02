import math
import random
from dataclasses import dataclass
import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

@dataclass

class Town:
    id: int
    tick: int = 0
    city: str = "test"
    lat: float = 0.0
    lng: float = 0.0
    population: int = 200
    infected: int = 1
    calories: int = 100
    dead: int = 0
    total_infected: int = 1
    params: dict = None
    
    def __post_init__(self):
        self.remaining_pop = self.population - self.infected
        self.alive = self.population - self.dead
        # Only set default params if none were provided
        if self.params is None:
            self.params = {
                'bpm': 80,
                'reduction': -2,
                'infection_period': 3,  # Fixed typo from 'infection_period'
                'infection_rt': 0.5,
                'death_rate': 0.1,
                'deathpoint': 25
            }

# MOVE THE DiseaseOutbreakSimulator CLASS OUTSIDE OF THE Town CLASS
class DiseaseOutbreakSimulator:
    def __init__(self, default_params=None):
        self.towns = {}
        self.global_tick = 0
        self.next_town_id = 1
        self.creation_events = []
        self.state_tick = 0
        self.state_infected = 0
        self.state_calories = 0
        self.state_population = 0
        self.state_dead = 0
        self.state_cities = 0

        # Ensure all required parameters are present
        self.default_params = {
            'bpm': 80,
            'reduction': -2,
            'infection_period': 3,
            'infection_rt': 0.5,
            'death_rate': 0.1,
            'deathpoint': 25
        }
        # Update with any user-provided defaults
        if default_params:
            self.default_params.update(default_params)


    def reset_infections(self):
        conn = sqlite3.connect('SqlliteDB/towns.db')  
        c = conn.cursor()
        c.execute("UPDATE france_citiesgrid2 SET infected = 0")
        conn.commit()
        conn.close()
        
    def get_town(self,id=647,tablename="france_citiesgrid2"):
        conn = sqlite3.connect('SqlliteDB/towns.db')  
        c = conn.cursor()
        query = f"SELECT * FROM {tablename} where id = {id}"
        df = pd.read_sql_query(query, conn)

        # Then update
        update_query = f"UPDATE {tablename} SET infected = 1 WHERE id = {id}"
        c.execute(update_query)
        conn.commit()
        conn.close()
    
        if df.empty:
            # print(f"No town found with id {id}")
            return None

        town_data = df.iloc[0].to_dict()
        return town_data
    
    def get_approx_towns(self, id, tablename="france_citiesgrid2"):
        conn = sqlite3.connect('SqlliteDB/towns.db')
        c = conn.cursor()
        
        try:
            c.execute(f"SELECT city,lat,lng FROM {tablename} WHERE id = ?", (id,))
            results = c.fetchone()

            if results is None:
                # print(f"No town found for id {id}")
                return None

            city, olat, olng = results
            # print(city, olat, olng)

            query = f"""
            SELECT id, city, lat, lng, population,
                6371 * acos(
                    cos(radians({olat})) * cos(radians(lat)) * cos(radians(lng) - radians({olng})) +
                    sin(radians({olat})) * sin(radians(lat))
                ) AS distance
            FROM {tablename}
            WHERE lat BETWEEN {olat} - 0.2 AND {olat} + 0.2
            AND lng BETWEEN {olng} - 0.2 AND {olng} + 0.2
            AND id <> {id} AND population > 0
            AND infected = 0
            ORDER BY distance ASC
            LIMIT 1
            """

            df = pd.read_sql_query(query, conn)

            if df.empty:
                # print(f"No nearby towns found for id {id}")
                return None

            return df.iloc[0]['id']

        except Exception as e:
            # print(f"Error in get_approx_towns: {e}")
            return None

        finally:
            conn.close()

    def haversine(self,lat1, lon1, lat2, lon2):
        R = 6371  
        phi1, phi2 = radians(lat1), radians(lat2)
        dphi = radians(lat2 - lat1)
        dlambda = radians(lon2 - lon1)
        # print("Haversine function")

        a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
        return 2 * R * atan2(sqrt(a), sqrt(1 - a))

    def get_approx_towns_python(self, id, tablename="france_citiesgrid2"):
        conn = sqlite3.connect('SqlliteDB/towns.db')
        c = conn.cursor()
        
        try:
            c.execute(f"SELECT city,lat,lng FROM {tablename} WHERE id = ?", (id,))
            results = c.fetchone()

            if results is None:
                # print(f"No town found for id {id}")
                return None

            city, olat, olng = results
            # print(city, olat, olng)

            query = f"""
            SELECT id, city, lat, lng, population
            FROM {tablename}
            WHERE lat BETWEEN {olat} - 0.2 AND {olat} + 0.2
            AND lng BETWEEN {olng} - 0.2 AND {olng} + 0.2
            AND id <> {id} AND population > 0
            AND infected = 0
            
            
            """

            df1 = pd.read_sql_query(query, conn)
            # print(df1)
            conn.close()

            if df1.empty:
                # print(f"No nearby towns found for id {id}")
                return None
            
            df1['distance'] = df1.apply(lambda row: self.haversine(olat, olng, row['lat'], row['lng']), axis=1)
            # print(self.haversine(olat, olng, df1.iloc[0]['lat'], df1.iloc[0]['lng']))
            nearest = df1.nsmallest(1, 'distance')
            # print(nearest)


            return nearest.iloc[0]['id']

        except Exception as e:
            print(f"Error in get_approx_towns: {e}")
            return None

        
    def add_town(self, start_tick=0, id=647, **kwargs):
        town_data = self.get_town(id)
        if town_data is None:
            return None

        # Get any params passed directly or from kwargs
        params = kwargs.pop('params', {})
        # Merge with default params (default params take precedence unless overridden)
        final_params = self.default_params.copy()
        final_params.update(params)

        new_town = Town(
            id=town_data['id'],
            tick=start_tick,
            city=town_data['city'],
            lat=town_data['lat'],
            lng=town_data['lng'],
            population=town_data['population'],
            params=final_params  # Pass the merged params
        )

        self.towns[id] = new_town
        return new_town


        
        #this calls the @dataclass town to create a new town object in the town dictionary with a population of 2m
        #any parameter could be adjusted here, instead of the population
#         self.towns[town_id] = Town(
#             id=town_id,
#             tick=start_tick,
#             population=kwargs.get('population', 2000000),
#             params=params 
#         )
        
#         self.next_town_id += 1
        
        # return new_town
    
    def run_tick(self,escape_chance=0):
        """Advance simulation by one global tick"""
        self.global_tick += 1
        events = []
        
#         print(f"Tick: {self.global_tick}")
#         time.sleep(0.1)  
        
        # Process each town that should be active this tick
        for town_id in list(self.towns.keys()):
            town = self.towns[town_id]
            
            # Skip towns that haven't started yet
            if town.tick >= self.global_tick:
                continue

            #skip towns where everyone is dead
            if town.alive > 0:    
                town.tick += 1
                
                # Reset per-tick counters
                infection_flag = new_infected = new_cal = dead = 0
                
                # 1. Update calories
                town.calories += town.params['reduction'] * town.infected
                town.calories = max(town.calories, 0)
                
                # 2. Calculate average calories
                avg_cal = town.calories / town.infected if town.infected > 0 else 0
                
                # 3. Death mechanic
                if avg_cal < town.params['deathpoint'] and town.infected > 0:
                    dead = math.ceil(town.infected * town.params['death_rate'])
                    dead = min(dead, town.infected)
                    town.infected -= dead
                    town.calories -= dead * 100
                    town.calories = max(town.calories, 0)
                    town.dead += dead
                    town.alive = town.population - town.dead
                
                # 4. Infection system
                if town.tick % town.params['infection_period'] == 0:
                    infection_flag = 1
                    potential_new = math.ceil(town.infected * town.params['infection_rt'])
                    new_infected = min(potential_new, town.remaining_pop)
                    
                    if new_infected > 0:
                        new_cal = new_infected * 100
                        town.infected += new_infected
                        town.calories += new_cal
                        town.total_infected += new_infected
                        town.remaining_pop = max(town.population - town.total_infected, 0)
                
                # 5. Escape check (per tick)
    #---------- SHUTTING THIS OFF FOR NOW -----------------------------------
                
                if escape_chance == 1:
                    if town.alive > 0:
                        if town.infected / town.population > 0.5:
                            if random.random() < 0.1:  # 10% chance per tick
                                # Create new town starting NEXT global tick

                                #want to 1) run the get approx towns to get the nearest place
                                #        2) add that particular town    
                                # Run approx towns:
                                escape_town_id = self.get_approx_towns_python(town.id)
                                # print(escape_town_id)

                                #        2) add that particular town    
                                if escape_town_id is None:
                                    continue
                                else:
                                    new_town_id = self.add_town(id=escape_town_id,start_tick=self.global_tick + 1)
                                    events.append((
                                    'town_created', 
                                    self.global_tick,
                                    town_id,
                                    new_town_id
                                    ))
                else:
                    pass
                    

        return events
        

    def get_town_status(self, town_id):
        """Get current status of a town"""
        town = self.towns[town_id]
        return {
            'CITY' :town.city,
            'tick': town.tick,
            'infected': town.infected,
            'calories': town.calories,
            'population': town.population,
            'dead': town.dead,
            'alive': town.alive,
            'remaining_pop': town.remaining_pop,
            'total_infected': town.total_infected
        }
    
    def get_infected_coords(self):
        data = []
        for town in self.towns.values():
            if town.infected > 0:
                data.append({'lat': town.lat, 'lng': town.lng, 'infected': town.infected})
        return pd.DataFrame(data)
    
    
    
    def get_global_status(self):
        towns_dict = {tid: town.__dict__ for tid, town in self.towns.items()}
        df = pd.DataFrame.from_dict(self.towns, orient='index').reset_index().rename(columns={'index': 'id'})
        city_count = df['city'].nunique()
        columns_to_sum = ['population', 'infected', 'calories','dead', 'total_infected']
        sums = df[columns_to_sum].sum()
        summary_df = pd.DataFrame(sums).transpose()
        summary_df.insert(0, 'city_count', city_count)
        summary_df.insert(0, 'global_tick', self.global_tick)
        return summary_df
    
    def get_state_vaiables(self,df):
        last_row = df.iloc[-1]
        # Set global variables
        self.state_tick = last_row["global_tick"]
        self.state_infected = last_row["infected"]
        self.state_calories = last_row["calories"]
        self.state_population = last_row["population"]
        self.state_dead = last_row["dead"]
        self.state_cities = last_row["city_count"]

    def make_charts(self,dataframe):
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))

        # Left chart
        axs[0].plot(df['global_tick'], df['population'], label='Population')
        axs[0].plot(df['global_tick'], df['infected'], label='Infected')
        axs[0].plot(df['global_tick'], df['dead'], label='Dead')
        axs[0].set_title('Population and Infected')
        axs[0].legend()

        # Right chart
        axs[1].plot(df['global_tick'], df['city_count'], label='Cities')
        axs[1].set_title('Cities')
        axs[1].legend()

        return plt
    
    def towns_dict_to_df(self, flatten_params=False):
        rows = []
        for key, town in self.towns.items():
            town_dict = town.__dict__
            rows.append(town_dict)

        df = pd.DataFrame(rows)

        if flatten_params and 'params' in df.columns:
            params_df = pd.json_normalize(df['params'])
            df = df.drop(columns='params').reset_index(drop=True)
            df = pd.concat([df, params_df], axis=1)

        return df
    
    def log_infected_coords(self):
        """
        Returns a DataFrame of lat/lng positions of currently infected towns.
        """
        data = []
        for town in self.towns.values():
            if town.total_infected > 0:
                data.append({
                    'tick': self.global_tick,
                    'lat': town.lat,
                    'lng': town.lng,
                    'infected': town.infected
                })
        return pd.DataFrame(data)


    def plot_infected_coords(self):
        """
        Plots a scatter plot of currently infected towns.
        """
        coords_df = self.log_infected_coords()
        if coords_df.empty:
            print(f"No infections at tick {self.global_tick}")
            return
        
        plt.xlim(0, 10)
        plt.ylim(45, 50)

        plt.scatter(coords_df['lng'], coords_df['lat'], 
                    # s=coords_df['infected'] * 0.5, 
                    c='red', alpha=0.7)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Infected Locations at tick {self.global_tick}')
        plt.show()


from flask import Flask, render_template, request,send_file,session,url_for,jsonify
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import numpy as np
import pandas as pd
import requests
import urllib3
# import xmltodict
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint # just a handy printing function
from stravalib import Client
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,BooleanField,DateTimeField,
                    SelectField,TextAreaField,RadioField,StringField)
from wtforms.validators import DataRequired
from guitar import Guitar
from Strava_Stats import StravaStats
import fretboard  
import sqlite3
import time
from Dancing_Class import DancingGame
import json
from flask import Flask, Response, request, jsonify
import math
# from IPython.display import SVG, display


import os
os.environ['APP_SETTINGS'] = 'settings.cfg'


app=Flask(__name__)
app.secret_key = "Lis@2104"

#put these in enviroment vars

app.config.from_envvar("APP_SETTINGS")


# client_id = "96903"
# client_secret = "0f4e7f68927263eb277b60fa2ef396b7964cdc94"


@app.route('/')
def home():
    return render_template('home.html')

#-------------------------------------------------------------------------#
#----------------STRAVA---------------------------------------------------#

@app.route('/strava')
def strava():
    c = Client()
    url = c.authorization_url(client_id=app.config["CLIENT_ID"],
                            redirect_uri=url_for('.lastruns',_external=True )
                            ,scope=['read_all','profile:read_all','activity:read_all'],
                            approval_prompt="force")
    print(url)
    return render_template('stravamain.html',authorize_url=url)

@app.route('/lastruns')
def lastruns():

    code = request.args.get("code")
    stuff = request.view_args.items
    if not code:
        return "Authorization code missing!", 400
    
    print(code)
    print(stuff)
    
    client = Client()
    access_token = client.exchange_code_for_token(
                                                    client_id=app.config["CLIENT_ID"],
                                                    client_secret=app.config["CLIENT_SECRET"],
                                                    code=code,
                                                )
    # Store tokens and expiry in the session
    session['access_token'] = access_token['access_token']
    session['refresh_token'] = access_token['refresh_token']
    session['expires_at'] = access_token['expires_at']    


    # Probably here you'd want to store this somewhere -- e.g. in a database.
    strava_athlete = client.get_athlete()
    print(strava_athlete)
    
    # print(access_token['access_token'])
    session['sac'] = access_token['access_token']
    print(access_token['access_token'])
    print(access_token['refresh_token'])
    expirestime=access_token['expires_at']
    print(expirestime)




    return render_template('lastruns.html',code=code,athlete=strava_athlete,access_token=access_token,)


strava=StravaStats()

#need to add this to strava_statsh;
def get_strava_client():
    """Initialize Strava client with a valid access token."""
    client = Client()
    access_token = session.get('access_token')
    refresh_token = session.get('refresh_token')
    expires_at = session.get('expires_at')

    if not access_token or not refresh_token or not expires_at:
        raise ValueError("Tokens are missing from session!")

    # Check if the token is expired
    if datetime.utcnow().timestamp() > expires_at:
        # Refresh the token
        refresh_response = client.refresh_access_token(
            client_id=app.config["CLIENT_ID"],
            client_secret=app.config["CLIENT_SECRET"],
            refresh_token=refresh_token
        )
        # Update session with new tokens
        session['access_token'] = refresh_response['access_token']
        session['refresh_token'] = refresh_response['refresh_token']
        session['expires_at'] = refresh_response['expires_at']
        access_token = refresh_response['access_token']

    client.access_token = access_token
    return client

@app.route('/lastruns2')
def lastruns2():

    client = get_strava_client()
    print(client)
    activities = client.get_activities() 
    strava_access_token = session.get('sac') 
    header2 = {'Authorization': 'Bearer ' + session['access_token'] }
    print(header2)

    print(f'Access Token: {session.get('access_token')}')
    print(f'Header: {header2}')
 
    actlist = strava.all_activities(header2)
    print(len(actlist))
    testlist = strava.activities_list(actlist,5000,50)
    print(len(testlist))
    testdf = strava.multi_activities(50,testlist,header2)
    testdf2 = strava.rolling_df(testdf,3)

    if testdf2.empty:
        return render_template('lastrunserror.html', error="No data available for analysis.")


    strava.load_to_sql(testdf)

    mean_of_runs = strava.mean_run_time(testdf2)
    median_of_runs = strava.median_run_time(testdf2)
    fastest_time = strava.fastest_time(testdf2)
    fastest_day = strava.fastest_day(testdf2)
    slowest_time = strava.slowest_time(testdf2)
    slowest_day = strava.slowest_day(testdf2)
    latest_day=strava.latest_day(testdf2)
    latest_time=strava.latest_time(testdf2)

    current_time_delta = abs(round(strava.convert_to_seconds(latest_time)-strava.convert_to_seconds(mean_of_runs),2))
   
    return render_template('lastruns2.html',
                           mean_of_runs=mean_of_runs,
                           median_of_runs=median_of_runs,
                           fastest_time=fastest_time,
                           fastest_day=fastest_day,
                           slowest_time=slowest_time,
                           slowest_day=slowest_day,
                           latest_day=latest_day,
                           latest_time=latest_time,
                           current_time_delta=current_time_delta,
                           tables=[testdf2.to_html(classes='data')], 
                           titles=testdf2.columns.values)

#-------------------------------------------------------------------------#
#----------------DEBT CALC------------------------------------------------#
#global variables
debtdf_start = None

@app.route('/calculate')
def calculate():

    # processed_data = request.json
    return render_template('calculate.html')

@app.route('/process_table_data', methods=['POST'])
def process_table_data():
    global debtdf_start
    table_data = request.json  # Get the JSON data sent from the frontend
    debtdf = pd.DataFrame(table_data)
    # Process the table_data in your Python function
    # Perform calculations or any other operations needed

    # For example, let's print the received data
    print(debtdf)
    debtdf_start = debtdf
    # You can return a response if needed
    return jsonify({'message': 'Data received and processed successfully'})
    # return render_template('calc_results.html')

@app.route('/calc_results')
def calc_results():
    global debtdf_start

    return render_template('calc_results.html',
                        tables=[debtdf_start.to_html(classes='data')], 
                        titles=debtdf_start.columns.values)


#-------------------------------------------------------------------------#
#----------------GUITAR---------------------------------------------------#

#define some globel variable
guitar = Guitar()
scale_types = guitar.scale_dict
tuning_types = guitar.tuning_dict

@app.route('/guitarscale', methods=['GET', 'POST'])
def guitarscale():
    if request.method == 'POST':
        # Get form inputs

        # scale_type = request.form['scale_type']
        scale_type = request.form.get('scale_type', 'maj_scale')
        root = request.form['root_note']
        tuning_type = request.form.get('tuning_type', 'standard')
        svg_file = "static/test.png"

        guitar.draw_fretboard(0,12,root,scale_type,tuning_type,0,svg_file)
        svg_image=guitar.get_svg_string(svg_file)
        svg_image_base64 = base64.b64encode(svg_image.encode('utf-8')).decode('utf-8')


        return render_template('guitarscale.html',
                               svg_image=svg_image_base64,
                            scale_types=scale_types,scale_type=scale_type,tuning_types=tuning_types,root=root,tuning_type=tuning_type
                            #    ,root_note=root_note
                            )
    return render_template('guitarscale.html',
                           svg_image=None,
                           scale_types=scale_types,tuning_types=tuning_types
                        #    ,root_note=root_note
                           )


#-------------------------------------------------------------------------#
#----------------Takeaway TRACKER-----------------------------------------#

#define some globel variable

@app.route('/Takeaway', methods=['GET', 'POST'])
def ttracker():
    if request.method == 'POST':
        date = request.form['Date']
        where = request.form['Where']
        cost = request.form['Cost']

        # Insert the data into the database
        conn = sqlite3.connect('SqlliteDB/takeaway.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO spendings (date, location, cost) 
            VALUES (?, ?, ?)
        ''', (date, where, cost))
        conn.commit()
        conn.close()

    # Fetch all records from the database
    conn = sqlite3.connect('SqlliteDB/takeaway.db')
    c = conn.cursor()
    c.execute('SELECT * FROM spendings')
    records = c.fetchall()
    conn.close()


    # Get the total amount spent
    conn = sqlite3.connect('SqlliteDB/takeaway.db')
    c = conn.cursor()
    c.execute('SELECT sum(cost) FROM spendings')
    totalspend = c.fetchone()[0]
    conn.close()



    return render_template('Takeaway.html', records=records,totalspend=totalspend)

#-------------------------------------------------------------------------#
#----------------Dancing Game---------------------------------------------#


@app.route('/dancing_simulator')
def dancing_simulator():
    return render_template('Dancing.html')

@app.route('/run_simulation', methods=['POST', 'GET'])
def run_simulation():
    # Get bpm and population from request data
    bpm = int(request.args.get('bpm', 120))  # Default to 120 if not provided
    population = int(request.args.get('population', 100))  # Default to 100 if not provided

    
    # Initialize the simulation
    dg = DancingGame(bpm, population)
    
    # Initialize infected_calories properly
    infected_calories = dg.create_list()
    print(f"Infected calories initialized: {infected_calories}")  # Log for debugging
    
    total_infected = dg.start_infected
    remaining_pop = dg.population - dg.start_infected
    total_dead = 0
    total_alive = dg.population
    tick = dg.tick


    # Initialize the response to stream data back to the client
    def generate():
        nonlocal infected_calories, total_infected, remaining_pop, total_dead, total_alive, tick
        
        while len(infected_calories) > 0:
            tick += 1
            new_infected = 0
            died_this_tick = 0
            minutes=0
            hours=0
            day=0
            
            adjusted_infection_rate, adjusted_reduction, adjusted_infection_period = dg.adjust_rates()
            
            infected_calories = dg.cal_reduction(infected_calories,adjusted_reduction)

            died_this_tick, infected_calories = dg.remove_dead(infected_calories)
            
            new_infected = dg.new_infections(tick, adjusted_infection_period, remaining_pop, 
                                              
                                              infected_calories)
            
            # Update total counters
            total_infected += new_infected
            remaining_pop = max(dg.population - total_infected, 0)
            total_dead += died_this_tick
            total_alive = dg.population - total_dead
            # print(total_alive)
            minutes=tick*5
            hours=math.floor((tick*5)/60)
            days=math.floor(((tick*5)/60)/24)
            print(died_this_tick,new_infected)


            # Prepare the data to be sent to the client as SSE
            data = {
                'tick': tick,
                'minutes':minutes,
                'hours':hours,
                'days':days,
                'total_alive': total_alive,
                'total_dead': total_dead,
                'infected_count': total_infected,
                'new_infected':new_infected,
                'new_dead':died_this_tick
            }
            # print(data)
            
            try:
                json_data = json.dumps(data)  # Try serializing the data
                print("Serialized JSON:", json_data)  # Print the serialized JSON
            except Exception as e:
                print(f"Error serializing JSON: {e}")
                json_data = "{}"  # If serialization fails, send an empty object to avoid breaking the SSE
        


            # Yield the response in the correct SSE format
            yield f"data: {json_data}\n\n"
            print(len(infected_calories))
            
            # Add a sleep if you want the simulation to update at intervals
            time.sleep(0.5)
    
        # Once the simulation ends, yield a message to indicate completion
        yield "data: {\"message\": \"Simulation completed\"}\n\n"

    # Return the streaming response
    return Response(generate(), mimetype='text/event-stream')
print(Response)

#define some globel variable

@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)  
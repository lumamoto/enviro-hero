from pages.heros import heros
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

import time, random
import SessionState

from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts

#def data():
    # # DATA
    # st.header("Data")

    # # get year
    # year = st.slider("Year", min_value=1990, max_value=2020)

    # # get all countries
    # countries = df['Country'].unique()
    # # select country
    # country = st.selectbox('Select a Country', countries)

    # # show row for selected year and country
    # row = df[ (df['Year']==year) & (df['Country']==country) ]
    # st.dataframe(row)

    # # extract value in emissions column
    # emissions = row.values[0][2]
    # st.markdown(country + "'s emissions is " + str(emissions))

    # # display map
    # st.header("World Map")
    # display_map()

class Scenario:
    object_num = random.randint(0,10) # The number of objects
    base_weight = random.randint(0,10) # The effect this has on the environment
    good_descriptions = ['','Replace {} incandescent lightbulbs with ENERGY STAR ® lights'.format(object_num), 
                        'Enable the power management features on my computer',
                        'Line dry all my laundry',
                        'Wash clothes in cold water',
                        'Recycle cans, plastic, glass, newspapers and magazines',
                        'Drive {} fewer miles per year'.format(object_num),
                        'Perform regular maintenance on your vehicle',
                        'Go vegan','']
    bad_descriptions = ['','Use {} bottles of hairspray per week'.format(object_num),
                        'Cut down {} trees in the local nature reserve to build a treehouse'.format(object_num),
                        'Put an extra {} scoops of laundry detergent in the washing machine'.format(object_num),
                        'Take an extra {} minutes in the shower'.format(object_num),
                        'Use {} plastic bags when grocery shopping'.format(object_num),
                        'Leave the lights on for {} when your not around'.format(object_num),
                        'Using chemicals to kill weeds in your yard',
                        'Eating only processed meat products','Eating only processed meat products']


def game():
    st.title("🌎 Welcome to Planet Earth")
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    chart = st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
    ))
############

    # st.sidebar.title("Person Multiplier:")
    # num_people = st.sidebar.slider("Number of People", min_value=1, max_value=100)



    # read actions csv
    # actions_df = pd.read_csv("./data/actions.csv")
    # actions = actions_df["Action"]
    # selected_actions = st.multiselect("What will you do?", actions)

    # st.markdown("You chose to do the following: ")

    # total_co2 = 0
    # total_meth = 0
    # for action in selected_actions:
    #     st.markdown("     **·** " + action)
    #     row = actions_df[actions_df['Action']==action]
    #     co2 = row.values[0][1]
    #     total_co2 += int(co2)
    
    # st.subheader("Your Savings")
    # st.markdown("You will prevent **" + str(total_co2) + "** lbs. of CO2 from entering the atmosphere each year!")

    # st.subheader("Savings Multiplier")
    # # get number of people
    # num_people = st.slider("Number of People", min_value=1, max_value=1000000)
    # multiplier = total_co2 * num_people

    # if num_people > 1 and selected_actions:
    #     st.markdown("If **" + str(num_people) + "** people followed your footsteps, we would prevent **" + str(multiplier) + "** lbs. of CO2 from entering the atmosphere each year!")
    #     st.markdown("That's equivalent to the weight of **" + str(int(multiplier/900)) + "** concert grand pianos!")

########
    session_state = SessionState.get(q=1, co2=0, methane=0)
    scen = Scenario()

    q = session_state.q
    st.header("Question " + str(session_state.q))

    st.sidebar.header("Be the change you wish to see in the world.")
    st.sidebar.markdown("You may think that you alone might not be able to make a difference. But what if you had more people following your footsteps?")
    num_people = st.sidebar.slider(
        "View your own impact or a whole crowd's impact.", 
        min_value=1, 
        max_value=100)
    st.sidebar.markdown("Number of People: **" + str(num_people) + "**")
        
    if q == 1:
        heroes = ["World Wildlife Fund", "Green Peace", "National Geographic Society", "Rainforest Action Network", "Friends of the Earth"]
        hero = st.selectbox('Choose your Hero', heroes)
        st.subheader("Are you ready, " + hero + "?")
        if st.button('Yes'):
            st.success('Congrats! You are now the head of the organization and will make the decisions.')
            session_state.q = 2
            st.button('Next')

    if q == 2:
        st.subheader("What is your first policy?")
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('Your actions have positively affected the environment!')
            session_state.co2 = session_state.co2 - random.randint(1,3) * num_people
            session_state.methane = session_state.methane - random.randint(1,3) * num_people
            session_state.q = 3
            st.button('Next')
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('The global temperature rises by 0.1°.')
            session_state.co2 = session_state.co2 + random.randint(1,4) * num_people
            session_state.methane = session_state.methane + random.randint(1,3) * num_people
            session_state.q = 3
            st.button('Next')
    

    if q == 3:
        st.warning('📰 Breaking News: The polar ice caps have begun to melt!')
        st.subheader("What do you do?")
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('The melting has subsided... for now.')
            session_state.co2 = session_state.co2 - random.randint(1,5) * num_people
            session_state.methane = session_state.methane - random.randint(1,3) * num_people
            session_state.q = 4
            st.button('Next')
            
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error("There is nowhere for the polar bears to go!")
            session_state.co2 = session_state.co2 + random.randint(1,2) * num_people
            session_state.methane = session_state.methane + random.randint(1,3) * num_people
            session_state.q = 4
            st.button('Next')
            

    if q == 4:
        st.subheader("You have just woken up for the day.")
        st.subheader('What do you do?')
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('Research is underway!')
            session_state.co2 = session_state.co2 - random.randint(1,2) * num_people
            session_state.methane = session_state.methane - random.randint(1,4) * num_people
            session_state.q = 5
            st.button('Next')

            
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('Uh oh, that\'s not very hero-like.')
            session_state.co2 = session_state.co2 + random.randint(1,3) * num_people
            session_state.methane = session_state.methane + random.randint(1,3) * num_people
            session_state.q = 5
            st.button('Next')
           


    if q == 5:
        st.warning("🏭 BREAKING: Carbon dioxide at Record Levels in the Atmosphere")
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('The trees thank you.')
            session_state.co2 = session_state.co2 + random.randint(1,4) * num_people
            session_state.methane = session_state.methane - random.randint(1,3) * num_people
            session_state.q = 6
            st.button('Next')
            
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('Some people just want to watch the world burn.')
            session_state.co2 = session_state.co2 - random.randint(1,2) * num_people
            session_state.methane = session_state.methane + random.randint(1,3) * num_people
            session_state.q = 6
            st.button('Next')

        
    if q == 6:
        st.subheader("You are invited to a international dinner with powerful elites.")
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('“It’s no hyperloop, but the slide is still fun” says Elon.')
            session_state.co2 = session_state.co2 - random.randint(1,5) * num_people
            session_state.methane = session_state.methane - random.randint(1,4) * num_people

        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('UN instigates the Bristol Accord')
            st.markdown("The wheels are turning, but how long will it take?")
            session_state.co2 = session_state.co2 + random.randint(1,2) * num_people
            session_state.methane = session_state.methane + random.randint(1,3) * num_people
            session_state.q = 7
            st.button('Next')
    
    if q == 7:
        st.subheader("A report has highlighted that petrol cars are one of the worlds biggest poluters")
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('The big electric switch has started!')
            st.markdown('Pollution from petrol goes down dramatically, but the environment takes a hit\nfrom having to build so many new electric cars so quickly. ')
            session_state.co2 = session_state.co2 - random.randint(1,6) * num_people
            session_state.methane = session_state.methane - random.randint(1,7) * num_people
            session_state.q = 8
            st.button('Next')
            
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('Keep on rolling')
            st.markdown("Life continues as normal. Which means increasing polution and carbon emissions.\nPeople are angry you're not doing anything to help. ")
            session_state.co2 = session_state.co2 + random.randint(1,5) * num_people
            session_state.methane = session_state.methane + random.randint(1,4) * num_people
            session_state.q = 8
            st.button('Next')
            
    if q == 8:
        st.subheader("Your scientists have told you our reliance on meat and fish has massively increased the world's carbon footprint.")
        st.subheader('What will you do about it?')
        if st.button('💠' + scen.good_descriptions[session_state.q]):
            st.success('People have embraced the new diet!')
            session_state.co2 = session_state.co2 - random.randint(1,6) * num_people
            session_state.methane = session_state.methane - random.randint(1,7) * num_people
            session_state.q = 9
            st.button('Next')
            
        if st.button('🔥' + scen.bad_descriptions[session_state.q]):
            st.error('People have refused to embrace the new diet!')
            session_state.co2 = session_state.co2 + random.randint(1,5) * num_people
            session_state.methane = session_state.methane + random.randint(1,4) * num_people
            session_state.q = 9
            st.button('Next')

    if q == 9:
        st.markdown('Your term has come to an end.')
        if(session_state.co2 > 70):
            st.subheader('The citizens of the world despise you!')
        else:
            st.balloons()
            st.subheader('The citizens of the world thank you!')

        st.markdown('Your scores are...')
        st.title(f"CO₂: {session_state.co2} lbs")
        st.title(f"Methane: {session_state.methane} lbs")
        if st.button("Play Again"):
            session_state.q = 1
            session_state.co2 = 0
            session_state.methane = 0

    
    st.sidebar.title(f"CO₂: {session_state.co2} lbs")
    if(session_state.co2 <= 0):
        co2_bar = st.sidebar.progress(0)
    elif(session_state.co2 >= 100):
        co2_bar = st.sidebar.progress(100)
    else:
        co2_bar = st.sidebar.progress(session_state.co2)

    st.sidebar.title(f"Methane: {session_state.methane} lbs")
    if(session_state.methane <= 0):
        meth_bar = st.sidebar.progress(0)
    elif(session_state.methane >= 100):
        meth_bar = st.sidebar.progress(100)
    else:
        meth_bar = st.sidebar.progress(session_state.methane)

    
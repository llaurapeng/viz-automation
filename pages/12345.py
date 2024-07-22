event = 12345

import pandas as pd
#from .. import start as viz
import streamlit as st
import openpyxl
from create_viz import Viz
from PIL import Image
from rembg import remove 
import os

# Define your custom CSS---------------------------------

obj = Viz (st.session_state [f'per_data{event}'], st.session_state [f'per_weight_benchmarks{event}'],st.session_state [f'per_names_ref{event}'])


#border radius 50 
custom_css_company = f"""
        <style>
         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .my-container_comp {{
        background-color: {st.session_state['primaryColor']};
        padding: 10px;
        border-radius: 50px; 
        margin-top: 2;  /* Remove top margin */
        margin-bottom: 30px;  /* Remove bottom margin */
        text-align: center;  /* Center text horizontally */
        font-size: 40px;
        font-weight: bold;
        font-family 'Poppins';
        color: {st.session_state['textColor']};  /* Optional: Specify text color */
        }}
        </style>
        """

#TITLE ---------------------------------------------

if 'company_name' in st.session_state and st.session_state ['company_name'] == ' ': 
    print ('empty')
    print (st.session_state ['logo'])
elif 'company_name' in st.session_state: 

        st.markdown(custom_css_company, unsafe_allow_html=True)
        company = st.session_state ['company_name']
        st.markdown(f'<div class="my-container_comp"> {company}</div>', unsafe_allow_html=True)


#ROX TITLE ---------------------------------------------

st.markdown(custom_css_company, unsafe_allow_html=True)
st.markdown('<div class="my-container_comp"> Return on Experience Scorecard (ROX)</div>', unsafe_allow_html=True)

#LOGO IMAGE -------------------------------------------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns([1, 1, 1,1,1])  # The middle column will be twice as wide as the side columns

print ('HI')
with col3:
    #st.image(st.session_state ['logo'])
    if 'logo' in st.session_state and st.session_state['logo'] != None:
        st.image(st.session_state ['logo'])
        print ('this')

    elif 'remove' in st.session_state and st.session_state['remove'] != None:
        st.image (st.session_state ['remove'])


#Activation name and dateslide-------------------------------------------------------------------------------------------------------

#border radius 80 

custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
.my-container {{
background-color: {st.session_state['primaryColor']};
padding: 10px;
border-radius: 80px;
margin-top: 2;  /* Remove top margin */
margin-bottom: 20px;  /* Remove bottom margin */
font-size: 30px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
font-family 'Poppins';
color: {st.session_state['textColor']};  /* Optional: Specify text color */
}}
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

left, center, right = st.columns([1,5,1])
data = obj.data
eventName = data ['Event Name'].values[0]
with center: 
    st.markdown(f'<div class="my-container">{eventName}</div>', unsafe_allow_html=True)

#border radius 20

custom_css2 = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
.my-container2 {{
background-color: {st.session_state['primaryColor']};
padding: 1px;
border-radius: 20px;
margin-top: 1px;  /* Remove top margin */
margin-bottom: 20px;  /* Remove bottom margin */
font-size: 23px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
font-family 'Poppins';
color: {st.session_state['textColor']};  /* Optional: Specify text color */
}}
</style>
"""

st.markdown(custom_css2, unsafe_allow_html=True)

left, center, right = st.columns([1,3,1])
with center: 
    st.markdown(f'<div class="my-container2">Performance Report Card | {obj.date_range}</div>', unsafe_allow_html=True)


#first slide-------------------------------------------------------------------------------------------------------
left, right = st.columns (2)

with left: 
    container1 = st.container (border = False, height = 500)
    container1.markdown('<div class="my-container2">ROX Score</div>', unsafe_allow_html=True)
    #st.write (st.session_state['primaryColor'])
    container1.plotly_chart (obj.fig4 (st.session_state['primaryColor'], st.session_state ['textColorPlots']),use_container_width=True)


with right:
    container2 = st.container (border = False, height = 500)
    container2.markdown('<div class="my-container2">Score Summary</div>', unsafe_allow_html=True)
    container2.plotly_chart (obj.table1 (st.session_state['primaryColor'], st.session_state ['textColor']), use_container_width = True)


with st.expander ('ROX Score Breakdown'):
    st.markdown('<div class="my-container2">Score Summary</div>', unsafe_allow_html=True)
    st.plotly_chart (obj.table2 (st.session_state['primaryColor'], st.session_state ['textColor']),use_container_width = True)

#second slide-------------------------------------------------------------------------------------------------------




left, right = st.columns ([1,2])

with right: 
    st.plotly_chart (obj.fig3(st.session_state['primaryColor'], st.session_state ['textColorPlots']))

with left: 
    custom_css3 = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
.my-container3 {{
background-color: {st.session_state['primaryColor']};
padding: 50px;
margin-top: 0px;
border-radius: 20px;
margin-bottom: 0px;  /* Remove bottom margin */
height: 300px
font-size: 19px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
font-family 'Poppins';
color: {st.session_state['textColor']};  /* Optional: Specify text color */
}}
</style>
"""
    st.markdown(custom_css3, unsafe_allow_html=True)
    st.markdown(
        '<div class="my-container3">'
        '<span style="font-size:30px;">ROX Visual Breakdown</span><br>'
        '<span style="font-size:20px;">Total Rox<br> </span>'
        f'<span style="font-size:80px;">{obj.rox_output}</span>'
        '</div>', 
        unsafe_allow_html=True
    )


#import packages ---------------------------------
import pandas as pd
import create_viz as viz
import streamlit as st
import openpyxl

# Set page configuration---------------------------------
st.set_page_config(layout="wide",
                   page_title="Verizon Survey Vizualizations")
# Define your custom CSS---------------------------------

background = 'red'
custom_css = """
<style>
.my-container {
 background-color: red;
 padding: 10px;
 border-radius: 20px;
 margin-top: 2;  /* Remove top margin */
 margin-bottom: 20px;  /* Remove bottom margin */
font-size: 40px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
color: white;  /* Optional: Specify text color */
}
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="my-container">Activation Name</div>', unsafe_allow_html=True)



custom_css2 = """
<style>
.my-container2 {
 background-color: red;
 padding: 1px;
 border-radius: 20px;
 margin-top: 2;  /* Remove top margin */
 margin-bottom: 20px;  /* Remove bottom margin */
font-size: 25px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
color: white;  /* Optional: Specify text color */
}
</style>
"""

st.markdown(custom_css2, unsafe_allow_html=True)

left, center, right = st.columns([1,3,1])
with center: 
    st.markdown(f'<div class="my-container2">Performance Report Card | {viz.date_range}</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 3, 1])  # The middle column will be twice as wide as the side columns

with col2:
    st.image('img.png')
    #, use_column_width=True

#first slide-------------------------------------------------------------------------------------------------------
left, right = st.columns (2)

with left: 
    container1 = st.container (border = False, height = 500)
    container1.markdown('<div class="my-container2">ROX Score</div>', unsafe_allow_html=True)
    container1.plotly_chart (viz.fig4,use_container_width=True)


with right:
    container2 = st.container (border = False, height = 500)
    container2.markdown('<div class="my-container2">Score Summary</div>', unsafe_allow_html=True)
    container2.plotly_chart (viz.fig)


with st.expander ('ROX Score Breakdown'):
    st.markdown('<div class="my-container2">Score Summary</div>', unsafe_allow_html=True)
    st.plotly_chart (viz.fig2)

#second slide-------------------------------------------------------------------------------------------------------

left, right = st.columns ([1,2])

with right: 
    st.plotly_chart (viz.fig3)

with left: 
    custom_css3 = """
<style>
.my-container3 {
 background-color: red;
 padding: 50px;
 margin-top: 40px;
 border-radius: 20px;
 margin-bottom: 20px;  /* Remove bottom margin */
 height: 300px;
font-size: 25px;
text-align: center;  /* Center text horizontally */
font-weight: bold;
color: white;  /* Optional: Specify text color */
}
</style>
"""
    st.markdown(custom_css3, unsafe_allow_html=True)
    st.markdown(
        '<div class="my-container3">'
        '<span style="font-size:30px;">ROX Visual Breakdown</span><br>'
        '<span style="font-size:20px;">Total Rox<br> </span>'
        f'<span style="font-size:80px;">{viz.rox_output}</span>'
        '</div>', 
        unsafe_allow_html=True
    )
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import openpyxl
import streamlit as st
from PIL import Image
from rembg import remove 
import onnxruntime
import io
import os
import time

#check if logo and remove key exists if not set to False



# Set page configuration---------------------------------
st.set_page_config(layout="wide",
                   page_title="Verizon Survey Vizualizations")


class ThemeManager:
    def __init__(self):
        self.colorss = {}
        self.initialize_colors()
        
    def initialize_colors(self):
        # Set default values for session state if not already set
        if 'primaryColor' not in st.session_state:
            st.session_state['primaryColor'] = '#00f900'
            self.colorss['primaryColor'] = st.session_state['primaryColor']


        if 'backgroundColor' not in st.session_state:
            st.session_state['backgroundColor'] = '#ffffff'
            self.colorss['backgroundColor'] = st.session_state['backgroundColor']

        if 'secondaryBackgroundColor' not in st.session_state:
            st.session_state['secondaryBackgroundColor'] = '#f0f0f0'
            self.colorss['secondaryBackgroundColor'] = st.session_state['secondaryBackgroundColor']

        if 'textColor' not in st.session_state:
            st.session_state['textColor'] = '#000000'
            self.colorss['textColor'] = st.session_state['textColor']

        if 'textColorPlots' not in st.session_state:
            st.session_state['textColorPlots'] = '#000000'



    def reconcile_theme_config(self):

        keys = ['primaryColor', 'backgroundColor', 'secondaryBackgroundColor', 'textColor']
        has_changed = False
        for key in keys:
            if st.session_state.get(key) and st.session_state[key] != st._config.get_option(f'theme.{key}'):
                st._config.set_option(f'theme.{key}', st.session_state[key])
                has_changed = True
        if has_changed:
            st.rerun()
    

    #RESIZE IMAGE --------------------------------------------------------

    def resize_image_aspect_ratio(self, input_path, new_width, new_height):
        with Image.open(input_path) as img:
            # Calculate the aspect ratio of the original image
            width_percent = new_width / float(img.size[0])
            height_percent = new_height / float(img.size[1])
            
            # Choose the smallest ratio to ensure the image fits within the new dimensions
            min_percent = min(width_percent, height_percent)
            
            # Calculate the new width and height based on the smallest ratio
            new_width = int(float(img.size[0]) * min_percent)
            new_height = int(float(img.size[1]) * min_percent)
            
            # Resize the image
            new_img = img.resize((new_width, new_height), Image.LANCZOS)  # Use Image.LANCZOS filter for high-quality resizing
        
        return new_img
    

    #UPLOAD FILE --------------------------------------------------------
    
    def upload_file (self):
        response1 = st.radio ('Do you need to upload a file?',
                                 ['yes','no'],
                                 index = 1)
        
        #yes to upload file then update the session state
        if response1 == 'yes':
            st.session_state ['uploaded_file'] = st.file_uploader("Upload an Excel file", type=['xlsx', 'xls'])
            uploaded_file = st.session_state ['uploaded_file']
        #if there is not uploaded file then set it to none
        else:
            uploaded_file = None
        # Check if a file is uploaded

        #if there is no uploaded file then create a warning
        if uploaded_file is None:
            st.warning('please upload an Excel file.')

        #if there IS A uploaded file then...
        #put the uploaded file in the session state
        #write the python files for each event 

        #if there is a uploaded file
        else:
            # Read the Excel file
            df = pd.read_excel(uploaded_file,sheet_name=None)
            st.session_state ['uploaded_file'] = df

            #writ the python files
            self.writefile()

        return response1
    
    
    
    #CLEAR WORKSPACE --------------------------------------------------------

    def clear_space(self):
        clear_resp = st.radio ('Would you like to clear your workspace?',
                                 ['yes','no'],
                                 index = 1)
        #CLEARS APP ---------------------------------------
        if clear_resp == 'yes':
            # Specify the directory path
            curr_dir = os.getcwd()
            print (curr_dir)
            # Specify the new file name and path
            directory = '/mount/src/viz-automation/pages'
           
            # Iterate over all files in the directory
            for filename in os.listdir(directory):
                filePath = os.path.join(directory, filename)
                try:
                    # Check if the path is a file (not a directory)
                    if os.path.isfile(filePath):
                        # Attempt to remove the file
                        os.remove(filePath)
                        print(f"Deleted {filename}")
                except OSError as e:
                    print(f"Error deleting {filename} : {e.strerror}")
                
            st.session_state ['uploaded_file'] = None
            #st.session_state['page_titles'] = []

        return clear_resp
            
    
    #modify the theme of the report
    def modify_theme(self):
        st.session_state['primaryColor'] = st.color_picker('Primary Color', st.session_state['primaryColor'])
        st.session_state['backgroundColor'] = st.color_picker('Background Color', st.session_state['backgroundColor'])
        st.session_state['secondaryBackgroundColor'] = st.color_picker('Secondary Background Color', st.session_state['secondaryBackgroundColor'])
        st.session_state['textColor'] = st.color_picker('Text Color', st.session_state['textColor'])
        st.session_state['textColorPlots'] = st.color_picker('Text Color for plots', st.session_state['textColorPlots'])
            

    def change_logo (self):
        response = st.radio ('Would you like to change add a image?',
                            ['yes','no'],
                            index = 1)
        
        left, right = st.columns (2)

        #change logo DONT DO ANYTHING------------------------------------
        with left: 
            #response = response to change the logo 
            if response == 'yes':
                st.session_state['logo'] = st.file_uploader ('Upload a image for the logo: ', type = ['png','jpeg'])
                if st.session_state['logo'] is not None:
                    resized = self.resize_image_aspect_ratio(st.session_state ['logo'], 200,300)
                    momo = Image.open ('momo.png')

                    # Resize the momo image to a smaller size
                    momo.thumbnail((30, 30), Image.LANCZOS) 

                    base_width, base_height = resized.size
                    overlay_width, overlay_height = momo.size

                    position = (base_width - overlay_width, base_height - overlay_height)
                    
                    resized = resized.convert("RGBA")
                    momo = momo.convert("RGBA")
                    
                    resized.paste(momo, position, momo)

                    st.image (resized)
                    st.session_state ['logo'] = resized
               
        #change logo REMOVE BACKGROUND------------------------------------
        with right: 
            if response == 'yes':
                st.session_state['remove'] = st.file_uploader ('Upload a image to remove the background: ', type = ['png','jpeg'])
                if st.session_state['remove'] is not None:
            
                    #resize the image
                    resized = self.resize_image_aspect_ratio(st.session_state['remove'], 200,300)

                    resized = remove (resized)

                    momo = Image.open ('momo.png')
                    # Resize the momo image to a smaller size
                    momo.thumbnail((35, 35), Image.LANCZOS) 

                    base_width, base_height = resized.size
                    overlay_width, overlay_height = momo.size

                    position = (base_width - overlay_width, base_height - overlay_height)
                    
                    resized = resized.convert("RGBA")
                    momo = momo.convert("RGBA")
                    
                    resized.paste(momo, position, momo)

                    st.image (resized)
                    st.session_state ['remove'] = resized
        

    def modify_table (self):
        #find all the unique events
        if 'events' in st.session_state: 
            events = st.session_state ['events']
            events_choosen = st.multiselect ('Would you like to modify any of these events benchmarks?',
                    events)
            
        #store all the original data
        original_data = {}
        for event in events_choosen:
                original_data[event] = st.session_state [f'per_weight_benchmarks{event}']
                st.session_state [f'per_weight_benchmarks{event}'] = st.data_editor (st.session_state [f'per_weight_benchmarks{event}'])
                orginal = st.checkbox (f'Revert back to orginal for {event}', value = False)
                
                if orginal:
                    st.session_state [f'per_weight_benchmarks{event}'] = st.session_state [f'per_weight_benchmarks{event}_original']


    def apply_theme(self):
        #UPLOAD A FILE  ---------------------------------------------------------------
        uploadNum = self.upload_file()

        st.write("---")

         #CLEAR THE SPACE ---------------------------------------------------------------
        clearVal = self.clear_space()

        st.write("---")

        #can only make changes if you choose not to clear the workspace and there is uploaded file
        #CHANGE THE DATA ---------------------------------------------------------------
    
   
        if clearVal == 'no' and 'uploaded_file' in st.session_state and st.session_state ['uploaded_file'] is not None:
            self.modify_table()

        st.write("---")

        #APPLY THE THEME  ---------------------------------------------------------------
        self.modify_theme()

        st.write("---")

        #CHANGE THE LOGO  ---------------------------------------------------------------
        self.change_logo()

        st.write("---")
    
        #RERUN THE WEB PAGE TO SEE THEME UPDATES  ---------------------------------------------------------------
        self.reconcile_theme_config()

    def writefile(self):
        file_content = '''
curr_dir = os.getcwd()
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

'''

        #end of file content -------------------------------------------

        if 'uploaded_file' in st.session_state: 
            uploaded = st.session_state ['uploaded_file']

            if uploaded is None:
                st.write ('Please put in a data frame')

            #if not empty------------------
            else:

                #find all the event ids in the data frame
                for sheet_name, df in uploaded.items():
        
                    
                    if sheet_name == 'Data':
                        data = df 
                        st.session_state ['data'] = data
                    if sheet_name == 'WeightandBenchmarks':
                        weight_benchmarks = df
                        st.session_state ['weight_benchmarks'] = weight_benchmarks
                    if sheet_name == 'Names_Ref':
                        names_ref = df
                        st.session_state ['names_ref'] = names_ref
                    
                #finds all the events
                events = data['Event ID'].unique()
                st.session_state ['events'] = events

                #creates the filtered data sets
                for event in events: 
                    per_data = data [data['Event ID'] == event]
                    st.session_state [f'per_data{event}'] = per_data
                    st.session_state [f'per_data{event}_original'] = per_data
            
                    per_weight_benchmarks = weight_benchmarks[weight_benchmarks['Event ID'] == event]
                    st.session_state [f'per_weight_benchmarks{event}'] = per_weight_benchmarks
                    st.session_state [f'per_weight_benchmarks{event}_original'] = per_weight_benchmarks

                    per_names_ref = names_ref [names_ref['Event ID'] == event]
                    st.session_state [f'per_names_ref{event}'] = per_names_ref
                    st.session_state [f'per_names_ref{event}_original'] = per_names_ref


                    curr_dir = os.getcwd()

                    # Specify the new file name and path
                    new_file_path = os.path.join(curr_dir, f'/pages/{event}.py')

                    try:
                        with open(new_file_path, 'w') as f:
                            f.write (f'''event = {event}''')
                            f.write(file_content)
                            print(f"New file '{new_file_path}' created successfully.")
                    except IOError:
                        print(f"Error: Could not write to file '{new_file_path}'.")


# Usage
theme_manager = ThemeManager()
theme_manager.apply_theme()

print ('----------')





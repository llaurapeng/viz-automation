#IMPORT PACKAGES ---------------------------------
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

#READ IN DATA---------------------------------

excel_data = pd.read_excel('sample.xlsx', sheet_name=None)

for sheet_name, df in excel_data.items():
    if sheet_name == 'Data':
        data = df
    if sheet_name == 'WeightandBenchmarks':
        weight_benchmarks = df
    if sheet_name == 'Names_Ref':
        names_ref = df

#CREATE DF TO USE --------------------------------

#date structure
timestamp1 = str (data ['Event Start Date'].values [0])
timestamp1 =timestamp1 [:10]

timestamp2 = str (data ['Event End Date'].values [0])
timestamp2 =timestamp2 [:10]


date_range = timestamp1+ ':' + timestamp2



#makes a dictionary with all the KPIs

values = {'KPI ID':[],
         'Values':[],
         'Benchmark':[],
         'Weight':[],
         'Index':[],
         'Input':[]}

for x in data.columns:
    if 'KPI' in x:
        values['KPI ID'].append (x)
        id_val = data[x].values[0]
        values ['Values'].append (id_val)


#add benchmark, weight, index, input, output
rox_output = 0

for key in values['KPI ID']:
    #put the benchmark in-------------------------
    benchmark = weight_benchmarks.loc[weight_benchmarks['KPI ID'] == key, 'Benchmark']
    benchmark = benchmark.values[0]
    values['Benchmark'].append (benchmark)
    
    #put the weight in-----------------------------
    weight = weight_benchmarks.loc[weight_benchmarks['KPI ID'] == key, 'Weight']
    weight = weight.values[0]
    values['Weight'].append (weight)

    
    #calculate the index---------------------------

    #find the KPI ID index so can index values

    ind = values['KPI ID'].index (key)
    
    index = (1+ ((values['Values'][ind] - benchmark)/benchmark)) * 100
    values['Index'].append (round (index,2))

    #calculate the rox input---------------------------

    input = round (index * weight)
    values['Input'].append (input)
    rox_output+=input
    
    
    
print (values)
    
rox_output = round (rox_output)


#FINAL DATA FRAME CREATION ---------------------------------

df = pd.DataFrame (values)

#merge dataframes

include_col = ['KPI ID','KPI Name', 'Bucket','Bucket Name']

names_ref = names_ref [include_col]


df = pd.merge (df, names_ref, on = 'KPI ID', how = 'left')


#sort by buckets
sorted_df = df.sort_values (by = 'Bucket', ascending = True)
sorted_df.head (10)

#PUT VALUES INTO A LIST ---------------------------------

KPI_name = sorted_df ['KPI Name'].values 
Weights = sorted_df ['Weight'].values
KPI_comb = []
Input = sorted_df ['Input'].values
for i in range (len (Weights)):
    KPI_comb.append (f'<b> {KPI_name[i]}</b>' + ' (' + str (Weights[i] * 100) + '%' + ')')

Buckets = sorted_df ['Bucket Name'].values
print (Buckets)
Values = sorted_df ['Values'].values
Benchmark = sorted_df ['Benchmark'].values
Index = sorted_df ['Index'].values

#TABLE COLORING ---------------------------------

colors = []
text_color = []
for i, row in sorted_df.iterrows ():
    bucketNum = row['Bucket'].split () [1]
    if int (bucketNum) % 2 != 0:
        #if odd number then white
        colors.append ('white')
    else:
        colors.append ('#E1EEF2')

    if row ['Index'] > 120:
        text_color.append ('green')
    elif row['Index'] <=80:
        text_color.append ('red')
    else:
        text_color.append ('black')

colors_text = [
    ['black', 'black', 'black', 'black','black', 'black', 'black', 'black','black'],
    ['black', 'black', 'black', 'black','black', 'black', 'black', 'black','black'],
    ['black', 'black', 'black', 'black','black', 'black', 'black', 'black','black']
]
colors_text = colors_text + [text_color]

#TABLE 1  ------------------------------------------------------------------

#table 1 specific coloring
header_color = 'white'
header_fill_color = 'black'


fig = go.Figure(data=[go.Table(
    header=dict(values=['<b>KPI(Weight)</b>', 
                        '<b>Result</b>', 
                        '<b>Benchmark</b>',
                        '<b>Index</b>'],
               line=dict(width=0),
               font=dict(color=header_color, size = 13),
                fill_color = header_fill_color
               ),
    cells=dict(values=[KPI_comb, Values, Benchmark, Index],
               align=['left', 'center', 'center', 'center'], 
              font=dict(color=colors_text),
              fill = dict (color = [colors]),
              line=dict(width=0)
              )
    
)])

fig.update_layout(
    height=700,  # Specify the height in pixels
    margin=dict(l=0, r=0, t=20, b=0)  # Optional: Adjust margins if needed
)

#TABLE 2  ------------------------------------------------------------------

#format + color specifics for table 2

#modify brand name so that any duplicates would have a blank space

start = ''
Buckets_3 = []
print (Buckets)

for i in range (len (Buckets)):
    if Buckets[i] is not start:
        Buckets_3.append (f'<b> {Buckets[i]}</b>')
        start = Buckets[i]
    else:
        Buckets_3.append(' ')

print (Buckets_3)

#bold the KPI values

for i in range (len (Weights)):
    KPI_name [i] = f'<b> {KPI_name[i]}</b>'

#change font sizes

cell_font_size = [16, 12, 12, 12, 12, 12]  


#add colors

colors_text.append (['black', 'black', 'black', 'black','black', 'black', 'black', 'black','black'])
colors_text.append (['black', 'black', 'black', 'black','black', 'black', 'black', 'black','black'])

fig2 = go.Figure(data=[go.Table(
    header=dict(values=['',
                        '<b>KPI Name</b>', 
                        '<b>Result</b>', 
                        '<b>Benchmark</b>',
                        '<b>Index</b>',
                        '<b>Weight</b>',
                        '<b>ROX Input</b>'
                       ],
               line=dict(width=0),
               font=dict(color='white', size = 13),
                fill_color = 'black'
               ),
    cells=dict(values=[Buckets_3,KPI_name, Values, Benchmark, Index, Weights, Input],
               align=['left', 'center', 'center', 'center'], 
              font=dict(color=colors_text, size = cell_font_size),
              fill = dict (color = [colors]),
              line=dict(width=0)
              )
    
)])

if rox_output > 120: 
    text_color_rox = 'green'
    dot = 'green'

elif rox_output < 80: 
    text_color_rox = 'red'
    dot = 'red'
else: 
     text_color_rox = 'yellow'
     dot = 'purple'


border_color = 'white'
# Add annotation outside the table
fig2.add_annotation(
    xref='paper', yref='paper',
    x=.96, y=-.15,  # Coordinates relative to the entire plot
    text='ROX: ' + str (rox_output),
    showarrow=False,
    font=dict(size=25, color=text_color_rox),
    borderpad=4,  # Padding around the annotation box
    borderwidth=5,  # Border width
    bordercolor=border_color  # Border color

)

fig2.update_layout (margin=dict(t=20))

#THIRD VIZ (histogram) ------------------------------------------------------------------


pio.templates.default = "plotly_white"
# Assuming sorted_df contains your data and variables are defined (KPI_name, Index, Buckets)
fig3 = px.histogram(sorted_df, x=KPI_name, y=Index,
                   color=Buckets, barmode='group',
                   height=400, text_auto=True)
fig3.update_layout(xaxis_title="KPI Names",
                  yaxis_title="Index",
                  title = 'Distribution of Index for KPIs',
                  legend_title_text="Type")


#FOURTH VIZ (gauge plot) ------------------------------------------------------------------



fig4_textcolor = 'white'
fig4 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=rox_output,
    number = {'font': {'color': text_color_rox}}, 
    domain={'x': [0, 1], 'y': [0, 1]},
    #title={'text': "ROX Score"},
    gauge={
        'axis': {'range': [0, 200], 'tickwidth': 1, 'tickcolor': "black"},
        'bar': {'color': "black"},
        'steps': [
            {'range': [0, 80], 'color': 'red'},
            {'range': [80, 120], 'color': 'yellow'},
            {'range': [120, 200], 'color': '#26ff26'}
        ],
        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}
    }
))

fig4.add_annotation (
    x = 0.5,
    y = 0, 
    text = '<br> (Weighted) </br>',
    showarrow = False
)

fig4.add_annotation (
    x = 1,
    y = 0, 
    text = '<b> Above Threshold </b>',
    showarrow = False
)

fig4.add_annotation (
    x = 0,
    y = 0, 
    text = '<b> Below Threshold </b>',
    showarrow = False
)

fig4.update_layout (font=dict(family="sans serif",size=18,color=fig4_textcolor),
                    margin=dict(t=0))
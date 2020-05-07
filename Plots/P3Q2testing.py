import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df2 = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df3 = pd.read_csv('../Datasets/Weather2014-15.csv')
df4 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
app = dash.Dash()

# Bar chart data
barchart_df = df1[df1['Country'] == 'US']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['State'])['Confirmed'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['State'], y=barchart_df['Confirmed'])]

# Stack bar chart data
stackbarchart_df = df4.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


stackbarchart_df = stackbarchart_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()

trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df3
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['actual_max_temp'], mode='lines', name='Weather')]

# Multi Line Chart
multiline_df = df3
multiline_df['date'] = pd.to_datetime(multiline_df['date'])

trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines', name='Max')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines', name='Min')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='Mean')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
#bubble_df = df3.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
#buble_df = bubble_df.sort_values(by=['month'], ascending=[False]).head(20).reset_index()

#data_bubblechart = [
#    go.Scatter(x=bubble_df['average_min_temp'],
#               y=bubble_df['average_max_temp'],
#               text=bubble_df['date'],
#               mode='markers',
#               marker=dict(size=bubble_df['average_max_temp'], color=bubble_df['average_max_temp'] / 200, showscale=True))
#]

bubble_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
bubble_df['Unrecovered'] = bubble_df['Confirmed'] - bubble_df['Deaths'] - bubble_df['Recovered']
bubble_df = bubble_df[(bubble_df['Country'] != 'China')]
bubble_df = bubble_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['Recovered'],
               y=bubble_df['Unrecovered'],
               text=bubble_df['Country'],
               mode='markers',
               marker=dict(size=bubble_df['Confirmed'] / 200, color=bubble_df['Confirmed'] / 200, showscale=True))
]
# Heatmap
data_heatmap = [go.Heatmap(x=df3['day'],
                   y=df3['month'],
                   z=df3['record_max_temp_year'].values.tolist(),
                   colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Coronavirus COVID-19 Global Cases -  1/22/2020 to 3/17/2020', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 countries of selected continent.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),

    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
    ],
        value='Europe'
    ),
    html.Br(),

    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 states of the US.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases in The US',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),


    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the Gold, Silver, Bronze medals of Olympic 2016 of 20 first top countries.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Q3 stack of all medals of olympic 2016 of first top 20',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'All medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),



    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart to represent the actual max temperature of each month in weather statistics.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Q2 total medals of olympic 2016 of first top 20',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Actual max temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),



    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div( 'This line chart represent the actual max, min and mean temperature of each month in weather statistics.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Max, Min and mean',
                      xaxis={'title': 'date'}, yaxis={'title': 'temp'})
              }
              ),

    html.Hr(style={'color': '#7FDBFF'}),
#   down here is my attemp for making bubble of part 1 and 2 but it makes errors so I gotta put it out
    #
#    html.H3('Bubble chart', style={'color': '#df1e56'}),
#    html.Div(
#        'This bubble chart represent the average min and max temperature of each month in weather statistics.'),
#    dcc.Graph(id='graph6',
#              figure={
#                  'data': data_bubblechart,
#                  'layout': go.Layout(title='average min/max temp',
#                                      xaxis={'title': 'date'}, yaxis={'title': 'temp'},
#                                      hovermode='closest')
#              }
#              ),
html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Corona Virus recovered and under treatment of all reported countries except China.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases',
                                      xaxis={'title': 'Recovered Cases'}, yaxis={'title': 'under Treatment Cases'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),



    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the recorded max temperature on day of week and month of year. .'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='recorded max temp',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month of Year'})
              }
              ),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),

    dcc.Dropdown(
        id='select-continent7',
        options=[
            {'label': 'Monday', 'value': 'Monday'},
            {'label': 'Tuesday', 'value': 'Tuesday'},
            {'label': 'Wednesday', 'value': 'Wednesday'},
            {'label': 'Thursday', 'value': 'Thursday'},
            {'label': 'Friday', 'value': 'Friday'},
            {'label': 'Saturday', 'value': 'Saturday'},
            {'label': 'Sunday', 'value': 'Sunday'}
    ],
        value='Monday'
    ),
    html.Br(),
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Corona Virus Confirmed Cases in '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of confirmed cases'})}

#testing heatmap seleciton

@app.callback(Output('graph7', 'figure'),
              [Input('select-continent7', 'value')])
def update_figure(selected_continent7):
    filtered_df = df3[df3['day'] == selected_continent7]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['day'])['record_max_temp'].sum().reset_index()
    new_df = new_df.sort_values(by=['record_max_temp'], ascending=[False]).head(20)
    data1 = [go.Heatmap(x=df3['day'],
                   y=df3['month'],
                   z=df3['record_max_temp_year'].values.tolist(),
                   colorscale='Jet')]
    return {'data': data1, 'layout': go.Layout(title='It is '+selected_continent7,
                                                                   xaxis={'title': 'day of week'},
                                                                   yaxis={'title': 'month of year'})}


if __name__ == '__main__':
    app.run_server()
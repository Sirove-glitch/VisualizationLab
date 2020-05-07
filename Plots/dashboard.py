"""
Interactive Data Visualization Dashboard
Authors: ITSC 3155 Group 24: Diego, Dylan Masi, Nick, Tri Tran, Trent Woolard

Using pre-formatted example data
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import base64
import datetime
import io

app = dash.Dash()


df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
barchart_df = df1[df1['Country'] == 'US']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['State'])['Confirmed'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['State'], y=barchart_df['Confirmed'])]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Interactive  Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Upload a comma-delimited Excel spreadsheet and select which format to view',
             style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload'),

    dcc.Tabs(id='tabs-graphs', value='tab-1', children=[
        dcc.Tab(label='Data Table', value='tab-1'),
        dcc.Tab(label='Bar Chart', value='tab-2'),
    ]),

    html.Div(id='tabs-graphs-content')
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line
    ])


# Parse file upload
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Tab display
@app.callback(Output('tabs-graphs-content', 'children'),
              [Input('tabs-graphs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                html.H3('Place Holder Content')
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(id='graph2',
                      figure={
                          'data': data_barchart,
                          'layout': go.Layout(title='Corona Virus Confirmed Cases in The US',
                                              xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})
                      })
        ])


if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df['Unrecovered'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

df = df[(df['Country'] != 'China') & (df['Country'] != 'Others')]

new_df = df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()

data = [
    go.Scatter(x=new_df['Recovered'],
               y=new_df['Unrecovered'],
               text=new_df['Country'],
               mode='markers',
               marker=dict(size=new_df['Confirmed'] / 100,color=new_df['Confirmed'] / 100, showscale=True))
]

layout = go.Layout(title='Corona Virus Confirmed Cases', xaxis_title="Recovered Cases", yaxis_title="Unrecovered Cases", hovermode='closest')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='bubblechart.html')
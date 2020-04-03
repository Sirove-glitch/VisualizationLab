import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df = df.groupby(['month'])['actual_max_temp'].max().reset_index()

data = [go.Scatter(x=df['month'], y=df['actual_max_temp'], mode='lines', name='actual_max_temp')]

layout = go.Layout(title='Actual Max Temperatures From 2014 to 2015', xaxis_title="Month", yaxis_title="Temperature")

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='linechart.html')

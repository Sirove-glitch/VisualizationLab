import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df1 = df.groupby(['month'])['actual_max_temp'].max().reset_index()

df2 = df.groupby(['month'])['actual_min_temp'].max().reset_index()

df3 = df.groupby(['month'])['actual_mean_temp'].max().reset_index()

trace1 = go.Scatter(x=df1['month'], y=df1['actual_max_temp'], mode='lines', name='Max')
trace2 = go.Scatter(x=df2['month'], y=df2['actual_min_temp'], mode='lines', name='Min')
trace3 = go.Scatter(x=df3['month'], y=df3['actual_mean_temp'], mode='lines', name='Mean')
data = [trace1, trace2, trace3]

layout = go.Layout(title='Max, Min, and Mean Temperatures From 2014 to 2015', xaxis_title="month", yaxis_title="Temperature")

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='multilinechart.html')
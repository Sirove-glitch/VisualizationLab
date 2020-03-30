import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df['Date'] = pd.to_datetime(df['Date'])

data = [go.Scatter(x=df['Date'], y=df['Confirmed'], mode='lines', name='Death')]

layout = go.Layout(title='Corona Virus Confirmed Cases From 2020-01-22 to 2020-03-17', xaxis_title="Date", yaxis_title="Number of cases")

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='linechart.html')
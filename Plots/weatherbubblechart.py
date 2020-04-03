import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

new_df = df.groupby(['month']).agg(
    {'average_min_temp': 'min', 'average_max_temp': 'max'}).reset_index()

data = [
    go.Scatter(x=new_df['month'],
               y=new_df['average_min_temp'],
               text=new_df['month'],
               mode='markers',
               marker=dict(size=new_df['average_min_temp'] / 50,color=new_df['average_min_temp'] / 50, showscale=True))
]

layout = go.Layout(title='Corona Virus Confirmed Cases', xaxis_title="Recovered Cases", yaxis_title="Unrecovered Cases", hovermode='closest')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='bubblechart.html')
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

new_df = df.groupby(['NOC']).agg(
    {'Total': 'sum', 'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()

new_df = new_df.sort_values(by=['Total'],
                            ascending=[False]).head(20).reset_index()

trace1 = go.Bar(x=new_df['NOC'], y=new_df['Bronze'], name='Bronze',
                marker={'color': '#CD7F32'})
trace2 = go.Bar(x=new_df['NOC'], y=new_df['Silver'], name='Silver',
               marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=new_df['NOC'], y=new_df['Gold'], name='Gold',
                marker={'color': '#FFD700'})
data = [trace1, trace2, trace3]

layout = go.Layout(title='Total Medals of Top 20 Countries in 2016 Rio Olympics', xaxis_title="Country", yaxis_title="Number of Medals", barmode='stack')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='stackbarchart.html')
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/CoronavirusTotal.csv')

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df['Unrecovered'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

df = df[(df['Country'] != 'China')]

new_df = df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()

new_df = new_df.sort_values(by=['Confirmed'],
                            ascending=[False]).head(20).reset_index()

trace1 = go.Bar(x=new_df['Country'], y=new_df['Unrecovered'], name='Unrecovered',
                marker={'color': '#CD7F32'})
trace2 = go.Bar(x=new_df['Country'], y=new_df['Recovered'], name='Recovered',
               marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=new_df['Country'], y=new_df['Deaths'], name='Deaths',
                marker={'color': '#FFD700'})
data = [trace1, trace2, trace3]

layout = go.Layout(title='Corona Virus Cases in the first 20 Country except China', xaxis_title="Country", yaxis_title="Number of cases", barmode='stack')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='stackbarchart.html')
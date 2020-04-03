import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

new_df = df.groupby(['NOC'])['Total'].sum().reset_index()

new_df = new_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()

data = [go.Bar(x=new_df['NOC'], y=new_df['Total'])]

# Preparing layout
layout = go.Layout(title='Total Medals of Olympic 2016 of 20 First Top Countries', xaxis_title="Country",
                   yaxis_title="Number of medals")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='barchart.html')

#%%
import plotly.graph_objects as go

import pandas as pd

#%%
df = pd.read_parquet("Analisis/datos_para_plotly")
df.head(3)
# df = df[df['Sold Year'] == 2010 ]

#%%
df['text'] = df['Town'] \
    + '<br>Sales: $' + (df['Sale Amount']).astype(str) \
    + '<br>Type: ' + df['Property Type']
limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 5000

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['Longitude'],
        lat = df_sub['Latitude'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['Sale Amount']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

fig.update_layout(
        title_text = 'Sales in 2020<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)'
        )
    )

fig.show()
# %%

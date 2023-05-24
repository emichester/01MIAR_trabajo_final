from app import app
from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from data_cleaning_utils import *
import plotly.figure_factory as ff


df= pd.read_parquet(r'data_frame.gzip')
df, df_sales_stats= clean_input_df(df)


app.layout = html.Div(children=[
    html.Div(children=[html.H1('Python para la IA')]),
    html.Hr(),

    dcc.Tabs([

            dcc.Tab(id= 'analysis-tab', label= ' Real State Exploratory Data Analysis', children= [
                html.Div([
                    html.Div(children=[
                        dcc.Dropdown(id='y_value_general', options=['Sale Amount', 'Sales Ratio', 'Assessed Value'],
                                    style= {'margin-left': '20px', 'margin-top': '20px'}),
                        dcc.Graph(id='graph-general')
                    ],
                    className='col-6', style= {'display': 'inline-block'}),
                    html.Div(children=[
                        dcc.Graph(id='graph-distribution')
                    ],
                    className='col-6', style= {'display': 'inline-block'}),
                ]),
                html.Hr(),
                html.Div(
                    children= [
                        html.Div(children= [
                                        dcc.Dropdown(id= '2dist-x', options= ['Sale Amount', 'Sales Ratio', 'Assessed Value'], style= {'width': '600px', 'margin-left': '20px'}),
                                        dcc.Dropdown(id= '2dist-y', options= ['Sale Amount', 'Sales Ratio', 'Assessed Value'], style= {'width': '600px', 'margin-left': '20px'}),
                                        ], style= {'display': 'flex'}),
                        html.Div(children= [dcc.Slider(id= 'range-slider', min=0, max= 10, value= 10)], className= 'row-4'), #style= {'width': '100px'}
                        dcc.Graph(id= '2d-distplot')
                    ]
                ),
                html.Hr(),
                html.Div(children= [
                    html.H5('Town analysis chart'),
                    html.Div(children=[
                        dcc.Dropdown(id= 'input_var_town', options= ['Sale Amount', 'Sales Ratio', 'Assessed Value'], style= {'width': '600px', 'margin-left': '20px'}),
                        dcc.Graph(id= 'town-graph')
                    ])
                ])

            ]),

            dcc.Tab(id= 'predictive-analysis-tab', label= 'Predictive analysis', children= [
                html.Div(children= [
                                    html.Div(children= [
                                        dcc.Input(id= 'Input-year', type= 'number', placeholder= 'Introduce Year', style= {'width': '200px', 'margin-left': '20px'}),
                                        dcc.Dropdown(id= 'Dropdown-town', options= df['Town'].drop_duplicates().to_list(), placeholder= 'Select Town', style= {'width': '200px', 'margin-left': '20px'}),
                                        dcc.Dropdown(id= 'Dropdown-street', options= df['Street'].drop_duplicates().to_list(), placeholder= 'Select Street', style= {'width': '200px', 'margin-left': '20px'}),
                                        dcc.Dropdown(id= 'Dropdown-property-type', options= df['Property Type'].drop_duplicates().to_list(), placeholder= 'Select Property Type', style= {'width': '200px', 'margin-left': '20px'}),
                                        dcc.Dropdown(id= 'Dropdown-residential-type', options= df['Residential Type'].drop_duplicates().to_list(), placeholder= 'Select Residential Type', style= {'width': '200px', 'margin-left': '20px'})
                                    ], style= {'display': 'flex', 'margin-top': '50px'}),
                                    html.Div(children= [
                                        html.Button(id= 'submit-pred-data', children= 'Submit data', style= {'width': '100px', 'height': '50px', 'margin-top': '20px', 'margin-left': '20px'})
                                    ])


                ])
            ])
            ])

    
])


@app.callback(Output('graph-general', 'figure'),
              Input('y_value_general', 'value'),
              )
def get_general_graph(y_value):
    if y_value is not None:
        df_fig= pd.DataFrame(df.groupby('year_and_month').mean()[y_value])
        fig= go.Figure(data= [go.Scatter(x= df_fig.index, y= df_fig[y_value], mode= 'markers+lines')])
        fig.update_layout(title= f'Mean monthly {y_value}', xaxis_title= 'Month', yaxis_title= y_value)
        return fig
    else:
        raise PreventUpdate

@app.callback(Output('graph-distribution', 'figure'),
              Input('y_value_general', 'value'),
              )
def get_hist_graph(y_value):
    if y_value is not None:
        df_stat= df[df[y_value] < np.percentile(df[y_value], 90)]
        fig= go.Figure(go.Histogram(x= df_stat[y_value], nbinsx= 50))
        fig.update_layout(title= f'Distribution of {y_value}', xaxis_title= y_value)
        return fig
    else:
        raise PreventUpdate

@app.callback(
            Output('2d-distplot', 'figure'),
            Input('2dist-x', 'value'),
            Input('2dist-y', 'value'),
            Input('range-slider', 'value')
              )
def get_2d_hist(x_in, y_in, range_filter):
    if all([_ is not None for _ in(x_in, y_in)]):
        range_filter= float(range_filter) if range_filter else float(0)
        df_2d= df.iloc[-2000:]
        print(range_filter)
        y_upper_lim, y_lower_lim, x_upper_lim, x_lower_lim=np.percentile(df_2d[y_in], 100-range_filter), np.percentile(df_2d[y_in], 0), np.percentile(df_2d[x_in], 100-range_filter), np.percentile(df_2d[x_in], 0)

        x, y= df_2d[x_in], df[y_in]
        fig = go.Figure(go.Histogram2dContour(
                x = x,
                y = y,
                colorscale = 'Jet',
                contours = dict(
                    showlabels = True,
                    labelfont = dict(
                        family = 'Raleway',
                        color = 'white'
                    )
                ),
                hoverlabel = dict(
                    bgcolor = 'white',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Raleway',
                        color = 'black'
                    )
                ),
                histfunc= 'avg'

        ))
        fig.update_layout(xaxis_title= x_in,
                          yaxis_title= y_in, title= '2D distribution plot',
                          xaxis= dict(range= [x_lower_lim, x_upper_lim]), yaxis= dict(range= [y_lower_lim, y_upper_lim])
                          )
        return fig
    else:
        raise PreventUpdate

@app.callback(
    Output('town-graph', 'figure'),
    Input('input_var_town', 'value')
)
def get_town_cart(input_var_town):
    if input_var_town:
        df_expensive_towns= df[['Town', 'Assessed Value', 'Sale Amount', 'Sales Ratio']].groupby('Town').mean().sort_values(by= input_var_town, ascending= False)
        df_expensive_towns= df_expensive_towns.iloc[:13].sort_values(by= input_var_town, ascending= False)
        fig = go.Figure([go.Bar(y= df_expensive_towns[input_var_town], x=list(df_expensive_towns.index))])
        return fig
    else:
        raise PreventUpdate
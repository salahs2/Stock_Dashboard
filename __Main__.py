# python3 -m venv venv
# . venv/bin/activate (Activate Virtual Environmetn)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

df = pd.read_csv('/Users/salah/Desktop/Programming/Python/Dash/stocks.csv')
label_name = {'SPY': 'S&P500', 'XAR': 'Aerospace & Defence','XBI': 'Biotech','XES': 'Oil & Gas','XHE': 'Health-Care Equipment','XHS': 'Health-Care Services','XITK': 'Innovative Technologies'}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], 
                            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}] #mobile layout
                )

'''
Layout
--------------------------------------------
'''
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Market Dashboard",
                        className = 'text-center mb-4'), #bootstrap styling
                        width = 12) #max cols = 12
                        
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id = 'my-dpdn', multi=False, value='SPY',
                        options=[{'label': label_name.get(str(x)), 'value' : x}
                            for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig', figure={})
        ], 
        width={'size': 5}),

        dbc.Col([
            dcc.Dropdown(id = 'my-dpdn2', multi=True, value=['SPY', 'XAR'],
                        options=[{'label': label_name.get(str(x)), 'value' : x}
                            for x in sorted(df['Symbols'].unique())]
                            ),
            dcc.Graph(id='line-fig2', figure={})
        ], 
        width={'size': 5, 'offset':2}),
        
        ]),

    # dbc.Row([
    #         dbc.Col([
    #         dcc.Checklist(id='my-checklist', value=['SPY', 'GOOGL', 'AMZN'],
    #                       options=[{'label':x, 'value':x}
    #                                for x in sorted(df['Symbols'].unique())],
    #                       labelClassName="mr-md-5"), #label spacing not working fix later
    #         dcc.Graph(id='my-hist', figure={}),
    #     ], width={'size':5}
    #     ),

    # ])
], fluid=True)

@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='Adj Close')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Adj Close', color='Symbols')
    return figln2


# Histogram
# @app.callback(
#     Output('my-hist', 'figure'),
#     Input('my-checklist', 'value')
# )
# def update_graph(stock_slctd):
#     dff = df[df['Symbols'].isin(stock_slctd)]
#     dff = dff[dff['Date']=='2020-12-03']
#     fighist = px.histogram(dff, x='Symbols', y='Close')
#     return fighist

if __name__ == '__main__':    
    app.run_server(debug=True, port=3000)

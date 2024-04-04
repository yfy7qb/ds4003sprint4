# Import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash,dash_table, dcc, html, Input, Output, callback
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py

# Import CSV
df = pd.read_csv('data.csv')

# Set up app and sever
app = Dash(__name__, external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# Set app layout
app.layout = html.Div([
    
    # Adding title
    html.Div(html.H1(
        children = 'Georgia Election Results: 2016 and 2020',
        style = {'display': 'flex', 'justifyContent': 'center'}
        )),

    # Adding description
    html.Div(html.P(children =
        'This interactive dashboard, when fully functional, will allow for comparisons between 2016 and 2020 election data, and House and Presidential results, in the state of Georgia.'
        )),

    html.Div(html.P(children=
            'Note: The 2016/2020 radio buttons are not yet functional, and are just there for design.'
        )),

    # Adding Radio Items for Year
    html.Div(dcc.RadioItems(
            id = 'yearradio',
            options = [2016, 2020],
            value =  2016,
            inline = True,
            className="four columns",
            style = {'display': 'flex', 'justifyContent': 'center'}
            )),

    # Adding Dropdown for District
    html.Div(dcc.Dropdown(
            id = 'districtdd',
            options = df['district'].unique(),
            value =  'statewide',
            multi = False,
            className="four columns"
            )),

    # Adding Radio Items for Race
    html.Div(dcc.RadioItems(
            id = 'preshouseradio',
            options=[
                {'label': 'President', 'value': 'pres'},
                {'label': 'House', 'value': 'house'}],
            value =  'pres',
            inline = True,
            className="four columns",
            style = {'display': 'flex', 'justifyContent': 'center'}
            )),

    # Add space
    html.Hr(),

    # Adding graph
    html.Div(dcc.Graph(
        id = 'votingtypechart',
        className = 'eight columns')),

    html.Div(dcc.Graph(
        id = 'pie',
        className = 'four columns'))
    ])

# Define chained callback
@app.callback(
    Output('districtdd', 'options'),
    Input('preshouseradio', 'value'))
def set_subcat_options(preshouseradio):
    # Filter the dataframe based on the selected category
    dfnew = df[df['race'] == preshouseradio]
    # Generate options for the subcategory dropdown
    return [{'label': i, 'value': i} for i in dfnew['district'].unique()]


# Define callback function for graphs
@callback(
    Output('votingtypechart', 'figure'),
    Output('pie', 'figure'),
    Input('yearradio', 'value'),
    Input('districtdd', 'value'),
    Input('preshouseradio', 'value')
)

# Define update function
def update_graph(yearradio, districtdd, preshouseradio):

    # Filter for data in given year
    dff = df[df['year'] == 2016]

    # Filter for race
    dff = dff[dff['race'] == preshouseradio]

    # Filter for districts in dropdown
    dff = dff[dff['district'] == districtdd]

    fig1 = px.histogram(
            dff[dff['mode'] != 'provisional'], # Filtered dataframe, no provisional votes
             x="party", # by party
             y="votes",
             color="party",
             facet_col="mode", # seperate by mode of voting
             histfunc = 'sum', # sum of votecount
             title = 'Results by Voting Type',
             color_discrete_map = {"republican": "red", "democratic": "blue", 'libertarian': 'yellow'}, # matching colors
             category_orders= {'mode': ['election day', 'absentee by mail', 'advance in person']}
             )
    
    fig2 = px.pie(
        dff,
        values = 'votes',
        names = 'candidate',
        title = 'Pie Chart of Results',
        color = 'party',
        color_discrete_map = {"republican": "red", "democratic": "blue", 'libertarian': 'yellow'} # matching colors
    )

    return fig1, fig2

# Run app
if __name__ == '__main__':
    app.run_server(debug = True)
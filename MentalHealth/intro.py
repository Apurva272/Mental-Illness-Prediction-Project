import pandas as pd 
import plotly.express as px # (version 4.7.0)
import plotly.graph_objects as graph_objects

import dash #(version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("dataMental.csv")
df = df.groupby(['Age', 'Gender'])[["Apparent Sadness (Representing despondency, gloom and despair, (more than just ordinary transient low spirits) reflected in-speech, facial expression, and posture. Rate by depth and inability to brighten up.)"]].mean()
df.reset_index(inplace=True)
print(df[:5])

app.layout = html.Div([
html.H1("Mental Health Awareness DIT University", style={'text-align': 'center'}),
dcc.Dropdown(id="slct_gender",
    options=[
        {"label": "male", "value": 1},
        {"label":"female", "value":2}

    ],
    multi=False,
    value=1,
    style={'width': "40%"}),

html.Div(id='output_container', children=[]),
html.Br(),

dcc.Graph(id='mental_health_map', figure={})
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='mental_health_map', component_property='figure')],
    [Input(component_id='slct_gender', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The gender chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Gender"] == option_slctd]
    dff = dff[dff["Affected by"] == "Apparent Sadness (Representing despondency, gloom and despair, (more than just ordinary transient low spirits) reflected in-speech, facial expression, and posture. Rate by depth and inability to brighten up.)"]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations='India',
        scope="asia",
        
        template='plotly_dark'
    )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)





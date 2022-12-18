from tabnanny import check
import numpy as np
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
# from skimage import io

df = pd.read_csv("inference_merged_data.csv", usecols=[
                 "id", "merchant_name", 'address', 'lat', 'lng', 'objects','product_name'])

df['objects'] = df.objects.apply(lambda x: str(x).split(','))

image_path = 'assets/logo.png'

html.Img(src=image_path)

header = dbc.Row(

    dbc.Col([
            html.H1("Product Location Identifier",
                    className='text-center  border rounded', style={'color': "white","backgroundColor":"#02033b"}),
            html.H1(
                "", className=' bg-light text-center mb-1 border rounded')
            ], width={'size': 12, 'offset': 0, 'order': 1}, style={"backgroungColor":"red"} ),style={"backgroungColor":"red"}
)


map_row = dbc.Row(
    [


        dbc.Col(
            [

                html.Br(),
                html.H6("Product Type"),
                dcc.Dropdown(["chips", "cake"], value="cake",
                               id='product'),

                html.Br(),
                html.H6("Select Brand"),
                dcc.Dropdown(placeholder="Select Brand", id='chips', multi=False),

                html.Br(),
                html.H6("Area"),
                dcc.Dropdown(["Mirpur", "Gulshan", "Banani", "Paltan"],
                               value="Mirpur", id='area'),

                html.Br(),
                html.H6("Map Type"),
                dcc.RadioItems(["open-street-map", "carto-positron",
                               "stamen-terrain"], value="open-street-map", id='mapbox',),

                html.Br(),
                html.Br(),
                html.Br(),


                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),
                #    html.Br(),


                html.Img(src=image_path, style={
                         "height": "100px", "width": "220px"}, className='"align-middle')


            ], width={'size': 2, 'offset': 0, 'order': 1}),

        dbc.Col(dcc.Graph(id='map', style={'height': "700px"}), width={
                'size': 10, 'offset': 0, 'order': 1})

                
    ], justify="center", align='center'
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


app.layout = dbc.Container([



    header,
    map_row




], fluid=True,
    style={"backgroundColor": "#e7f7ff", }
)

@app.callback(
    Output("chips", "options"),
    Input("product", "value"),
)

def brand(prod_type):
    if prod_type=='chips':
        return ['detos', 'kurkure', 'curl',
                              'alooz', 'sticks', 'ring',
                              'sun', 'potato_crackers', 'zeros',
                              'mr_twist', 'cheese_puff']
    if prod_type == 'cake':
        return ['dan_cake',"no_dan_cake"]


@app.callback(
    Output("map", "figure"),
    Input("chips", "value"),
    Input("mapbox", "value"),
    Input("product", "value"),


)
def map(chips, map_type,prod):
    def data_filter(data):
        return any(x in data for x in [chips])
    data = df[df.objects.apply(data_filter)]

    

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        name=f"all {prod}",
        lat=df['lat'],
        lon=df['lng'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=6,
            color='#ff9900',
            opacity=1
        ),
        text=df["id"],
        # hovertemplate='ID: {}',
        hoverinfo='text'
    ))

    fig.add_trace(go.Scattermapbox(

        lat=data['lat'],
        lon=data['lng'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=7,
            color='blue',
            opacity=0.7
        ),
        text=data["id"],
        hoverinfo='text',
        name=f"Selected {prod}",
    ))

    fig.update_layout(
        title='<b>Merchant Locations for Mirpur Area </b>',
        mapbox_style=map_type,
        autosize=True,
        hovermode='closest',
        margin={"r": 90, "t": 90, "l": 90, "b": 90},
        showlegend=True,
        mapbox=dict(
            bearing=0,
            center=dict(
                lat=23.80,
                lon=90.37
            ),
            pitch=0,
            zoom=12,
        ),
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=False, port=8050)

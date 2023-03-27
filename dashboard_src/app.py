import os
import json
import dash
from dash import dcc
from dash import html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from mni import create_fig

import time
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# from transformers import AutoModelWithLMHead, AutoTokenizer
# import torch
import plotly.graph_objects as go

from gpt_index import GPTSimpleVectorIndex

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = "Brain Chat"

server = app.server

axis_template = {
    "showbackground": True,
    "backgroundcolor": "#141414",
    "gridcolor": "rgb(255, 255, 255)",
    "zerolinecolor": "rgb(255, 255, 255)",
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    "plot_bgcolor": "#141414",
    "paper_bgcolor": "#141414",
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectratio": {"x": 1.8, "y": 1.8, "z": 1},
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

# API Key
os.environ['OPENAI_API_KEY'] = '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'

index = GPTSimpleVectorIndex.load_from_disk('index.json')
# Model response
def chatbot(input_text, index=index):
    response = index.query(input_text,
                           response_mode='compact')
    return response.response


# Textbox
def textbox(text, box="other"):
    style = {
        "max-width": "55%",
        "width": "max-content",
        "padding": "10px",
        "border-radius": "25px",
    }

    if box == "self":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        color = "primary"
        inverse = True

    elif box == "other":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        color = "light"
        inverse = False

    else:
        raise ValueError("Incorrect option for `box`.")

    return dbc.Card(text, style=style, body=True, color=color, inverse=inverse)

# Conversation 
conversation = html.Div(
    style={
        "width": "80%",
        "max-width": "800px",
        "height": "70vh",
        "margin": "auto",
        "overflow-y": "auto",
    },
    id="display-conversation",
)

# Text Controls
controls = dbc.InputGroup(
    style={"width": "80%", "max-width": "800px", "margin": "auto"},
    children=[
        dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text"),
        dbc.Button("Submit", id="submit", className="me-1"),
    ],
)

# Create Figure
files = ['10156.obj',
'10653.obj',
'10648.obj']

def first_fig(files):
    fig = go.Figure()
    for file in files:
        data = create_fig(file)
        fig.add_trace(data)
    go.Figure.update_layout(fig, plot_layout)
    # fig.update_layout(width = "50%")
    return fig


app.layout = html.Div([
    # First section -- title, info
    html.H1('Brain Chat',
            style={'margin': '30px', 'margin-bottom': 10}),
    html.Div([
        html.P('Welcome! Brain Chat is a friendly chat service. It will highlight areas of the brain that may be affected based on the symptoms you provide.',
               style={'fontSize': 20}),
        html.P("Chat with the bot on the right!.",
               style={'fontSize': 20, 'margin-top': -10})],
             style={'margin-left': 50,
                    # 'margin-top': 25
                    }
             ),
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    
                        html.P( "Drag the black corners of the graph to rotate."),
                        dcc.Graph(
                                            id="brain-graph",
                                            figure = first_fig(files),
                                            # figure={
                                            #     "data": create_mesh_data("human_atlas"),
                                            #     "layout": plot_layout,
                                            # },
                                            config={"editable": True, "scrollZoom": False},
                                            # width=500
                                            style={'height': '75vh'}
                                    )
                    
                ], width = {'size': 8}), 
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Chat',
                                    style={'textAlign': 'center'}),
                        dbc.CardBody([
                                    conversation,
                                    controls])
                    
                                    
                    ])
                ], width = {'size': 4})
            ])
        ])
    ])
]
)

# @app.callback(
#     [Output("store-conversation", "data"), Output("user-input", "value")],
#     [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
#     [State("user-input", "value"), State("store-conversation", "data")],
# )
# def run_chatbot(n_clicks, n_submit, user_input, chat_history):
#     if n_clicks == 0:
#         return "", ""

#     if user_input is None or user_input == "":
#         return chat_history, ""

#     response = chatbot(user_input)
#     chat_history = chat_history + "help" + user_input + response

    # return chat_history, ""

@app.callback(
    [Output("display-conversation", "children"), Output('user-input', 'value')], 
    [Input('submit', 'n_clicks')], 
    [State("user-input", "value")]
)
def update_display(clicks, user_input):
    if clicks is not None:
        response = chatbot(user_input)
        return [textbox(user_input, box="self"), textbox(response, box="other")], ""
    else:
        return "", ""

# @app.callback(
#     [Output("store-conversation", "data"), Output("user-input", "value")],
#     [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
#     [State("user-input", "value"), State("store-conversation", "data")],
# )
# def run_chatbot(n_clicks, n_submit, user_input, chat_history):
#     if n_clicks == 0:
#         return "", ""

#     if user_input is None or user_input == "":
#         return chat_history, ""

#     response = chatbot(user_input)
#     chat_history = chat_history + "help" + user_input + response

#     return chat_history, ""


@app.callback(
    Output("brain-graph", "figure"),
    [Input("display-conversation", "children"), Input("brain-graph", "figure")]
)
def update_figure(children, figure):
    print(f"history2: {children}")
    return figure




if __name__ == "__main__":
    app.run_server(debug=True)
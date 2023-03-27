import os
import json
import dash
from dash import dcc
from dash import html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from mni import create_fig, fname_to_brain_part_mapper
import time
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from glob import glob
import pandas as pd
import openai

from gpt_index import GPTSimpleVectorIndex

credentials_file = open("../credentials.json")
auth_file = json.load(credentials_file)
auth_key = auth_file['auth']['key']

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
    "zerolinecolor": "rgb(255, 255, 255)"
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
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
# Declaring global variables

files_list_to_read = []
fig = go.Figure()
brain_df = pd.read_csv('../data/naming_brain.csv')

# Creating the Brain figure (Fore Brain, Mid-Brain and Hind Brain)
files = ['10156.obj',
         '10653.obj',
         '10648.obj']

for file in files:
    data = create_fig(file)
    fig.add_trace(data)

figure = go.Figure.update_layout(fig, plot_layout)

# API Key
os.environ['OPENAI_API_KEY'] = auth_key

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
        dbc.Textarea(id="user-input", placeholder="Write to the chatbot...", style={"padding": 5}),
        dbc.Button("Submit", id="submit", className="me-1", style={"padding": 5}),
    ],
)

# add_fig_button = html.Div(
#     [
#         dbc.Label("Add an output"),
#         dbc.RadioItems(
#             options=[
#                 {"label": "Dont add", "value": 1},
#                 {"label": "Add", "value": 2},
#             ],
#             value=1,
#             id="add-fig-input",
#         ),
#     ]
# )

render_button = html.Div(
    [
        dbc.Button(
            "Visualize This", id="render-brain-image", n_clicks=0
        )
    ]
)

app.layout = html.Div([
    # First section -- title, info
    html.H1('Brain Chat - A Brain Diagnostic Assistant Tool',
            style={'margin': '30px', 'margin-bottom': 10}),
    html.Div([
        html.P(
            'Welcome! Brain Chat is a friendly chat service. It will highlight areas of the brain that may be '
            'affected based on the symptoms you provide.',
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
                    dcc.Graph(
                        id="brain-graph",
                        figure=figure,
                        # figure={
                        #     "data": create_mesh_data("human_atlas"),
                        #     "layout": plot_layout,
                        # },
                        config={"editable": True},
                        # width=500
                        style={'height': '75vh'}
                    )

                ], width={'size': 8}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Chat',
                                       style={'textAlign': 'center'}),
                        dbc.CardBody([
                            conversation,
                            controls])

                    ], style={'height': '75vh'}
)
                ], width={'size': 4},
                    style={'height': '75vh'}
                )
            ]),
            dbc.Row(
                render_button,
                style={
                    'padding': '15px',
                    'margin': '20px',
                }
            )
        ])
    ])
]
)


@app.callback(
    [Output("display-conversation", "children"), Output('user-input', 'value')],
    [Input('submit', 'n_clicks')],
    [State("user-input", "value")]
)
def update_display(clicks, user_input):
    if clicks is not None:
        response = chatbot(user_input)
        global brain_df
        global files_list_to_read

        brain_list = brain_df['name'].to_list()
        brain_list = "[" + ', '.join(brain_list[i] for i in range(len(brain_list))) + "]"

        context = "Remember this list: " + brain_list
        query = f"""
        Give an answer from the list elements

        Question: The absence of right face, arm, and leg movements in response to pain could be explained by a lesion affecting the entire left cerebral cortex, or a left hemisphere lesion involving a large region of cortex plus all subcortical pathways.
        Answer: cerebral cortex
        Question: The left eye blurriness and right arm weakness could be caused by a lesion in the right occipital lobe and right motor cortex, respectively. This lesion would affect the corticobulbar and corticospinal pathways originating in the right motor cortex.
        Answer: cerebral cortex, occipital lobe
        Question: The localization for right arm weakness and finger flexion in the brain is the left precentral gyrus.
        Answer: precentral gyrus
        Question: This could be a lesion in the right occipital lobe, which is responsible for vision and eye movement.
        Answer: occipital lobe
        Question: {response}
        Answer:"""
        # Generate a response using GPT-3
        brain_part = openai.Completion.create(
            engine="davinci",
            prompt=context + " " + query,
            temperature=0.5,
            n=1,
            stop=None,
            timeout=15,
        )

        # Print the generated response
        print(brain_part.choices[0].text.strip().split('\n'))
        outputs = brain_part.choices[0].text.strip().split('\n')[:-1]
        try:
            print(outputs)
            for output in outputs[0].split(', '):
                id = brain_df.query("name == @output")['id'].values[0]
                id = str(id) + ".obj"
                print(id)
                files_list_to_read.append(id)
        except Exception as e:
            print(e)

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
    Input("render-brain-image", "n_clicks")
)
def update_figure(n_clicks):
    global figure
    global fig
    if n_clicks == 0:
        return figure
    else:
        temp_fig = fig
        global files_list_to_read
        print(files_list_to_read)
        for fname in files_list_to_read:
            data = create_fig(fname, cmap=True)
            temp_fig.add_trace(data)
            part_name = fname_to_brain_part_mapper(fname, brain_df)
            print("part name is {}".format(part_name))
            temp_fig.update_traces(name=part_name)
    temp_figure = go.Figure.update_layout(temp_fig, plot_layout)
    files_list_to_read = []

    return temp_figure


if __name__ == "__main__":
    app.run_server()

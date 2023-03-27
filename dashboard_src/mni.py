import pathlib
import numpy as np
import plotly.graph_objects as go
import os
import pandas as pd

folder_path = "../meshes"

# default_colorscale = [
#     [0, "rgb(12,51,131)"],
#     [0.25, "rgb(10,136,186)"],
#     [0.5, "rgb(242,211,56)"],
#     [0.75, "rgb(242,143,56)"],
#     [1, "rgb(217,30,30)"],
# ]
brain_df = pd.read_csv("../data/naming_brain.csv")


def fname_to_brain_part_mapper(fname, brain_df):
    fname = int(fname.split('.')[0])
    part_name = brain_df.query("id == @fname")['name'].values[0]

    return part_name


def read_mniobj(fpath):
    fpath = os.path.join(folder_path, fpath)
    with open(fpath) as fp:

        matrix_vertices = []
        matrix_faces = []
        for i, line in enumerate(fp):
            alpha = line.split()[0]

            if i == 0:
                continue
            elif alpha == 'v':
                matrix_vertices.append(list(map(float, line.split()[1:])))
            elif alpha == 'f':
                matrix_faces.append(list(map(int, line.split()[1:])))
            else:
                continue
    return np.array(matrix_vertices), np.array(matrix_faces)


def plotly_triangular_mesh(
        vertices,
        faces,
        intensities=None,
        colorscale="Grey",
        flatshading=False,
        showscale=False,
        plot_edges=False,
):
    x, y, z = vertices.T
    I, J, K = faces.T

    if intensities is None:
        intensities = z

    mesh = {
        "type": "mesh3d",
        "x": x,
        "y": y,
        "z": z,
        "colorscale": colorscale,
        "intensity": intensities,
        "flatshading": flatshading,
        "i": I,
        "j": J,
        "k": K,
        "name": "",
        "showscale": showscale,
        "lighting": {
            "ambient": 0.18,
            "diffuse": 1,
            "fresnel": 0.1,
            "specular": 1,
            "roughness": 0.1,
            "facenormalsepsilon": 1e-6,
            "vertexnormalsepsilon": 1e-12,
        },
        "lightposition": {"x": 100, "y": 200, "z": 0},
    }

    if showscale:
        mesh["colorbar"] = {"thickness": 20, "ticklen": 4, "len": 0.75}

    if plot_edges is False:
        return [mesh]

    lines = create_plot_edges_lines(vertices, faces)
    return [mesh, lines]


def create_plot_edges_lines(vertices, faces):
    tri_vertices = vertices[faces]
    Xe = []
    Ye = []
    Ze = []
    for T in tri_vertices:
        Xe += [T[k % 3][0] for k in range(4)] + [None]
        Ye += [T[k % 3][1] for k in range(4)] + [None]
        Ze += [T[k % 3][2] for k in range(4)] + [None]


def create_fig(fname, cmap=False):
    vertices, faces = read_mniobj(fname)
    brain_part = fname_to_brain_part_mapper(fname, brain_df)

    data = []

    outer_mesh = plotly_triangular_mesh(vertices, faces)[0]

    outer_mesh['hovertext'] = brain_part
    if cmap:
        outer_mesh["colorscale"] = "Reds"
        outer_mesh["opacity"] = 0.9

    else:
        outer_mesh['colorscale'] = "Greys"
        outer_mesh["opacity"] = 0.1

    data.append(outer_mesh)
    return data[0]
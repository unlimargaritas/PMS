from datetime import date
from sre_parse import State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

# FORM TO CREATE NEW ACCOUNTS (page 10 in mock)
# ONLY ADMIN HAS ACCESS TO

layout = html.Div(
    [
        html.H2("Account Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Employee Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_id", placeholder="Enter Officer ID"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_username", placeholder="Enter Username"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("First Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_firstname", placeholder="Enter First Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_middlename", placeholder="Enter Middle Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Last Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_lastname", placeholder="Enter Last Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Email", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_emailadd", placeholder="Enter email address"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employee_pw", placeholder="Enter password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Role:", width=2),
                dbc.RadioItems(
                    options=[
                        {"label": "Admin", "value": 1},
                        {"label": "Faculty", "value": 2},
                        {"label": "Department Head", "value": 3},
                    ],
                    value=1,
                    id="employee_role",
                    inline=True,
                ),
            ]
        ),

        html.Hr(),
        dbc.Button('Submit', color="secondary", id='account_submitbtn', n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader("New Account Created"),
                dbc.ModalBody("tempmessage", id='account_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Done", id="account_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="account_modal",
            is_open=False
        ),
    ],
)

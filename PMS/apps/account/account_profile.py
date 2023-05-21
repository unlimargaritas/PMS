from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
from dash.dependencies import Input, Output, State
from apps import dbconnect as db

from app import app

# LANDING PAGE TO 'ACCOUNT MODULE' (page 9 in mock)
# EDIT BUTTON FOR PASSWORD ONLY?

layout = html.Div(
    [
        html.H2("Account"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Hello!"), id="current_account_name"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            dbc.Label("Username", width=2),
                            dbc.Col(
                                html.P(
                                    "", id="current_account_username", width=6
                                ),
                            ),
                        ),
                        dbc.Row(
                            dbc.Label("Role: ", width=2),
                            dbc.Col(
                                html.P("", id="current_account_role", width=6,
                                ),
                            ),
                        ),
                        dbc.Row(
                            dbc.Label("Password: ", width=2),
                            dbc.Col(
                                html.P("", id="current_account_pw", width=6,
                                ),
                            ),
                        ),
                        dbc.Button("Update Password", color="Secondary", id="current_account_updatepw", n_clicks=0),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Update Password"),
                                dbc.ModalBody[
                                    dbc.Row(
                                        dbc.Label("New Password: ", width=2),
                                        dbc.Input(
                                            type="text", id="current_account_new_pw", placeholder="Enter new password"
                                        ),
                                        width=6,
                                    ),
                                    dbc.Row(
                                        dbc.Label("Confirm New Password: ", width=2),
                                        dbc.Input(
                                            type="text", id="current_account_confirm_pw", placeholder="Retype new password"
                                        ),
                                        width=6,
                                    )

                                ],
                                dbc.ModalFooter(
                                    dbc.Button(
                                        " ", id="account_closebtn", className="ms-auto", n_clicks=0
                                    )
                                ),
                            ],
                            id="account_modal",
                            is_open=False
                        ),
                    ]
                ),

            ]
        )
    ]
)

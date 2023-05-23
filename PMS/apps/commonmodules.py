from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

navlink_style = {
    'color': '#fff',
    'margin-right': '1em'
}
navbar = dbc.Navbar(
    [
        html.A(
            dbc.NavbarBrand("DIEOR PMS", className="ml-2", 
            style={'margin-right': '2em','margin-left': '1em', 'font-size':'3em'}),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Faculty", href="/faculty", style=navlink_style),
        dbc.NavLink("Accountabilities", href="/props", style=navlink_style),
        dbc.NavLink("Login", href="/login", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style),
    ],
    dark=True,
    color='blue'
)


    

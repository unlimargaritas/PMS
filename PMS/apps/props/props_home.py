from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
from dash.dependencies import Input, Output, State
from apps import dbconnect as db

from app import app

layout = html.Div(
    [
        html.H2("Accountabilities"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Property Records")),
                dbc.CardBody(
                    [
                        dbc.Button("Add Property", color="primary", href = '/props/props_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Property",style={'fontweight':'bold'}),
                                html.Hr(),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Property", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='prop_name_filter',
                                                placeholder='Enter Property Name'
                                            ),
                                            width=6,
                                        ),
                                    ],
                                className='mb-3',
                                ),
                                html.Div(
                                    "This will contain the table for property records",
                                    id="prop_proplist"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
@app.callback(
    [
        Output('property_propertylist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('prop_name_filter', 'value'),
    ]
 )
def updatepropertylist(pathname, searchterm):
    if pathname == '/properties':
        sql = """select prop_name, prop_desc, prop_purch_amt, prop_qty, prop_total_purch_amt, prop_purch_date, prop_stat, prop_ret_date,
            from properties p 
            where not prop_delete_ind
        """
        val = []
        colnames = ['Name', 'Description', 'Purchase Amount', 'Quantity', 'Total Purchase Amount', 'Purchase Date', 'Status', 'Return Date']
        if searchterm:
            sql += "AND prop_name ILIKE %s"
            val += [f"%{searchterm}%"]
        
        properties = db.querydatafromdatabase(sql, val, colnames)
        if properties.shape[0]:
            buttons = []
            for propid in properties['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f"/props/props_profile?mode=edit&id={propid}",
                                    size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            properties['Edit/Delete Record'] = buttons

            properties.drop('ID', axis=1, inplace=True)

            table = dbc.Table.from_dataframe(properties, striped = True, bordered = True, hover = True, size = 'sm')
            return [table]

        else:
            return ["There are no records that match the search term."]
    
    else:
        raise PreventUpdate
                            
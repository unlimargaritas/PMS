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

layout = html.Div(
    [ 
        html.Div(
            [
            dcc.Store(id='propprof_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Property Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Property ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_id", placeholder="Enter Property ID"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_name", placeholder="Enter name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),        
        dbc.Row(
            [
                dbc.Label("Description", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_desc", placeholder="Enter description"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Quantity", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_qty", placeholder="Enter quantity"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Date Acquired", width=2),
                dbc.Col(     
                    html.Div(
                        dcc.DatePickerSingle(
                            id='propprof_purch_date',
                        ),
                        className="dash-bootstrap"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Quantity Cost", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_purch_amt", placeholder="Enter quantity cost per unit"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),   
        dbc.Row(
            [
                dbc.Label("Total Cost", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_total_purch_amt", placeholder="Enter total cost"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),   
        dbc.Row(
            [
                dbc.Label("Officer ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="employeeprof_id", placeholder="Enter Officer ID that logged this"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),   
        dbc.Row(
            [
                dbc.Label("Status", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_stat", placeholder="Enter Officer ID that logged this"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),   
        dbc.Row(
            [
                dbc.Label("Remarks", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="propprof_remarks", placeholder="Remarks"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),   
        html.Div(
                dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='propprof_removerecord',
                            options=[
                                {
                                'label': "Mark for Deletion",
                                'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id = 'propprof_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color="success", id='propprof_submitbtn', n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader("Saving Progress"),
                dbc.ModalBody("tempmessage", id='propprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="propprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="propprof_modal",
            is_open=False
        ),
    ],
)


@app.callback(
    [
        Output('propprof_toload', 'data'),
        Output('propprof_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def propprof_submitprocess(pathname, search):
    if pathname == '/props/props_profile':
        sql = """
        """
    
        parsed = urlparse (search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0

        removerecord_div = None if to_load else {'display': 'none'}
    else:
        raise PreventUpdate
    
    return [to_load, removerecord_div]

@app.callback(
    [
        Output('propprof_modal', 'is_open'),
        Output('propprof_feedback_message','children'),
        Output('propprof_closebtn','href')
    ],
    [
        Input('propprof_submitbtn', 'n_clicks'),
        Input('propprof_closebtn','n_clicks')
    ],
    [
        State('propprof_name', 'value'),
        State('propprof_desc', 'value'),
        State('propprof_qty', 'value'),
        State('propprof_unit', 'value'),
        State('propprof_purch_date', 'date'),
        State('propprof_purch_amt', 'value'),
        State('propprof_total_purch_amt', 'value'),
        State('employeeprof_id', 'value'),
        State('propprof_stat', 'value'),
        State('propprof_remarks', 'value'),
        State('url', 'search'),
        State('propprof_removerecord', 'value')
    ]
)

def propprof_submitprocess(submitbtn, closebtn,
                                name, desc, qty, unit, purch_date, purch_amt, total_purch_amt, employee_id, stat,remarks,
                                search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
        if eventid == "propprof_submitbtn" and submitbtn:
            openmodal = True
            inputs = [
                name,
                desc,
                qty,
                unit,
                purch_date,
                purch_amt,
                total_purch_amt,
                employee_id,
                stat,
                remarks
            ]
            if not all(inputs):
                feedbackmessage = "Please supply all inputs."
            elif len(name) > 256:
                feedbackmessage = "Property name is too long (length=256)."
            else:
                parsed = urlparse(search)
                mode = parse_qs(parsed.query)['mode'][0]
                if mode == 'add':
                    sqlcode = """ INSERT INTO properties(
                        prop_name,
                        prop_desc,
                        prop_qty,
                        prop_unit,
                        prop_purch_date,
                        prop_purch_amt,
                        prop_total_purch_amt,
                        employee_id,
                        prop_stat,
                        prop_remarks,
                        prop_delete_ind
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [name, desc, qty, unit, purch_date, purch_amt, total_purch_amt, employee_id, stat, remarks, False]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "prop has been saved."
                    okay_href = '/props'

                elif mode == 'edit':
                    parsed = urlparse(search)
                    propid = parse_qs(parsed.query)['id'][0]
                    sqlcode = """UPDATE properties
                    SET
                        prop_name = %s,
                        prop_desc = %s,
                        prop_qty = %s,
                        prop_unit = %s,
                        prop_purch_date = %s,
                        prop_purch_amt = %s,
                        prop_total_purch_amt = %s,
                        employee_id = %s,
                        prop_stat = %s,
                        prop_remarks = %s,
                    WHERE
                        prop_id = %s
                    """

                    to_delete = bool(removerecord)

                    values = [name, desc, qty, unit, purch_date, purch_amt, total_purch_amt, employee_id, stat, remarks, to_delete, propid]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "prop has been updated."
                    okay_href = '/props'


                else:
                    raise PreventUpdate

        elif eventid == 'propprof_closebtn' and closebtn:
            pass

        else:
            raise PreventUpdate

        return [openmodal, feedbackmessage, okay_href]

@app.callback(
    [
        Output('propprof_name', 'value'),
        Output('propprof_desc', 'value'),
        Output('propprof_qty', 'value'),
        Output('propprof_unit', 'value'),
        Output('propprof_purch_date', 'date'),
        Output('propprof_purch_amt', 'value'),
        Output('propprof_total_purch_amt', 'value'),
        Output('employeeprof_id','value'),
        Output('propprof_stat', 'value'),
        Output('propprof_remarks', 'value'),
    ],
    [
        Input('propprof_toload', 'modified_timestamp')
    ],
    [
        State('propprof_toload', 'data'),
        State('url', 'search')
    ]
)

def loadpropdetails(timestamp, to_load, search):
    if to_load == 1:
        sql = """prop_name, prop_desc, prop_qty, prop_unit, prop_purch_date, prop_purch_amt, prop_total_purch_amt, employee_id, prop_stat, prop_remarks
        FROM properties
        WHERE prop_id = %s
        """

        parsed = urlparse(search)
        propid = parse_qs(parsed.query)['id'][0]

        val = [propid]
        colnames = ['name', 'desc', 'qty', 'unit', 'purch_date', 'purch_amt', 'total_purch_amt', 'employee_id','stat', 'remarks']

        df = db.querydatafromdatabase(sql, val, colnames)

        name = df['name'][0]
        desc = df['desc'][0]
        qty = df['qty'][0]
        unit = df['unit'][0]
        purch_date = df['purch_date'][0]
        purch_amt = df['purch_amt'][0]
        total_purch_amt = df['total_purch_amt'][0]
        employee_id = df['employee_id'][0]
        stat = df['stat'][0]
        remarks = df['remarks'][0]

        return [name, desc, qty, unit, purch_date, purch_amt, total_purch_amt, employee_id, stat, remarks]

    else:
        raise PreventUpdate
                            

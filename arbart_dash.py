import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State




app = dash.Dash(__name__)

server = app.server

app.layout = dbc.Container([
    html.H1('Arb finder - Bart'),
    html.H3('View Golf Matchups between BT and BM'),
    dbc.Button('Refresh', id='refresh-match-table'),
    dbc.Spinner(html.Div(id='match_table_show')),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output('match_table_show','children'),
    [Input('refresh-match-table','n_clicks'),
    Input('interval-component', 'n_intervals'),
     ])
def show_matches(x, y):
    df_matchups = pd.read_csv(r'https://raw.githubusercontent.com/sardarnb/df_arbart/main/df_arbart.csv')
    df = df_matchups[['match_time_bm','match_time_bto', 'away_player', 'home_player', 'away_decimal_odds_bm', 'home_decimal_odds_bm',
             'away_decimal_odds_bto', 'home_decimal_odds_bto', 'best_away','best_book_away', 'best_home','best_book_home', 'cum_prob',
             'log_time']]
    df.log_time = pd.to_datetime(df.log_time)
    df = df.drop_duplicates()
    # df.loc[df.log_time == df.log_time.max()]
    data = df.loc[df.log_time == df.log_time.max()].to_dict('records'),

    m_table = dt.DataTable(
        id='match_table',
        columns=[{'name': 'match_time_bm', 'id': 'match_time_bm'},
                 {'name': 'away_player', 'id': 'away_player'},
                 {'name': 'home_player', 'id': 'home_player'},
                 {'name': 'away_decimal_odds_bm', 'id': 'away_decimal_odds_bm'},
                 {'name': 'home_decimal_odds_bm', 'id': 'home_decimal_odds_bm'},
                 {'name': 'match_time_bto', 'id': 'match_time_bto'},
                 {'name': 'away_decimal_odds_bto', 'id': 'away_decimal_odds_bto'},
                 {'name': 'home_decimal_odds_bto', 'id': 'home_decimal_odds_bto'},
                 {'name': 'best_away', 'id': 'best_away'},
                 {'name':'best_book_away', 'id':'best_book_away'},
                 {'name': 'best_home', 'id': 'best_home'},
                 {'name': 'best_book_home', 'id': 'best_book_home'},
                 {'name': 'cum_prob', 'id': 'cum_prob'},
                 {'name': 'log_time', 'id': 'log_time'},
                 ],
        data=data[0],
        # row_selectable='single',
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['away_player', 'home_player']
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0
        },
        filter_action="native",
    )

    return m_table


if __name__ == '__main__':
    app.run_server(debug=True)

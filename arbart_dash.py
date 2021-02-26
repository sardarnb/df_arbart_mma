import dash
import dash_table
import pandas as pd
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
    dt.DataTable(
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
                 {'name': 'best_home', 'id': 'best_home'},
                 {'name': 'cum_prob', 'id': 'cum_prob'},
                 {'name': 'log_time', 'id': 'log_time'},
                 # {'name': 'Operator', 'id': 'operator'},
                 # {'name': 'Country', 'id': 'country'},
                 # {'name': 'Well Name', 'id': 'well_nm'}
                 ],
        # data=[],
        row_selectable='single',
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
])


@app.callback(
    Output('match_table','data'),
    [Input('refresh-match-table','n_clicks'),
     ])
def show_matches(x):
    df = pd.read_csv('https://raw.githubusercontent.com/sardarnb/df_arbart/main/dff_bart.csv')
    df = df[['match_time_bm', 'away_player', 'home_player', 'away_decimal_odds_bm', 'home_decimal_odds_bm',
             'match_time_bto', 'away_decimal_odds_bto', 'home_decimal_odds_bto', 'best_away', 'best_home', 'cum_prob',
             'log_time']]
    df.log_time = pd.to_datetime(df.log_time)
    df.loc[df.log_time == df.log_time.max()]
    data = df.tail(10).to_dict('records'),
    #
    # users = []
    #
    # for result in results:
    #     users.append({
    #         'id' : result[0],
    #         'username' : result[1],
    #         'email' : result[2],
    #         'admin' : str(result[3]),
    #         'operator': result[4],
    #         'country': result[5],
    #         'well_nm': result[6],
    #
    #     })

    # match_table = dash_table.DataTable(
    #     id='table',
    #     columns=[{"name": i, "id": i} for i in df.columns],
    #     data=show_matches(),
    #     row_selectable='single',
    #     style_data={
    #         'whiteSpace': 'normal',
    #         'height': 'auto',
    #     },
    #     style_cell={
    #         'overflow': 'hidden',
    #         'textOverflow': 'ellipsis',
    #         'maxWidth': 0
    #     },
    #     filter_action="native",
    # )

    return data[0]


if __name__ == '__main__':
    app.run_server(debug=False)

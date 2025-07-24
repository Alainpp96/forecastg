import pandas as pd
import dash
from dash import html, dcc
from dash.dash_table import DataTable
import dash.dash_table.Format as Format

# Carica Excel
df = pd.read_excel("need_to_buy.xlsx")

# Formattazione numerica
format_2_dec = Format.Format(precision=2, scheme='f')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Tabella Need to Buy", style={"textAlign": "center", "marginBottom": "20px"}),

    DataTable(
        data=df.round(2).to_dict('records'),
        columns=[
            {
                "name": col,
                "id": col,
                "type": "numeric",
                "format": format_2_dec
            } if df[col].dtype.kind in "fc" else {"name": col, "id": col}
            for col in df.columns
        ],
        page_size=15,
        style_table={'overflowX': 'auto', 'maxWidth': '95%', 'margin': 'auto'},
        style_cell={
            'textAlign': 'center',
            'padding': '8px',
            'fontFamily': 'Arial',
            'fontSize': '14px',
        },
        style_header={
            'backgroundColor': '#f2f2f2',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'need_to_buy_MW'},
                'backgroundColor': '#ffdddd',
                'color': '#990000',
                'fontWeight': 'bold',
            },
        ],
    )
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)

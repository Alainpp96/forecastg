import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dash_table import DataTable
import dash.dash_table.Format as Format

# Carica Excel
df = pd.read_excel("need_to_buy.xlsx")

# Assicuriamoci che 'Giorno' sia in formato datetime
if "Giorno" in df.columns:
    df["Giorno"] = pd.to_datetime(df["Giorno"])

# Ordina il dataframe per 'Giorno'
df = df.sort_values(by="Giorno") if "Giorno" in df.columns else df

# Per la tabella, formattiamo la colonna 'Giorno' come stringa gg-mm-aaaa
if "Giorno" in df.columns:
    df["Giorno_str"] = df["Giorno"].dt.strftime("%d-%m-%Y")

# Colore barre e condizione su 'need_to_buy_MW'
if "need_to_buy_MW" in df.columns:
    df["colore_barra"] = df["need_to_buy_MW"].apply(lambda x: "#990000" if x >= 0 else "#228B22")

# Crea grafico con asse x 'Giorno'
fig = None
if "need_to_buy_MW" in df.columns and "Giorno" in df.columns:
    fig = px.bar(
        df,
        x="Giorno",
        y="need_to_buy_MW",
        color="colore_barra",
        color_discrete_map="identity",
        title="Andamento Need to Buy (MW)",
        labels={"need_to_buy_MW": "Need to Buy (MW)", "Giorno": "Giorno"},
        template="simple_white",
        height=400,
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(
        tickformat="%d-%m-%Y",
        tickangle=45,
        tickmode="auto",
        nticks=20,
    )

# Formattazione numerica per colonne numeriche
format_2_dec = Format.Format(precision=2, scheme="f")

# Condizioni colore nella tabella per 'need_to_buy_MW'
style_data_conditional = []
if "need_to_buy_MW" in df.columns:
    style_data_conditional = [
        {
            "if": {"filter_query": "{need_to_buy_MW} < 0", "column_id": "need_to_buy_MW"},
            "backgroundColor": "#d4fcd4",
            "color": "#006400",
            "fontWeight": "bold",
        },
        {
            "if": {"filter_query": "{need_to_buy_MW} >= 0", "column_id": "need_to_buy_MW"},
            "backgroundColor": "#ffdddd",
            "color": "#990000",
            "fontWeight": "bold",
        },
    ]

# Costruisci le colonne mettendo prima 'Giorno_str' come "Giorno"
columns = []

if "Giorno_str" in df.columns:
    columns.append({"name": "Giorno", "id": "Giorno_str"})

for col in df.columns:
    if col in ["colore_barra", "Giorno", "Giorno_str"]:
        continue  # escludi colonne tecniche e quella già aggiunta
    elif df[col].dtype.kind in "fc":
        columns.append({"name": col, "id": col, "type": "numeric", "format": format_2_dec})
    else:
        columns.append({"name": col, "id": col})

# App Dash
app = Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "#f9f9f9", "fontFamily": "Arial, sans-serif", "padding": "40px"},
    children=[
        html.H1("Need to Buy Dashboard", style={"textAlign": "center", "color": "#333"}),

        html.Div(dcc.Graph(figure=fig) if fig else html.Div("Colonna 'need_to_buy_MW' o 'Giorno' non trovata."), style={"marginBottom": "40px"}),

        html.Div([
            html.H2("NEED TO BUY", style={"textAlign": "center", "color": "#444", "marginBottom": "20px"}),

            DataTable(
                data=df.round(2).to_dict("records"),
                columns=columns,
                page_size=15,
                style_table={"overflowX": "auto", "maxWidth": "95%", "margin": "auto"},
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
                style_data_conditional=style_data_conditional,
            ),
        ]),
    ],
)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

# Final Version of the code
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from app import app

# This is to link with the app.py
dash.register_page(__name__)

# Load data for choropleth maps
path = 'https://github.com/MaJoCedeno/DVGroup/raw/main/'
# df_map = pd.read_excel('dataset_payments.xlsx', sheet_name='POS_country_2022')
df_map = pd.read_excel(path + 'dataset_payments.xlsx',
                       sheet_name='POS_country_2022')

# Load data for bar plot
# df_bar = pd.read_excel('dataset_payments.xlsx', sheet_name='POS_demo_2022')
df_bar = pd.read_excel(path + 'dataset_payments.xlsx',
                       sheet_name='POS_demo_2022') # Local storage - Change later
df_bar.set_index('Payment Method', inplace=True)

# Preprocessing data for bar plot
for column in df_bar.columns[1:]:
    df_bar[column] = round(df_bar[column]*100,2)

# Load the data from the dataset - Nested pie chart
data_number = pd.read_csv(path + 'data_df_1.csv')
data_value = pd.read_csv(path + 'data_df_2.csv')

# Extract unique years and categories from the dataframes
years = data_number['Year'].unique()
categories = data_number['Categories'].unique()

# Preprocessing data for choropleth maps
for column in df_map.columns[1:]:
    df_map[column] = round(df_map[column]*100,2)

# Define a dictionary to map the country codes to country names
country_mapping = {
    'EA19': 'Euro Area',
    'AT': 'Austria',
    'BE': 'Belgium',
    'CY': 'Cyprus',
    'DE': 'Germany',
    'EE': 'Estonia',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'GR': 'Greece',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'PT': 'Portugal',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
}

df_map['Country'] = df_map['Country'].map(country_mapping)

# Preprocessing data for bar plot
df_bar = df_bar.round(2)
df_bar = df_bar.rename(
    columns={'<EUR 500': '<EUR 500', 'EUR 500-\n1,000': 'EUR 500-1,000', 'EUR 1,000-\n2,000': 'EUR 1,000-2,000',
             'EUR 2,000-\n3,000': 'EUR 2,000-3,000', 'EUR 3,000-\n4,000': 'EUR 3,000-4,000',
             '>EUR 5,000': '>EUR 5,000'})

# Initiate Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define app layout
layout = html.Div([
    # Block 1
    html.Div([
        html.Div(
            [
                html.Label('Payment Method:', style={'font-weight': 'bold', 'margin-bottom': '30px'}),
                html.Br(),
                dcc.RadioItems(
                    id='payment_radio',
                    options=[{'label': i, 'value': i} for i in ['Cash', 'Cards', 'Mobile', 'Online', 'Other']],
                    value='Cash',
                    labelStyle={'display': 'inline-block', 'padding': '5px 10px',
                                'border': '1px solid #ccc', 'border-radius': '4px',
                                'margin-right': '10px'},
                    inputStyle={'display': 'none'},  # Hide the radio button input
                    style={'display': 'inline-block', 'margin-top': '30px'}
                )
            ],
            style={'width': '100%', 'text-align': 'center', 'margin-bottom': '30px'}
        ),
        html.Div(
            [
                dcc.Graph(id='v_transaction')
            ],
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
        ),
        html.Div(
            [
                dcc.Graph(id='n_transaction')
            ],
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-bottom': '100px'}
        ),
    ],
        style={'width': '100%', 'text-align': 'center'}
    ),
    html.Div([
        # New order of divs in Block 2 & 3
        html.Div([
            # Block 2
            html.Div([
                dcc.Dropdown(
                    id='filter_dropdown',
                    options=[{'label': i, 'value': i} for i in ['Income', 'Age', 'Education']],
                    value='Income',
                    style={'width': '200px', 'margin-right': '150px'}
                ),
                dcc.Graph(id='bar_plot')
            ],
                style={'width': '100%', 'height': '100%', 'display': 'flex',
                       'justify-content': 'center', 'align-items': 'center'}
            ),
        ],
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

        html.Div([
            # Block 3
            html.Div([
                dcc.Graph(
                    id='nested-donut-chart',
                    style={'height': '100%', 'width': '70%', 'justify-content': 'center', 'align-items': 'center',
                           'margin-left': '300px'}
                ),
                html.Div([
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in years],
                        value=years[0],
                        style={'width': '100%', 'margin-right': '10px', 'margin-bottom': '10px'}
                    ),
                    dcc.Dropdown(
                        id='category-dropdown',
                        options=[{'label': category, 'value': category} for category in categories],
                        value=categories[0],
                        style={'width': '100%', 'margin-right': '10px', 'margin-bottom': '10px'}
                    ),
                    dcc.Dropdown(
                        id='transaction-type-dropdown',
                        options=[
                            {'label': 'Number of Payments', 'value': 'number'},
                            {'label': 'Value of Payments', 'value': 'value'}
                        ],
                        value='number',
                        style={'width': '100%'}
                    ),
                ],
                    style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'width': '30%',
                           'margin-top': '20px', 'margin-right': '50px'}
                ),
            ],
                style={'display': 'flex', 'width': '100%', 'height': '100%', 'justify-content': 'space-between'}
            ),
        ],
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ],
        style={'width': '100%', 'text-align': 'center'})
])

# Define function to generate choropleth map
def generate_map(payment_method, transaction_type, colorscale, zoom):
    # Construct the column name based on selected options
    column = f"{payment_method}_share_POS_{transaction_type}"
    payment_title=f"{payment_method}"
    transaction_title=f"{transaction_type}"

    fig_1 = px.choropleth(df_map, locations='Country',
                        locationmode='country names',
                        color=column,
                        hover_name='Country',
                        title =f'{payment_title} usage across Europe (in terms of {transaction_title} of transactions), 2022',
                        color_continuous_scale=colorscale,
                        scope='europe')

    fig_1.update_geos(
        visible=False,
        resolution=50,
        showcountries=True,
        countrycolor='gray',
        showcoastlines=True,
        coastlinecolor='lightgray',
        showland=True,
        landcolor='white',
        showocean=True,
        oceancolor='white',
        showlakes=False,
        lakecolor='white',
        showrivers=False,
        rivercolor='white',
        projection_type='natural earth',
        lonaxis_range=zoom,  # Adjust the longitude axis range for zoom
        lataxis_range=[35, 72],  # Adjust the latitude axis range for zoom
    )

    fig_1.update_layout(
        margin=dict(t=50, b=0, r=0, l=0), # Reduce spacing in the graph
        height=600, # Adjust the height of the map
        coloraxis_colorbar=dict(title=""),
    )

    return fig_1

# Define callbacks to update choropleth maps
@app.callback(
    [Output('v_transaction', 'figure'),
     Output('n_transaction', 'figure')],
    [Input('payment_radio', 'value')]
)
def update_maps(payment_method):
    v_map = generate_map(payment_method, 'value', 'Blues', zoom=[-20, 35])
    n_map = generate_map(payment_method, 'number', 'Greens', zoom=[-20, 35])
    return v_map, n_map

# Define callback to update bar plot
@app.callback(
    Output('bar_plot', 'figure'),
    [Input('filter_dropdown', 'value')]
)
def update_plot(filter_option):
    if filter_option == 'Income':
        columns = ['<EUR 500', 'EUR 500-1,000', 'EUR 1,000-2,000', 'EUR 2,000-3,000', 'EUR 3,000-4,000', '>EUR 5,000']
    elif filter_option == 'Age':
        columns = ['18-24', '25-39', '40-54', '55-64', '65+']
    elif filter_option == 'Education':
        columns = ['Low', 'Medium', 'High']

    filtered_df = df_bar[columns]

    colors = ['#B3D9FF','#93C6FF','#6FA8FF','#4DA4FF','#0066CC','#003D99','#001A66']

    # Create the bar traces
    bar_traces = [go.Bar(
        x=filtered_df.index,
        y=filtered_df[col],
        name=col,
        marker_color=colors[i],
        hovertemplate='%{y:.2f}%',
    ) for i, col in enumerate(columns)]

    # Combine the traces
    fig_2 = go.Figure(data=bar_traces)

    fig_2.update_layout(
        barmode='group',
        title={
            'text': f'<b>Distribution of population per {filter_option} groups by payment method</b>',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'t': 10, 'b': 20}
        },
        xaxis_title='Payment Method',
        yaxis_title='Percentage',
        width=700,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )

    return fig_2

@app.callback(
    Output('nested-donut-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('transaction-type-dropdown', 'value')]
)
def update_nested_donut(year, category, transaction_type):
    if transaction_type == 'number':
        df = data_number
    else:
        df = data_value

    df_filtered = df[(df['Year'] == year) & (df['Categories'] == category)]
    payment_methods = ['Cash', 'Cards', 'Mobile app', 'Other']

    # For inner slicers, we directly retrieve the payment method values
    payment_method_values = df_filtered[payment_methods].values.flatten().tolist()

    # Create labels for the category (outer slice) and payment methods (inner slices)
    labels = [category] + payment_methods

    colors = [
        '#228b22', '#058c42', '#4EA8DE', '#FB8B24'
    ]

    # Create donut chart figure
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=[None] + payment_method_values, # Don't assign any value to the outer slice
        hole=0.3,
        pull=[0] + [0.10] * len(payment_methods),
        marker=dict(colors=colors),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textposition='outside',
        textfont=dict(size=18),
        domain={'x': [0.0, 1.0], 'y': [0.0, 1.0]},
    )])

    fig.update_layout(
        autosize=False,
        width=600,
        height=600,
        margin=dict(t=50, l=50, r=50, b=50),  # adding margin as a spacer
        # margin=dict(t=0, l=0, r=0, b=0),
        title={
            'text': f'<b>Structure of POS payments by payment instrument</b>',
            'y': 0.93,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },

    )

    return fig


# if __name__ == '__main__':
    # app.run_server(debug=True, port=8080)

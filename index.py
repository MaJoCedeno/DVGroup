import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app, server

# Connect to your app pages
from apps import page1, page2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Page 1', href='/apps/page1', style={
            'background-color': '#DDB892',
            'color': 'white',
            'padding': '14px 25px',
            'text-align': 'center',
            'text-decoration': 'none',
            'display': 'inline-block',
            'border-radius': '25px',  # Add border-radius property for rounded corners
            'margin-right': '10px',
            'margin-left': '10px',
            'margin-top': '20px'
        }),
        dcc.Link('Page 2', href='/apps/page2', style={
            'background-color': '#00b4d8',  #9ad6e3
            'color': 'white',
            'padding': '14px 25px',
            'text-align': 'center',
            'text-decoration': 'none',
            'display': 'inline-block',
            'border-radius': '25px',  # Add border-radius property for rounded corners
            'margin-right': '10px',
            'margin-top': '20px'
        }),
    ], className="row"),
    html.Div(id='page-content', children=[])
])

# Add hover and active styles
app.css.append_css({
    'external_url': (
        'a:hover, a:active {'
        'background-color: green;'
        '}'
    )
})

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/page1':
        return page1.layout
    if pathname == '/apps/page2':
        return page2.layout
    else:
        return "404 Page Error! Please choose a page."


if __name__ == '__main__':
    app.run_server(debug=False, port=8011)

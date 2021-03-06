import dash
import dash_html_components as html

from app_template import GenerateApp

app = dash.Dash(__name__)

app.layout = html.Div(children=GenerateApp(app=app).html)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000, debug=True)
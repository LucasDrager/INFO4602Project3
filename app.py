from flask import Flask, render_template
import altair as alt
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load all JSON files from the graphJSONs folder
    json_folder_path = './Data/graphJSONs/'
    charts = []
    try:
        for filename in os.listdir(json_folder_path):
            if filename.endswith('.json'):
                with open(os.path.join(json_folder_path, filename), 'r') as f:
                    charts.append(f.read())
    except Exception as e:
        return f"Error loading graphs: {e}", 500

    return render_template('Index.html', charts=charts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

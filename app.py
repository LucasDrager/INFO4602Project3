from flask import Flask, render_template, jsonify
import altair as alt
import pandas as pd

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to serve Altair chart as JSON
@app.route('/bar-chart')
def bar_chart():
    # Sample data
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'values': [5, 3, 6, 7, 2]
    })

    # Altair bar chart
    chart = alt.Chart(data).mark_bar().encode(
        x='category',
        y='values'
    )

    # Return the chart as a Vega-Lite JSON
    return chart.to_json()

# Route for the graph page
@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)

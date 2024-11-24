from flask import Flask, render_template
import altair as alt
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():
    # Bar Chart Example
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [4, 7, 2, 5]
    })
    bar_chart = alt.Chart(data).mark_bar().encode(
        x='Category',
        y='Value'
    ).to_json()

    # Line Chart Example
    data_line = pd.DataFrame({
        'x': range(10),
        'y': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    })
    line_chart = alt.Chart(data_line).mark_line().encode(
        x='x',
        y='y'
    ).to_json()

    # Scatter Plot Example
    data_scatter = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [3, 5, 4, 6, 7],
        'Category': ['A', 'B', 'A', 'B', 'A']
    })
    scatter_plot = alt.Chart(data_scatter).mark_point().encode(
        x='x',
        y='y',
        color='Category'
    ).to_json()

    return render_template('index.html', 
                           bar_chart=bar_chart, 
                           line_chart=line_chart, 
                           scatter_plot=scatter_plot)

@app.route('/test')
def test():
    # Create first Altair chart
    data1 = pd.DataFrame({
        'x': range(10),
        'y': [i ** 2 for i in range(10)]
    })

    chart1 = alt.Chart(data1).mark_line().encode(
        x='x',
        y='y'
    ).properties(width=600, height=400)

    # Create second Altair chart
    data2 = pd.DataFrame({
        'x': range(10),
        'y': [2 ** i for i in range(10)]
    })

    chart2 = alt.Chart(data2).mark_line(color='red').encode(
        x='x',
        y='y'
    ).properties(width=600, height=400)

    # Convert charts to JSON
    chart1_json = chart1.to_json()
    chart2_json = chart2.to_json()

    return render_template('test.html', chart1_json=chart1_json, chart2_json=chart2_json)

# Route for the About page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template
import altair as alt
import pandas as pd


app = Flask(__name__)

@app.route('/')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

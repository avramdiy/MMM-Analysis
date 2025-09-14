from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def show_dataframe():
    # Load the data from the specified path
    file_path = r'C:\Users\avram\OneDrive\Desktop\Bloomtech TRG\TRG Week 41\mmm.us.txt'
    df = pd.read_csv(file_path, sep=None, engine='python')
    # Render the dataframe as HTML
    return render_template_string('<h1>DataFrame</h1>{{ table|safe }}', table=df.to_html(index=False))

if __name__ == '__main__':
    app.run(debug=True)
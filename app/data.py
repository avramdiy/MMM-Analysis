from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

# Load the data
file_path = r'C:\Users\avram\OneDrive\Desktop\Bloomtech TRG\TRG Week 41\mmm.us.txt'
df = pd.read_csv(file_path, sep=None, engine='python')

# Remove the 'OpenInt' column
df = df.drop(columns=['OpenInt'])

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Define date ranges for splitting
start = pd.Timestamp('1970-01-02')
end = pd.Timestamp('2017-11-10')
total_days = (end - start).days
split1 = start + pd.Timedelta(days=total_days // 3)
split2 = start + pd.Timedelta(days=2 * total_days // 3)

# Create three dataframes for analysis
df1 = df[df['Date'] < split1].reset_index(drop=True)
df2 = df[(df['Date'] >= split1) & (df['Date'] < split2)].reset_index(drop=True)
df3 = df[df['Date'] >= split2].reset_index(drop=True)

@app.route('/')
def show_all():
	return render_template_string(
		'<h1>MMM DataFrame (Full)</h1>{{ table|safe }}',
		table=df.to_html(index=False)
	)

@app.route('/period1')
def show_period1():
	return render_template_string(
		'<h1>MMM DataFrame (Period 1)</h1>{{ table|safe }}',
		table=df1.to_html(index=False)
	)

@app.route('/period2')
def show_period2():
	return render_template_string(
		'<h1>MMM DataFrame (Period 2)</h1>{{ table|safe }}',
		table=df2.to_html(index=False)
	)

@app.route('/period3')
def show_period3():
	return render_template_string(
		'<h1>MMM DataFrame (Period 3)</h1>{{ table|safe }}',
		table=df3.to_html(index=False)
	)

if __name__ == '__main__':
	app.run(debug=True)
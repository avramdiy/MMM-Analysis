
import matplotlib.pyplot as plt
import io
import base64


from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

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

def plot_avg_open(df, label):
	monthly_avg = df.groupby(df['Date'].dt.to_period('M'))['Open'].mean()
	fig, ax = plt.subplots()
	monthly_avg.plot(ax=ax, title=f'Average Open Price per Month ({label})')
	ax.set_xlabel('Month')
	ax.set_ylabel('Average Open Price')
	fig.tight_layout()
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	buf.seek(0)
	img_base64 = base64.b64encode(buf.read()).decode('utf-8')
	plt.close(fig)
	return img_base64

@app.route('/avg_open')
def avg_open_plot():
	img1 = plot_avg_open(df1, 'Period 1')
	img2 = plot_avg_open(df2, 'Period 2')
	img3 = plot_avg_open(df3, 'Period 3')
	html = f'''
		<h1>Average Open Price per Month</h1>
		<h2>Period 1</h2><img src="data:image/png;base64,{img1}"/>
		<h2>Period 2</h2><img src="data:image/png;base64,{img2}"/>
		<h2>Period 3</h2><img src="data:image/png;base64,{img3}"/>
	'''
	return render_template_string(html)

if __name__ == '__main__':
	app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/visaanswer')
def visaanswer():
	return render_template('webversion2.html')

@app.route('/visaanswer')
def choice():
	abstract = ['Afganistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Austria', 'Azerbaijan']
	return render_template('webversion2.html', abstract = abstract)

if __name__ == "__main__":
	app.run()





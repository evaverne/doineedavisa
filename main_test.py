from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

#the following code is for sending data to the user to chose. 

conn_string = "dbname='visachecker' user = 'evaverne'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

statement = "SELECT citizenship FROM test"

cursor.execute(statement)
conn.commit()
operatewithit = [r[0] for r in cursor.fetchall()]  #also converts from list of tuples to a list

statement1 = "SELECT country from test1"

cursor.execute(statement1)
conn.commit()
call_for_countries = [r[0] for r in cursor.fetchall()]

#the main trigger

@app.route('/test', methods = ["GET", "POST"])
def visatest():
	try:
		if request.method == "POST":
			cit = request.form['citizen']
			cou = request.form['countr']

			db_command1 = "SELECT uid FROM test WHERE citizenship = '{}'".format(cit)
			cursor.execute(db_command1)
			conn.commit()
			store = cursor.fetchone()[0]
			
			db_command2 = "SELECT uid FROM test1 WHERE country = '{}'".format(cou)
			cursor.execute(db_command2)
			conn.commit()
			store2 = cursor.fetchone()[0]
			
			db_command3 = "SELECT requirements FROM test2 WHERE citizenship = '%s' AND country = '%s'"
			team = (store, store2)
			cursor.execute(db_command3, team)
			conn.commit()
			store3 = cursor.fetchone()[0]

			db_command4 = "SELECT comment FROM test2 WHERE citizenship = '%s' AND country = '%s'"
			team = (store, store2)
			cursor.execute(db_command4, team)
			conn.commit()
			store4 = cursor.fetchone()[0]
			
			return render_template('webversion.html', variable = store3, variable2 = store4, countries = operatewithit, country = call_for_countries)
	except TypeError:
		message = 'In some cases the information is unavailable. Perhaps respective sides did not come up with the agreement yet. But please, continue to explore.'
		return render_template('webversion.html', variable = message, countries = operatewithit, country = call_for_countries)
	return render_template('webversion.html', countries = operatewithit, country = call_for_countries)


if __name__ == '__main__':
	app.run(debug=True)
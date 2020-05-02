from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)


class TodoList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(200))
	complete = db.Column(db.Boolean)


@app.route('/')
def index():
	todos = TodoList.query.order_by(TodoList.id).all()
	return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
	if request.form['new-todo'] != '':
		new_todo = TodoList(text=request.form['new-todo'], complete=False)
		db.session.add(new_todo)
		db.session.commit()
		return redirect(url_for('index'))
	return redirect(url_for('index'))


@app.route('/delete/<item_id>', methods=['POST'])
def delete(item_id):
	TodoList.query.filter_by(id=item_id).delete()
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
	db.session.query(TodoList).delete()
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/complete/<item_id>', methods=['POST'])
def complete(item_id):
	if TodoList.query.filter_by(id=item_id).first().complete != True:
		TodoList.query.filter_by(id=item_id).update({'complete': True})
		db.session.commit()
		return redirect(url_for('index'))
	else:
		TodoList.query.filter_by(id=item_id).update({'complete': False})
		db.session.commit()
		return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True, port=5002)
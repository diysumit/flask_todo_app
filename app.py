#imports
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)#app passed self __name__

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db' #configuring our database using sqlite, sqlite:///main.db created db in our project folder
db = SQLAlchemy(app)#for linking our app and our data base

'''Class to work with database
    adds three columns to our database: id, content, date_created
'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)#id integer type also primary_key to our database
    content = db.Column(db.String(250), nullable=False)#content to store content or tasks
    date_created = db.Column(db.DateTime, default=datetime.utcnow)#adds date-time marker for individual tasks and day they were created

    #overriding __repr__ method to return task with id
    def __repr__(self):
        return '<Task %r>' % self.id

#an app route to send requests and get response
#created a resource at / , accepts two type of requests: POST and GET
@app.route('/', methods=['POST', 'GET'])
def index():
    #handling POST request
    if request.method == 'POST':
        task_content = request.form['content']#used id:content to accept str input
        new_task = Todo(content=task_content)

        #trying to add to data base
        try:
            db.session.add(new_task)#add command
            db.session.commit()#commit command
            return redirect('/')#when done redirect to home or resource at /
        #if above task fails return an error
        except:
            return 'There was an issue adding your task'
    #handling GET request
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()#showing content of database on order they were created
        return render_template('index.html', tasks=tasks)#passing task for rendering
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


#executing app with debug on
if __name__ == "__main__":
    app.run(debug=True)
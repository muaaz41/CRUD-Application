from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class myTask(db.Model):
    id = db.Column(db.Integer ,primary_key =True)
    content = db.Column(db.String(100),nullable=False)
    completed = db.Column(db.Integer)
    created = db.Column(db.DateTime ,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"TASK {self.id}"

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        current_task=request.form['content']
        new_task =myTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error:{e}')
            return "There was an issue adding your task"
    else:
        task = myTask.query.order_by(myTask.created).all()
        return render_template('index.html',task=task)

@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task=myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f'Error:{e}')
        return "There was an issue adding your task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    task = myTask.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error: {e}')
            return "There was an issue updating your task"
    else:
        return render_template('update.html',task=task)

if __name__ == "__main__":
    app.run(debug=True)
 
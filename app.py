
from flask import Flask,render_template,url_for,request,redirect
#db
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
#init db
db=SQLAlchemy(app)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        content=request.form['content']
        new_task=Todo(content=content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'issue'
            pass


    else:
        #queringtodo
        tasks=Todo.query.order_by(Todo.date_created).all()#or.first

        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delte=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delte)
        db.session.commit()
        return redirect('/')
    except:
        return 'problem'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'problem'


    else:
        return render_template('update.html',task=task_to_update)
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

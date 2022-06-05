from flask import Flask,render_template,redirect,request,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import main


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///item.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Item(db.Model):
    sno  =  db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(200),nullable=False)
    rating  =  db.Column(db.String(200),nullable=False)
    price = db.Column(db.Integer,nullable=False)

    def __repr__(self)->str:
        return f"{self.sno} - {self.name}"


@app.route('/',methods=["GET","POST"])
def home():
    db.create_all()
    if request.method=="POST":
        search=request.form["item"]
        print(request.form.get('excel'))
        if request.form.get('excel')=='on':
            save=True
        else:
            save=False
        main.search(search,save)
    itemdb=Item.query.all()
    db.drop_all()
    return render_template("index.html",items=itemdb)

@app.route('/about')
def about():
    return render_template("about.html")

def items(df):
    db.create_all()
    for index in df.index:
        name=df['Item'][index]
        rating=df['Rating'][index]
        price=df['Price'][index]
        item=Item(name=name,rating=rating,price=price)
        db.session.add(item)
        db.session.commit()
def save(file):
    return send_file(file,as_attachment=True)
if __name__=="__main__":
    app.run(debug=True,port=8000)
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

def dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route('/random')
def  randcafe():
    cafes = db.session.query(Cafe).all()
    random_choice = random.choice(cafes)
    random_choice = dict(random_choice)
    return jsonify(random_choice)

@app.route('/all')
def allcafes():
    cafes = db.session.query(Cafe).all()
    return jsonify([dict(cafe)for cafe in cafes])

@app.route('/select')
def search_cafe():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(dict(cafe))
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

## HTTP POST - Create Record

@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={'success':'Successfully added new cafe'})

## HTTP PUT/PATCH - Update Record

@app.route('/update-price/<int:cafeId>', methods=['PATCH', 'POST'])
def update_cafe(cafeId):
    cafe = db.session.query(Cafe).get(cafeId)
    price = request.args.get("price")
    if cafe:
        cafe.cafe_price = price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafeId>', methods=['DELETE', 'POST'])
def delete_closed(cafeId):
    cafe = db.session.query(Cafe).get(cafeId)
    api_key = request.args.get("api_key")
    if cafe:
        if api_key == '12334':
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(respone={"success": "Successfully deleted the cafe from the database."})
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."})
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

if __name__ == '__main__':
    app.run(debug=True)

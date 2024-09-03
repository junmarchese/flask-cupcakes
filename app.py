"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "favoriteSprinklesCupcakes"

    connect_db(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return data of all cupcakes.  Returns JSON like:
        {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.cupcake_dict() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_spec_cupcake(cupcake_id):
    """Return data on specific cupcake. Returns JSON like:
        {cupcake: {id, flavor, size, rating, image}}    
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.cupcake_dict())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add a cupcake and return data about new cupcake. Returns JSON like:
        {cupcake: {id, flavor, size, rating, image}}    
    """
    data = request.json

    id = data.get("id")
    flavor = data.get("flavor")
    size = data.get("size")
    rating = data.get("rating")
    image = data.get("image") or "https://tinyurl.com/demo-cupcake"

    new_cupcake = Cupcake(id=id, flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    response = jsonify(cupcake=new_cupcake.cupcake_dict())
    response.status_code = 201
    return response


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update an existing cupcake and return its data."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get("flavor", cupcake.flavor)
    cupcake.size = data.get("size", cupcake.size)
    cupcake.rating = data.get("rating", cupcake.rating)
    cupcake.image = data.get("image", cupcake.image)
    
    db.session.commit()

    return jsonify(cupcake=cupcake.cupcake_dict()), 200


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake and return a 404 message if cupcake not found."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")






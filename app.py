from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt  # Import sha256_crypt from passlib.hash



app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLAlchemy configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/garage'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use SQLite database named 'database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Models
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100),nullable=False)
    ingredients = db.Column(db.String(100))
    cook_time = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    

# Routes
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    my_recipes = Recipe.query.all()
    print(my_recipes)
    return render_template('index.html', recipes=my_recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        cook_time = request.form['cook_time']
        
        new_recipe = Recipe(recipe_name=recipe_name, ingredients=ingredients, cook_time=cook_time)
        
        db.session.add(new_recipe)
        db.session.commit()
        
        flash('Recipe added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

# Update Recipe
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if not session.get('logged_in'):
        flash('You need to be logged in to edit a recipe.', 'error')
        return redirect(url_for('login'))

    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        flash('Recipe not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        recipe.recipe_name = request.form['recipe_name']
        recipe.ingredients = request.form['ingredients']
        recipe.cook_time = request.form['cook_time']

        db.session.commit()
        flash('Recipe updated successfully', 'success')
        return redirect(url_for('index'))

    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password matches using sha256_crypt.verify
        if user and sha256_crypt.verify(password, user.password):
            # Password matches, set session and redirect to a protected route
            session['logged_in'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            # Invalid username or password, show error message
            flash('Invalid username or password', 'error')
    elif request.method == 'GET':
        # Render the login form for GET requests
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('register'))

        # Hash the password before storing it in the database
        hashed_password = sha256_crypt.hash(password)  # Use sha256_crypt from passlib

        # Create a new user with the hashed password
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    elif request.method == 'GET':
        # Render the registration form for GET requests
        return render_template('register.html')
    
    

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

from flask_app import app, render_template, request, redirect, session, flash, bcrypt
from flask_app.models.tech import Tech
from flask_app.models.facilitie import Facilitie


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reg', methods = ['post'])
def reg():
    print(request.form)
    data = {'email': request.form['email']}
    tech_in_db = Tech.get_one_with_email(data)
    if tech_in_db:
        flash("email already in use", 'email')
        return redirect('/')
    if not Tech.validate_tech(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    print(data)
    tech_id = Tech.save(data)
    session['tech_id'] = tech_id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')


@app.route('/login', methods = ['post'])
def login():
    data = {'email': request.form['log_email']}
    tech_in_db = Tech.get_one_with_email(data)
    if not tech_in_db:
        flash("login invalid")
        return redirect('/')
    if not bcrypt.check_password_hash(tech_in_db.password, request.form['log_password']):
        flash("login invalid")
        return redirect('/')
    session['tech_id'] = tech_in_db.id
    session['first_name'] = tech_in_db.first_name
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    pass

@app.route('/edit/tech')
def edit():
    data = {'id': session['tech_id']}
    return render_template('edit_tech.html', tech = Tech.get_one(data))

@app.route('/update/tech', methods = ['POST'])
def updateTech():
    print(request.form)
    if not Tech.validate_tech(request.form):
        return redirect('/edit/tech')
    Tech.update(request.form)
    return redirect('/dashboard')

@app.route('/show/tech')
def show_tech():
    data = {'id': session['tech_id']}
    return render_template('show_tech.html', tech = Tech.get_one_with_facilities(data))

@app.route('/dashboard')
def dashboard():
    if 'tech_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', facilities = Facilitie.get_all_with_tech())
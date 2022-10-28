from flask_app import app, render_template, request, redirect, session
from flask_app.models.facilitie import Facilitie
from flask_app.models.tech import Tech


@app.route('/facilities')
def facilities():
    if 'tech_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html', facilities = Facilitie.get_all_with_tech())

@app.route('/new/facilitie')
def new_facilitie():
#####
    return render_template('add_show.html')

@app.route('/create/facilitie', methods = ['post'])
def create_facilitie():
    print(request.form )
    if not Facilitie.validate_facilitie(request.form):
        return redirect('/new/facilitie')
    data = {
        'name' : request.form['name'],
        'address' : request.form['address'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'tech_id': request.form['tech_id']
    }
    Facilitie.save(request.form)
    return redirect('/facilities')

@app.route('/createfacilitiesuccess', methods=['post'])
def success_facilitie():
    print(request.form)
    facilitie = Facilitie.save(request.form)
    return redirect('/createfacilitie')

@app.route('/show/facilitie/<int:id>')
def show_facilitie(id):
    data = {'id': id}
    # tech = Tech.get_one({'id':facilitie.tech_id})
    return render_template('show_facilitie.html', facilitie = Facilitie.get_one(data))

@app.route('/delete/<int:id>')
def delete_facilitie(id):
    data = {'id':id}
    Facilitie.delete(data)
    return redirect("/facilities")

@app.route('/edit/<int:id>')
def edit_facilitie(id):
    data = {'id':id}
    return render_template('edit_facilitie.html', facilitie = Facilitie.get_one(data))

@app.route('/update/facilitie', methods=['post'])
def update_facilitie():
    print(request.form)
    if not Facilitie.validate_facilitie(request.form):
        return redirect(f"/edit/{request.form['id']}")
    Facilitie.update(request.form)
    return redirect(f"/dashboard")
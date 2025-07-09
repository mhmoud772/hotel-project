
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Room

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # لاستخدام الـ sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    rooms = Room.query.all()
    return render_template('home.html', rooms=rooms)

@app.route('/add', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        price = request.form['price']
        new_room = Room(room_number=room_number, room_type=room_type, price=price)

        db.session.add(new_room)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_room.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    room = Room.query.get_or_404(id)
    if request.method == 'POST':
        room.room_number = request.form['room_number']
        room.room_type = request.form['room_type']
        room.price = request.form['price']

        db.session.commit()
        flash('تم تعديل الغرفة بنجاح!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_room.html', room=room)

@app.route('/delete/<int:id>')
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('تم حذف الغرفة بنجاح!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

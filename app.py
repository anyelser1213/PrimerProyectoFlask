from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from Models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/BaseDatos.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    password = db.Column(db.String(200))


class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200))
    listo = db.Column(db.Boolean)



#### TODO ESTO ES PARA AUTENTICACION ######

# Clave secreta para las secciones
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    if 'username' in session:
        publicaciones = Publicacion.query.all()
        return render_template('index.html', publicaciones = publicaciones)
    return redirect(url_for('login'))
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    #Verificamos que tipo de metodo es
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    
    return render_template('login.html')
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


###############################################################



@app.route('/create-task', methods=['POST'])
def create():
    nueva_publicacion = Publicacion(contenido=request.form['contenido'], listo= False)
    db.session.add(nueva_publicacion)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    publicacion = Publicacion.query.filter_by(id=int(id)).first()
    publicacion.listo = not(publicacion.listo)
    db.session.commit()
    return redirect(url_for('home'))


#Para actualizar la publicacion
@app.get('/updateGet/<id>')
def updateGet(id):
    
    #Cuando es un solo objeto aplicamos asi
    publicacion = Publicacion.query.filter_by(id=id).first()
    db.session.commit()
    return render_template("actualizar.html", publicacion = publicacion)


@app.post('/update/<id>')
def update(id):
    publicacion = Publicacion.query.filter_by(id=int(id)).first()
    #print("Probando cosas")
    #print(request.form)
    publicacion.contenido = request.form['contenido']
    db.session.commit()
    return redirect(url_for('home'))





@app.route('/delete/<id>')
def delete(id):
    Publicacion.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
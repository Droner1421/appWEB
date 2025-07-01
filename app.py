from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from conexionDB import conexionDB

app = Flask(__name__)
app.secret_key = 'clave_secreta'
db = conexionDB()
personal = db['personal']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = personal.find_one({'usuario': usuario, 'contrasena': contrasena})
        if user:
            tipo = user['tipo_usuario']
            _id = str(user['_id'])
            flash(f'Bienvenido {usuario} ({tipo})')
            if tipo == 'medico':
                return redirect(url_for('vista_medico', id_usuario=_id))
            else:
                return redirect(url_for('vista_recepcionista', id_usuario=_id))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'apellido_paterno': request.form['apellido_paterno'],
            'apellido_materno': request.form['apellido_materno'],
            'telefono': request.form['telefono'],
            'usuario': request.form['usuario'],
            'contrasena': request.form['contrasena'],
            'tipo_usuario': request.form['tipo_usuario']
        }
        if personal.find_one({'usuario': data['usuario']}):
            flash('El usuario ya existe')
        else:
            personal.insert_one(data)
            flash('Registro exitoso. Ya puedes iniciar sesión.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/medico/<id_usuario>')
def vista_medico(id_usuario):
    return render_template('medico.html', id_usuario=id_usuario)

@app.route('/recepcionista/<id_usuario>')
def vista_recepcionista(id_usuario):
    return render_template('recepcionista.html', id_usuario=id_usuario)

if __name__ == '__main__':
    app.run(debug=True)

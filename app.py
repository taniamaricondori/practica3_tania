from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para usar sesiones

@app.route('/')
def index():
    return render_template('index.html')

# Inicializar la lista de inscritos en cada petición si no existe
def init_session():
    if 'inscritos' not in session:
        session['inscritos'] = []
    if 'id_counter' not in session:
        session['id_counter'] = 1  # Inicializar el contador de ID en 1

# Ruta para el formulario de registro de seminarios
@app.route('/registro_seminario', methods=['GET', 'POST'])
def registro_seminario():
    init_session()  # Inicializar la sesión si es necesario

    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')
        
        nuevo_id = len(session['inscritos']) + 1

        # Crear un diccionario para los datos
        inscrito = {
            'id': nuevo_id,
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': ', '.join(seminarios)
        }
        
        # session['id_counter'] += 1

        # Guardar los datos en la sesión
        session['inscritos'].append(inscrito)
        session.modified = True

        return redirect(url_for('listado_inscritos'))

    return render_template('registro_seminario.html')

# Ruta para mostrar el listado de inscritos
@app.route('/listado_inscritos')
def listado_inscritos():
    init_session()  # Inicializar la sesión si es necesario

    return render_template('listado_inscritos.html', inscritos=session['inscritos'])

# Ruta para editar un inscrito
@app.route('/editar_inscrito/<int:index>', methods=['GET', 'POST'])
def editar_inscrito(index):
    init_session()  # Inicializar la sesión si es necesario

    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Actualizar los datos del inscrito
        inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': ', '.join(seminarios)
        }

        session['inscritos'][index] = inscrito  # Actualizar en la sesión
        session.modified = True

        return redirect(url_for('listado_inscritos'))

    inscrito = session['inscritos'][index]  # Obtener el inscrito a editar
    return render_template('editar_inscrito.html', inscrito=inscrito, index=index)

# Ruta para eliminar un inscrito
@app.route('/eliminar_inscrito/<int:index>')
def eliminar_inscrito(index):
    init_session()  # Inicializar la sesión si es necesario
    del session['inscritos'][index]  # Eliminar el inscrito
    session.modified = True
    return redirect(url_for('listado_inscritos'))

if __name__ == '__main__':
    app.run(debug=True)

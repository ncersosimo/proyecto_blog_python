'''
Flask [Python]
Ejemplos de clase

Autor: Inove Coding School
Version: 2.0

Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas que registran su ritmo cardíaco.

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

import traceback, os
from flask import Flask, request, jsonify, render_template, Response

# Crear el server Flask
app = Flask(__name__)

# Base de datos
from flask_sqlalchemy import SQLAlchemy

def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == 'posix':  # Unix/Linux/Mac
        os.system("clear")
    elif sistema_operativo == 'nt':  # Windows
        os.system("cls")

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Asociamos nuestro controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)

# ------------ Tablas de la DB ----------------- #
class Posteos(db.Model):
    __tablename__ = "posteos"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    titulo = db.Column(db.String)
    texto = db.Column(db.String)
    
    def __repr__(self):
        return f"Usuario: {self.usuario}. Título del posteo: {self.titulo}"


# ------------ Rutas o endpoints ----------------- #
# Ruta que se ingresa por la URL 127.0.0.1:5000
@app.route("/")
def index():
    try:
        # Renderizar el temaplate HTML blog.html
        print("Renderizar blog.html")
        return render_template('blog.html')
    except:
        return jsonify({'trace': traceback.format_exc()})
    
# Ruta que se ingresa por la URL 127.0.0.1:5000/login
@app.route("/login")
def login():
    try:
        # Renderizar el temaplate HTML login.html
        print("Renderizar login.html")
        return render_template('login.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

# Ruta que se ingresa por la ULR 127.0.0.1:5000/posteos/
@app.route("/posteos/<usuario>", methods=['GET', 'POST', 'DELETE'])
def posteos(usuario):
    if request.method == 'GET':        
        try:
            # Obtenemos todos los posteos del usuario y
            # los ordenamos por id para obtener primero el ultimo registro
            query = db.session.query(Posteos).filter(Posteos.usuario == usuario).order_by(Posteos.id.desc())     

            # Limitamos la cantidad de posteos a mostrar del usuario
            query = query.limit(3)
            query = query.all()

            datos = []
            
            # Si hay registros, agrego los diccionarios a la lista
            if query is not None and len(query) > 0:            
                for posteo in query:
                    json_result = {}
                    json_result['titulo'] = posteo.titulo
                    json_result['texto'] = posteo.texto
                    datos.append(json_result)

            print("Posteos del usuario:")
            print(datos)

            return jsonify(datos)
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            # Obtenemos del HTTP POST JSON el titulo y texto del posteo
            titulo = str(request.form.get('titulo'))
            texto = str(request.form.get('texto'))

            if(titulo is None or texto is None):
                # Datos ingresados incorrectos
                return Response(status=400)
            
            # Crear un nuevo registro de pulsaciones
            posteos = Posteos(usuario=usuario, titulo=titulo, texto=texto)

            # Agregar el registro de posteos a la DB
            db.session.add(posteos)
            db.session.commit()

            # Indicamos que la petición se completó con éxito 
            # retornando código status 201:
            return Response(status=201)
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'DELETE':        
        try:
            # Obtenemos todos los posteos del usuario 
            # y realizamos la eliminación de los mismos
            query = db.session.query(Posteos).filter(Posteos.usuario == usuario).delete()            
            db.session.commit()

            # Imprimo en la consola la cantidad de registros eliminados
            print(f"Posteos eliminados del usuario {usuario}: {query}")
            
            return Response(status=201)
        except:
            return jsonify({'trace': traceback.format_exc()})



# Este método se ejecutará la primera vez
# cuando se construye la app.
with app.app_context():
    # Crear aquí la base de datos
    db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')
    limpiar_consola()
    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
import json
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, request, session
import os
import datetime
import os.path


## pasword encriptado
usuario={"username":"luis","password":"sha256$J6xaXBNEmJt7qCqOlj5Vy64BJ3qaUw$49ea080b0cc4b43ebf05079db72dd9c15cce560c5041cbaffe0dea5af5826035"}

from flask import Flask
app = Flask(__name__)


###  clave para la llave de sesion###
app.secret_key = "SQwHVi7VvgpHRf92gV8hVK7IEprPUbFhju4U5QtX"
#tiempo de vida de la sesion
app.permanent_session_lifetime = datetime.timedelta ( minutes=1440 )

"""
##ruta sin protecion para prueba
@app.route("/hello")
def hello():
    return jsonify({"message":"hello"}),200
"""

# Valida si esta o no en sesion el usuario el methods=['GET']
# no se define por que ya viene por default
@app.route('/')
def inicio():
    if usuario['username'] in session:
        return jsonify({"message":"Usuario en sesion"}+usuario['username']),200
    return jsonify({"message":"Usuario no en sesion"}),401


# probando ruta
@app.route('/ping')
def ping():
    if usuario['username'] in session:
        session.pop ( usuario['username'] )
        return jsonify({'response': 'pong!'}),200
    else:
        return jsonify({'response': 'inicie sesion /login'}),401


@app.route('/login', methods=['POST'])
def login():
        if request.authorization.username == usuario['username']:
            if check_password_hash(usuario["password"],request.authorization.password):
                session[request.authorization["username"]] = request.authorization["username"]
                return jsonify({"message":"Sesion iniciada"}),200
            else:
                return jsonify ( {"error" : "Password invalido"} ),401
        else:
            return jsonify ( {"error" : "username invalido"} ),401


@app.route('/logout', methods=['POST'])
def logout():
    if usuario['username'] in session:
        session.pop(usuario['username'])
        return jsonify ( {"Message" : "End user session"} ),200
    else:
        return jsonify ( {"Message" : "No session user found"} ), 200


#Delete files
@app.route('/api/exec/delete', methods=['POST'])
def process_json():
    if usuario['username'] in session :
        file = list(request.json)
        status=[]
        for f in file :
            ## If file exists, delete it and print json message##
            if os.path.isfile ( f ) :
                os.remove ( f )
                status.append("200 OK"+" "+ os.path.basename(f))
            else :  ## Show an error ##
                status.append("404 error"+" "+ os.path.basename(f))
        session.pop ( usuario['username'] )
        return status
    else:
        return jsonify ( {'response' : 'inicie sesion /login'} ), 401


@app.route('/api/file')
def info_files():
    #valida si el usuario esta en sesion
    if usuario['username'] in session :
        # extrae la info a procesar
        FILE_PATH = request.json
        # genera el comando
        command = 'permisos.sh ' + FILE_PATH['file'] + ' > /opt/apiml/permisos.txt'
        # Ejecuta el comando y guarda resultado en /opt/apiml/permisos.txt
        os.system(command)
        # extrae el resultado del archivo y lo guarada en f
        f = open("/opt/apiml/permisos.txt","r")
        #Termina la sesion del usuario
        session.pop ( usuario['username'] )
        # Retorna el valor leido en formato JSON con codigo 200
        return jsonify (json.loads(f.read())), 200
    else:
        # si el usuario no esta en sesion retorna retorna messaje indicando que debe iniciar sesion y codigo 401
        return jsonify ( {'response' : 'inicie sesion /login'} ), 401

""" ya no me dio tiempo en resolver el problema
@app.route('/vtscan',methods=['POST'])
def vtscan():
#    if usuario['username'] in session :
        data = request.json
        print(data['file'])
        FILE_PATH = '/opt/apiml/eicar.com.txt'
        print(FILE_PATH)
        # Create dictionary containing the file to send for multipart encoding upload
        files = {"file": (os.path.basename(FILE_PATH), open(os.path.abspath(FILE_PATH), "rb"))}

        with virustotal_python.Virustotal("cb111fa83a225787af039fd3ab95491b1fe89551b165232bdd8772a393e4a6fd") as vtotal:
            resp = vtotal.request("files", files=files, method="POST")
            pprint(f"ultimo {FILE_PATH}")
            pprint(resp.json())
        return json.jsonify(json.loads(resp.json()))
#    else:
#        return jsonify ( {'response' : 'inicie sesion /login'} ), 401
"""

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='127.0.0.1')
root@testapi:/opt/apiml#

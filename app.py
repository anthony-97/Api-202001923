from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente
from Medicamento import Medicamento

app = Flask(__name__)
CORS(app)

#Almacenamiento
administrador = {
    "nombre":"ingrid",
    "apellido":"perez",
    "nombre_usuario":"admin",
    "contrasena":"1234"
}

pacientes = []
medicamentos = []
doctores = []

@app.route('/', methods=['GET'])
def principal():
    return "Api Taller 1"

@app.route('/registro_paciente', methods=['POST'])
def registro_paciente():
    cuerpo = request.get_json()
    nombre = cuerpo['nombre'] 
    apellido = cuerpo['apellido']
    fecha_nacimiento = cuerpo['fecha_nacimiento']
    sexo = cuerpo['sexo']
    nombre_usuario = cuerpo['nombre_usuario']
    if(existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'Ya existe un usuario con este nombre'})
    contrasena = cuerpo['contrasena']
    telefono = cuerpo['telefono']
    nuevo_paciente = Paciente(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global pacientes
    pacientes.append(nuevo_paciente)
    return jsonify({'agregado':1,'mensaje':'Registro exitoso'})

@app.route('/obtener_pacientes', methods=['GET'])
def obtener_pacientes():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if not existe_usuario(nombre_usuario):
        return jsonify({'estado': 0, 'mensaje':'No existe este usuario'})
    if verificar_contrasena(nombre_usuario,contrasena):
        return jsonify({'estado': 1, 'mensaje':'Login exitoso'})
    return jsonify({'estado': 0, 'mensaje':'La contrasena es incorrecta'})
    

def verificar_contrasena(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario and paciente.contrasena == contrasena:
            return True
    return False

def existe_usuario(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True
    return False

#INICIO CRUD MEDICAMENTOS
@app.route('/cargar_medicamentos', methods=['POST'])
def cargar_medicamentos():
    cuerpo = request.get_json()
    contenido = cuerpo['contenido']
    filas = contenido.split("\n")
    global medicamentos
    for fila in filas:
        print(fila)
        columnas = fila.split(",")
        medicamento = Medicamento(columnas[0],columnas[1],columnas[2],columnas[3])
        medicamentos.append(medicamento)
    return jsonify({"mensaje":"Carga masiva exitosa"})

@app.route('/obtener_medicamentos', methods=['GET'])
def obtener_medicamentos():
    json_medicamentos = []
    global medicamentos
    for medicamento in medicamentos:
        json_medicamentos.append(medicamento.get_json())
    return jsonify(json_medicamentos)

@app.route('/eliminar_medicamento', methods=['POST'])
def eliminar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global medicamentos
    medicamentos.pop(i)
    return jsonify({"mensaje":"Eliminado exitosamente"})

@app.route('/editar_medicamento', methods=['POST'])
def editar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    precio = cuerpo['precio']
    descripcion = cuerpo['descripcion']
    cantidad = cuerpo['cantidad']
    i = int(indice)
    global medicamentos
    medicamentos[i].editar(nombre,precio,descripcion,cantidad)
    return jsonify(medicamentos[i].get_json())

#FIN CRUD MEDICAMENTOS

#INICIO CRUD DOCTORES
@app.route('/cargar_doctores', methods=['POST'])
def cargar_doctores():
    cuerpo = request.get_json()
    contenido = cuerpo['contenido']
    filas = contenido.split("\n")
    global doctores
    for fila in filas:
        print(fila)
        columnas = fila.split(",")
        doctor = Doctor(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6],columnas[7])
        doctores.append(doctor)
    return jsonify({"mensaje":"Carga masiva exitosa"})

@app.route('/obtener_doctores', methods=['GET'])
def obtener_doctores():
    json_doctores = []
    global doctores
    for doctor in doctores:
        json_doctores.append(doctor.get_json())
    return jsonify(json_doctores)

@app.route('/eliminar_doctor', methods=['POST'])
def eliminar_doctor():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global doctores
    doctores.pop(i)
    return jsonify({"mensaje":"Eliminado exitosamente"})

#nombre
#apellido
#fecha_nacimiento
#sexo
#nombre_usuario
#contrasena
#especialidad
#telefono
@app.route('/editar_doctor', methods=['POST'])
def editar_doctor():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    apellido = cuerpo['apellido']
    fecha_nacimiento = cuerpo['fecha_nacimiento']
    sexo = cuerpo['sexo']
    nombre_usuario = cuerpo['nombre_usuario']
    contrasena = cuerpo['contrasena']
    especialidad = cuerpo['especialidad']
    telefono = cuerpo['telefono']
    i = int(indice)
    global doctores
    doctores[i].editar(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,especialidad,telefono)
    return jsonify(doctores[i].get_json())

#FIN CRUD DOCTORES

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)

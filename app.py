from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente
from Medicamento import Medicamento
from Doctor import Doctor
from Enfermera import Enfermera
from Cita import Cita
from Factura import Factura

app = Flask(__name__)
CORS(app)

#Almacenamiento
#Cambios en las url's y tambien se le quito la s al https.
administrador = {
    "nombre":"ingrid",
    "apellido":"perez",
    "nombre_usuario":"admin",
    "contrasena":"1234"
}

pacientes = []
medicamentos = []
doctores = []
enfermeras = []
citas = []
facturas = []

@app.route('/', methods=['GET'])
def principal():
    return "API Proyecto 2"

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

#Metodos paciente
@app.route('/cargar_pacientes', methods=['POST'])
def cargar_pacientes():
    cuerpo = request.get_json()
    contenido = cuerpo['contenido']
    filas = contenido.split("\n")
    global pacientes
    for fila in filas:
        print(fila)
        columnas = fila.split(",")
        paciente = Paciente(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6])
        pacientes.append(paciente)
    return jsonify({"mensaje":"Carga masiva exitosa"})

@app.route('/obtener_pacientes', methods=['GET'])
def obtener_pacientes():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

@app.route('/eliminar_paciente', methods=['POST'])
def eliminar_paciente():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global pacientes
    pacientes.pop(i)
    return jsonify({"mensaje":"Eliminado exitosamente"})

@app.route('/editar_paciente', methods=['POST'])
def editar_paciente():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    apellido = cuerpo['apellido']
    fecha_nacimiento = cuerpo['fecha_nacimiento']
    sexo = cuerpo['sexo']
    nombre_usuario = cuerpo['nombre_usuario']
    contrasena = cuerpo['contrasena']
    telefono = cuerpo['telefono']
    i = int(indice)
    global pacientes
    pacientes[i].editar(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    return jsonify(pacientes[i].get_json())

#Fin metodos paciente

def verificar_contrasena(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return 1
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario and paciente.contrasena == contrasena:
            return 2
    global doctores 
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario and doctor.contrasena == contrasena:
            return 3
    global enfermeras
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario and enfermera.contrasena == contrasena:
            return 4
    return 0

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if not existe_usuario(nombre_usuario):
        return jsonify({'estado': 0,'mensaje':'No existe este usuario'})
    sesion = verificar_contrasena(nombre_usuario,contrasena)
    if sesion == 1 or 2 or 3 or 4 or 0:
        return jsonify({'estado': 1, 'sesion': sesion, 'mensaje':'Login exitoso','indice': get_indice_usuario(nombre_usuario), 'nombre': get_nombre(nombre_usuario)})
    return jsonify({'estado': 0, 'sesion': sesion,'mensaje':'La contrasena es incorrecta'})

def get_indice_usuario(nombre_usuario):
    for i in range(len(pacientes)):
        if pacientes[i].nombre_usuario == nombre_usuario:
            return i
    for i in range(len(doctores)):
        if doctores[i].nombre_usuario == nombre_usuario:
            return i
    for i in range(len(enfermeras)):
        if enfermeras[i].nombre_usuario == nombre_usuario:
            return i
    return -1


def get_nombre(nombre_usuario):
    for i in range(len(pacientes)):
        if pacientes[i].nombre_usuario == nombre_usuario:
            return pacientes[i].nombre
    for i in range(len(doctores)):
        if doctores[i].nombre_usuario == nombre_usuario:
            return doctores[i].nombre
    for i in range(len(enfermeras)):
        if enfermeras[i].nombre_usuario == nombre_usuario:
            return enfermeras[i].nombre
    return -1

def existe_usuario(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True
    global doctores
    for doctor in doctores:
        if doctor.nombre_usuario == nombre_usuario:
            return True
    global enfermeras
    for enfermera in enfermeras:
        if enfermera.nombre_usuario == nombre_usuario:
            return True
    return False

#Metodos medicamento
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
#Fin metodos medicamento

#Metodos doctor
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
#Fin metodos doctor

#Metodos enfermera
@app.route('/cargar_enfermeras', methods=['POST'])
def cargar_enfermeras():
    cuerpo = request.get_json()
    contenido = cuerpo['contenido']
    filas = contenido.split("\n")
    global enfermeras
    for fila in filas:
        print(fila)
        columnas = fila.split(",")
        enfermera = Enfermera(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6])
        enfermeras.append(enfermera)
    return jsonify({"mensaje":"Carga masiva exitosa"})

@app.route('/obtener_enfermeras', methods=['GET'])
def obtener_enfermeras():
    json_enfermeras = []
    global enfermeras
    for enfermera in enfermeras:
        json_enfermeras.append(enfermera.get_json())
    return jsonify(json_enfermeras)

@app.route('/eliminar_enfermera', methods=['POST'])
def eliminar_enfermera():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global enfermeras
    enfermeras.pop(i)
    return jsonify({"mensaje":"Eliminado exitosamente"})

@app.route('/editar_enfermera', methods=['POST'])
def editar_enfermera():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    apellido = cuerpo['apellido']
    fecha_nacimiento = cuerpo['fecha_nacimiento']
    sexo = cuerpo['sexo']
    nombre_usuario = cuerpo['nombre_usuario']
    contrasena = cuerpo['contrasena']
    telefono = cuerpo['telefono']
    i = int(indice)
    global enfermeras
    enfermeras[i].editar(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    return jsonify(enfermeras[i].get_json())
#Fin metodos enfermera

#Metodos citas
@app.route('/obtener_citas', methods=['GET'])
def obtener_citas():
    json_citas = []
    global citas
    for cita in citas:
        json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/obtener_citas_enfermera', methods=['GET'])
def obtener_citas_enfermera():
    json_citas = []
    global citas
    for cita in citas:
        if cita.estado == "Pendiente":
            json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/citas_doctor', methods=['GET'])
def citas_doctor():
    indice = request.args.get("id_doctor")
    i = int(indice)
    json_citas = []
    global citas
    for cita in citas:
        if cita.doctor == i and cita.estado=="Aceptada":
            json_citas.append(cita.get_json())
    return jsonify(json_citas)    

@app.route('/solicitar_cita', methods=['POST'])
def solicitar_cita():
    cuerpo = request.get_json()
    indice = cuerpo['id']
    fecha = cuerpo['fecha']
    hora = cuerpo['hora']
    motivo = cuerpo['motivo']
    i = int(indice)
    global citas
    citas.append(Cita(fecha,hora,motivo,i))
    return jsonify({"mensaje":"Cita creada exitosamente"})

@app.route('/rechazar_cita', methods=['POST'])
def rechazar_cita():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global citas
    citas.pop(i)
    return jsonify({"mensaje":"Se ha rechazado la cita"})
#Fin metodos citas

#Para saber si tiene cita
@app.route('/tiene_cita', methods=['GET'])
def tiene_cita():
    indice = request.args.get("id")
    global citas
    for cita in citas:
        if cita.paciente == int(indice):
            if cita.estado == "Pendiente" or cita.estado == "Aceptada":
                return jsonify({'estado':1, 'mensaje':'Tiene una cita pendiente o aceptada.', 'fecha':cita.fecha, 'hora':cita.hora,'estado_cita':cita.estado,'doctor':cita.doctor})
    return jsonify({'estado':0, 'mensaje':'No tiene citas pendientes.'})

#Facturas
@app.route('/gen_fact', methods=['POST'])
def gen_fact():
    cuerpo = request.get_json()
    doctor = cuerpo['doctor'] 
    nueva_fact = Factura(doctor)
    global facturas
    facturas.append(nueva_fact)
    return jsonify({'agregado':1,'mensaje':'Generada', 'doctor': doctor})

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)
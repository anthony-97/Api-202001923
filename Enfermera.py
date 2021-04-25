#Nombre: texto
#Apellido: texto
#Fecha de nacimiento: fecha formato dd/mm/yyyy
#Sexo: M/F
#Nombre de usuario: texto
#Contraseña: texto
#Teléfono: numero (opcional)

class Enfermera():
    def __init__(self,nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.telefono = telefono
    
    def get_json(self):
        return {
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "fecha_nacimiento" : self.fecha_nacimiento,
            "sexo": self.sexo,
            "nombre_usuario" : self.nombre_usuario,
            "contrasena" : self.contrasena,
            "telefono" : self.telefono
        }
    
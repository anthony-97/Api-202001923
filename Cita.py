class Cita():
    def __init__(self,fecha,hora,motivo,paciente):
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.paciente = paciente
        self.estado = "Pendiente"
        self.doctor = "Todavia no se ha asignado un doctor"
    
    def get_json(self):
        return {
            "fecha" : self.fecha,
            "hora" : self.hora,
            "motivo" : self.motivo,
            "paciente": self.paciente,
            "estado" : self.estado,
            "doctor" : self.doctor
        }
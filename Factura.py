class Factura():
    def __init__(self,doctor):
        self.doctor = "Todavia no se ha asignado un doctor"
    
    def get_json(self):
        return {
            "doctor" : self.doctor
        }
#Nombre: texto
#Precio: decimal
# Descripción: texto 
#Cantidad: numero 

class  Medicamento():
    def  __init__ ( self , nombre , precio , descripcion , cantidad ):
        self.nombre  =  nombre
        yo .precio  =  precio
        yo . descripcion  =  descripcion
        yo . cantidad  =  cantidad
    
    def  get_json ( yo ):
        return {
            "nombre" : self . nombre ,
            "precio" : self . precio ,
            "descripcion" : self . descripcion ,
            "cantidad" : self . cantidad
        }
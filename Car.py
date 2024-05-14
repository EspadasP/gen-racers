import utils

class Car:
    def __init__(self, coordinates):
        self.checkpoint_number = 0
        self.coordinates = coordinates
        self.prev_blue = False
        self.prev_red = False
        self.on_blue = False
        self.on_red = False

    def move_car(self, move_number): # Devuelve la coordenada donde se movera el coche en caso de aplicar el movimiento del número parametro pasado, pero no las almacena.
        last_coordinate = self.coordinates[-1]
        movements = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        return tuple(map(sum, zip(last_coordinate, movements[move_number])))
    
    def add_cordinate(self, new_coordinate): # Añade la coordenada pasada como parametro a la lista de coordenadas y actualiza si ha pasado por un checkpoint
        self.coordinates.append(new_coordinate)
        # self.on_blue = utils.on_checkpoint(self.checkpoint_blue[0], new_coordinate)
        # self.on_red = utils.on_checkpoint(self.checkpoint_red[0], new_coordinate)
        if(self.prev_blue):
            if(self.on_red):
                self.checkpoint_number+=1
        if(self.prev_red):
            if(self.on_blue):
                self.checkpoint_number-=1
        self.prev_blue=self.on_blue
        self.prev_red=self.on_red
    
    def get_position(self): # Devuelve la posicion actual
        return self.coordinates[-1]
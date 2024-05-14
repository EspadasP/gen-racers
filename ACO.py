from utils import image_to_matrix, extract_blue_checkpoints, extract_red_checkpoints, checkpoint_middle_pixel
from utils import print_map, print_checkpoints, print_track, print_coord_on_track
from utils import on_map, on_checkpoint, print_map
import numpy as np
from typing import List, Dict
import Car


MAXMOVES = 400

class ACO: GOOOOOOOOOOOO

    def __init__(self, map_path: str, blue_checkpoints_path: str, red_checkpoints_path: str, n_ants: int, alpha: float = 1, beta: float = 5, rho: float = 0.8):
        mapa = image_to_matrix(map_path)
        blue_checkpoints = extract_blue_checkpoints(blue_checkpoints_path)
        red_checkpoints = extract_red_checkpoints(red_checkpoints_path)

        print_checkpoints(blue_checkpoints)
        print_checkpoints(red_checkpoints)

        self.coord_inicial = checkpoint_middle_pixel(red_checkpoints[len(red_checkpoints)-1])
        print_coord_on_track(mapa, blue_checkpoints, red_checkpoints, self.coord_inicial)

        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.pheromone_history = []
        self.trails_history = []
        self.best_fitness_history = []


    def _evaluate(self, solution: List[int]) -> float: # implementar
        mask = np.argwhere(solution == 1).flatten() # busca los índices en la solución donde el valor es igual a 1, lo que indica que un elemento está incluido en la mochila. El resultado es un array con los índices de los elementos seleccionados.

        if np.sum(self.weights[mask]) > self.max_capacity:
            return float('-inf')

        return np.sum(self.values[mask])  


    def optimize(self, max_evaluations: int = 1000):
        
        self._initialize()

        car = ([Car(self.coord_inicial) for _ in range(self.n_ants)]) # instanciar lista de coches


        n_evaluations = 0

        while n_evaluations < max_evaluations:
            trails = []
            ant = 0

            for _ in range(self.n_ants):
                solution = self._construct_solution()
                fitness = self._evaluate(solution)
                n_evaluations += 1
                trails.append((solution, fitness))

                if fitness < self.best_fitness:
                    self.best_solution = solution
                    self.best_fitness = fitness

            self.trails_history.append(deepcopy(trails))
            self.best_fitness_history.append(self.best_fitness)
            self._update_pheromone(trails)

            print(f"Best fitness: {self.best_fitness}")

        return self.best_solution

    def _construct_solution(self) -> List[int]: 
        solution = None # Solucion inicialmente vacia

        while moves < MAXMOVES:
            candidates = self._get_candidates() # Candidatos estaticos, previa eleccion no excluyente
            pheromones = self.pheromone[candidates]**self.alpha
            heuristic = self._heuristic(candidates)**self.beta
        
            total = np.sum(pheromones * heuristic)
            probabilities = (pheromones * heuristic) / total

            selected_move = np.random.choice(candidates, p=probabilities)
            solution[selected_move] = 1
            
            new_coordinate = car[ant].move_car(selected_move)
            car[ant].add_coordinate(new_coordinate)

            moves += 1

    def _heuristic(self, candidates: List[int]) -> np.ndarray:
        return 10 / utils.min_distance_to_checkpoint(car[ant].move_car(candidates) , car[ant].checkpoint_number) # heuristica de distancia minima a siguiente checkpoint 

    def _get_candidates(self):
        '''
        funcion para generar los posibles candidatos, existen 8 posiciones
        a las que se puede mover el coche la C representa el coche, los numeros son
        la posicion a la que se movera el coche.
        012
        7C3
        654
        '''
        return np.array([0, 1, 2, 3, 4, 5, 6, 7])
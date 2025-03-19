import random
import math
from schedule import Schedule
import time

def solve(schedule: Schedule):
    """
    Algorithme de recuit simulé optimisé pour minimiser le nombre de créneaux.
    :param schedule: objet Schedule contenant les conflits.
    :return: un dictionnaire {cours: créneau}.
    """

    def generate_initial_solution():
        """Génère une solution initiale en minimisant les conflits dès l'affectation."""
        solution = {}
        available_timeslots = list(range(1, len(schedule.course_list) + 1))

        for course in random.sample(schedule.course_list, len(schedule.course_list)):
            random.shuffle(available_timeslots)
            for timeslot in available_timeslots:
                if all(solution.get(neighbor) != timeslot for neighbor in schedule.get_node_conflicts(course)):
                    solution[course] = timeslot
                    break
        return solution

    def get_neighbors(solution):
        """Génère les voisins en modifiant les créneaux des cours les plus conflictuels."""
        neighbors = []
        conflict_counts = {course: sum(1 for neighbor in schedule.get_node_conflicts(course) if solution.get(neighbor) == solution[course])
                           for course in solution}

        # Trier les cours par nombre de conflits décroissant
        sorted_courses = sorted(conflict_counts, key=conflict_counts.get, reverse=True)

        for course in sorted_courses:
            current_timeslot = solution[course]
            possible_timeslots = list(set(solution.values()) - {current_timeslot})
            random.shuffle(possible_timeslots)

            for timeslot in possible_timeslots:
                if all(solution.get(neighbor) != timeslot for neighbor in schedule.get_node_conflicts(course)):
                    neighbor_solution = solution.copy()
                    neighbor_solution[course] = timeslot
                    neighbors.append(neighbor_solution)
                    break  # Ajout d'un seul voisin viable

        return neighbors

    def evaluate(solution):
        """Évalue la solution en minimisant les créneaux tout en pénalisant les conflits."""
        penalty = sum(1 for course, timeslot in solution.items()
                      for neighbor in schedule.get_node_conflicts(course) if solution.get(neighbor) == timeslot)
        return schedule.get_n_creneaux(solution) + penalty

    def simulated_annealing(initial_solution, initial_temp, min_temp, alpha, max_iterations):
        """Algorithme de recuit simulé avec une meilleure exploration et convergence optimisée."""
        current_solution = initial_solution
        best_solution = current_solution
        best_score = evaluate(best_solution)
        temp = initial_temp

        for _ in range(max_iterations):
            neighbors = get_neighbors(current_solution)
            if not neighbors:
                break

            # Sélection d'un voisin au hasard
            neighbor = random.choice(neighbors)
            neighbor_score = evaluate(neighbor)

            # Critère d'acceptation
            if neighbor_score < best_score or random.random() < math.exp((best_score - neighbor_score) / temp):
                current_solution = neighbor
                if neighbor_score < best_score:
                    best_solution = neighbor
                    best_score = neighbor_score

            temp *= alpha  # Refroidissement exponentiel
            if temp < min_temp:
                break

        return best_solution

    start_time = time.time()

    # Paramètres ajustés pour une meilleure efficacité
    initial_temp = 5000.0
    min_temp = 0.1
    alpha = 0.998
    max_iterations = 5000

    # Recherche de la meilleure solution sur plusieurs essais
    best_solution = None
    best_score = float('inf')


    for _ in range(30):
        if time.time() - start_time >= 250:
            break
        initial_solution = generate_initial_solution()
        current_solution = simulated_annealing(initial_solution, initial_temp, min_temp, alpha, max_iterations)
        current_score = evaluate(current_solution)

        if current_score < best_score:
            best_solution = current_solution
            best_score = current_score

    return best_solution

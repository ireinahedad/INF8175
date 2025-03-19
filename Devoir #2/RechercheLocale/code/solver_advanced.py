import random
import math
import time
from schedule import Schedule

def solve(schedule: Schedule):
    """
    Algorithme de recuit simulé optimisé pour minimiser le nombre de créneaux.
    :param schedule: objet Schedule contenant les conflits.
    :return: un dictionnaire {cours: créneau}.
    """

    """
    Composantes importantes :
        1. Génération d'une solution initiale complète à améliorer petit à petit avec des mouvements locaux.
        2. Fonction de définition du voisinage (G)
        3. Fonction de définition des voisins valide (V)
        4. Fonction de sélection d'un voisin (s=Q(V,s))
        5. Fonction d'évaluation (Q(V,s))
        6. Mise à jour de la meilleure solution (s*=s)
        6. mécanisme d'échappement de minima locaux (annealing, perturbations/aléatoires/restarts)
        7. Autres modifications pour augmenter les performances (parallélisme?)
    """

    # 1. Génération d'une solution initiale complète
    def initial_greedy_solution_generator():
        """Génération d'une solution initiale gloutonne."""
        solution = {}
        courses = sorted(schedule.course_list, key=lambda c: len(schedule.get_node_conflicts(c)), reverse=True)

        # Suivre les créneaux disponibles pour chaque cours
        available_slots = {course: list(range(1, len(courses) + 1)) for course in courses}

        for course in courses:
            # Trier par le nombre de conflits
            slots_by_conflicts = sorted(available_slots[course], key=lambda slot: sum(solution.get(neigh) == slot for neigh in schedule.get_node_conflicts(course)))

            for slot in slots_by_conflicts:
                if all(solution.get(neigh) != slot for neigh in schedule.get_node_conflicts(course)):
                    solution[course] = slot
                    # Retirer ce créneau des créneaux disponibles pour les cours en conflit
                    for neigh in schedule.get_node_conflicts(course):
                        if slot in available_slots[neigh]:
                            available_slots[neigh].remove(slot)
                    break
            else:
                # Edge case: si aucun créneau n'est disponible, choisir le créneau avec le moins de conflits
                solution[course] = min(slots_by_conflicts, key=lambda slot: sum(solution.get(neigh) == slot for neigh in schedule.get_node_conflicts(course)))

        return solution

    def initial_naive_solution_generator():
        """Génération d'une solution initiale naïve."""
        solution = {}
        # Assigner un créneau différent pour chaque cours en ordre de conflits croissants
        courses = sorted(schedule.course_list, key=lambda c: len(schedule.get_node_conflicts(c)), reverse=True)
        for i, course in enumerate(courses, start=1):
            solution[course] = i
        return solution

    # 2. Fonction de définition du voisinage
    def generate_neighborhood(solution, max_neighbors=50):
        """
        Generates neighbors by moving the most conflictual courses to less conflictual time slots.
        :param solution: Current solution.
        :param schedule: Schedule object for validation.
        :param max_neighbors: Maximum number of neighbors to generate.
        :return: List of valid neighbors.
        """
        neighborhood = []

        # Identify courses with the most conflicts
        conflict_scores = {
            course: len(schedule.get_node_conflicts(course))
            for course in solution
        }

        # Sort courses by conflict score (most to least conflicting)
        sorted_courses = sorted(conflict_scores, key=conflict_scores.get, reverse=True)

        # Generate neighbors by moving most conflicting courses to less conflicting slots
        for _ in range(max_neighbors):
            # Pick a highly conflictual course
            most_conflictual = random.choice(sorted_courses[:len(sorted_courses)])

            # Find less conflictual slots
            potential_slots = list(range(1, len(solution) + 1))
            random.shuffle(potential_slots)

            # Move to a less conflictual slot
            for new_slot in potential_slots:
                if solution[most_conflictual] != new_slot:
                    neighbor = solution.copy()
                    neighbor[most_conflictual] = new_slot

                    # Validate and add the neighbor
                    try:
                        schedule.verify_solution(neighbor)
                        neighborhood.append(neighbor)
                        break  # Only add one valid neighbor per iteration
                    except AssertionError:
                        continue

        return neighborhood

    # 4. Fonction de sélection d'un voisin (probabiliste)
    def select_neighbor(neighborhood):
        """Sélectionne un voisin parmi ceux qui améliorent la solution actuelle."""
        return min(neighborhood, key=lambda n: evaluate(n))

    # 5. Fonction d'évaluation
    def evaluate(solution):
        """Évalue la qualité d'une solution en comptant le nombre de conflits."""
        conflicts = 0
        for course, slot in solution.items():
            for neighbor in schedule.get_node_conflicts(course):
                if neighbor in solution and solution[neighbor] == slot:
                    conflicts += 1
        return schedule.get_n_creneaux(solution) + conflicts

    # 7. Simulated_annealing pour tester les solutions n'ayant pas amélioré la solution actuelle
    def simulated_annealing(initial_solution, initial_temp, min_temp, alpha, max_iterations, reheat_interval):
        """Algorithme de recuit simulé."""
        current_solution = initial_solution
        current_score = evaluate(current_solution)
        best_solution = current_solution
        best_score = current_score
        temp = initial_temp
        tabu_list = []
        iterations_without_improvement = 0

        start_time = time.time()
        max_time = 290

        for i in range(max_iterations):
            if temp < min_temp or time.time() - start_time > max_time:
                print(f"Stopping at iteration {i} with temperature {temp}")
                break

            current_neighborhood = generate_neighborhood(current_solution, len(initial_solution) // 2)
            if not current_neighborhood:
                iterations_without_improvement += 1
                continue

            selected_neighbor = select_neighbor(current_neighborhood)
            neighbor_score = evaluate(selected_neighbor)

            # Metropolis criterion
            delta = neighbor_score - current_score
            metropolis_prob = math.exp(-delta / temp)
            if delta < 0 or random.random() < metropolis_prob:
                current_solution = selected_neighbor
                current_score = neighbor_score
                iterations_without_improvement = 0

            if current_score < best_score:
                best_solution = current_solution
                best_score = current_score
                print(f"New best solution found at iteration {i}: {best_score}")

            tabu_list.append(current_solution)
            if len(tabu_list) > 10:  # Limit the size of the tabu list
                tabu_list.pop(0)

            temp *= alpha

            # Reheating mechanism
            if i != 0 and i % reheat_interval == 0:
                temp = max(temp * 0.5, min_temp)  # Diminution progressive
                print(f"Reheating at iteration {i}, new temp: {temp}")

            # Early stopping criteria
            if iterations_without_improvement > 500:
                print("Early stopping due to lack of improvement.")
                break

        return best_solution

    # Sélection du générateur de solution initiale, Greedy est beaucoup plus performant comme solution initiale
    greedy = False

    if greedy:
        initial_solution = initial_greedy_solution_generator()
    else:
        initial_solution = initial_naive_solution_generator()

    best_solution = initial_solution

    best_solution = simulated_annealing(initial_solution, initial_temp=1000000, min_temp=0.001, alpha=0.999, max_iterations=100000, reheat_interval=1000)

    return best_solution

% Ireina Hedad (2213673)
% Thomas Rouleau (2221053)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre de villes à visiter + point de départ de la tournée
int: n;
 % Distance entre chaque villes (symmétrique)
array[1..n,1..n] of int: distance;
 % Distance minimale possible entre deux villes différentes
int: min_val = min([distance[i,j] | i,j in 1..n where distance[i,j] > 0]);
% Distance maximale possible entre deux villes différentes
int: max_val = max([distance[i,j] | i,j in 1..n]);

% Fenêtre de temps (1 = début, 2 = fin) durant laquelle il est possible de jouer pour chaque ville
array[1..n,1..2] of int: fenetre_arrivee;
% Temps maximum pour tout le trajet
int: max_trajet = max([fenetre_arrivee[i,2] | i in 1..n]);
% Fenêtre de temps la plus grande du trajet
int: max_fenetre = max([fenetre_arrivee[i,2] - fenetre_arrivee[i,1]| i in 2..n]);

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Ordre des villes visitées par la tournée
array[1..n] of var 1..n: chemin_tournee;
% Circuit de la tournée, circuit_tournee[i] = j => j est le successeur de i
array[1..n] of var 1..n: circuit_tournee;
% Temps cumulé lors de l'arrivé au point i de la tournée
array[1..n] of var 0..max_trajet: cumul_temps;
% Temps d'attente avant le spectacle en ville i
array[1..n] of var 0..max_fenetre: temps_attente;
% Temps d'attente total
var 0..max_trajet: total_temps_attentes = sum(temps_attente);

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Temps de trajet à minimiser
var int: temps_trajet;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%

% 1. 1ere ville = pt de départ, 1ere ville = dernière ville
% 2. chemin_tournee : [2ième ville à la dernière (=> rermine à la 1ere ville)]
% 3. Toute les villes dans le chimes sont différentes (pas de répétitions)
% 4. cumul_temps moment arrivé prochaine ville doit appartir à max_fenetre
  % Arriver en retard = interdit
  % Si arriver + tôt => possible de prendre en compte le temps d'attente avant fenetre_arrivee[i,1] pour calcul de temps_cumul
% 5. Minimiser Temps total de la tournées (minimize temps_trajet)

% Chaque point de la tournée est unique
constraint all_different(chemin_tournee);

% Contrainte pour lier chaque point de la tournée au point suivant dans l'ordre
constraint forall(i in 1..n-1) (circuit_tournee[chemin_tournee[i]] = chemin_tournee[i+1]);
constraint circuit_tournee[chemin_tournee[n]] = chemin_tournee[1];

% Contrainte pour revenir au point de départ à la fin de la tournée
constraint chemin_tournee[n] = 1;
constraint chemin_tournee[1] != 1;

% Temps cumulé pour le premier déplacement, en partant de chemin_tournee[n] vers chemin_tournee[1]
constraint cumul_temps[1] = distance[chemin_tournee[1], chemin_tournee[n]]  + temps_attente[chemin_tournee[1]];

% Contrainte pour calculer le temps cumulé à chaque étape de la tournée en prenant compte de l'ancien temps cumulé et de la distance entre les villes
constraint forall(i in 2..n) (cumul_temps[i] = cumul_temps[i-1] + distance[chemin_tournee[i], chemin_tournee[i-1]]  + temps_attente[chemin_tournee[i]]);

% Contrainte pour respecter les fenêtres d'arrivée pour chaque point de la tournée.
constraint forall(i in 1..n) (
    cumul_temps[i] >= fenetre_arrivee[chemin_tournee[i], 1] /\
    cumul_temps[i] <= fenetre_arrivee[chemin_tournee[i], 2]
);

constraint forall(i in 2..n) (cumul_temps[i] >= cumul_temps[i-1]); %Contrainte pour accélerer le calcul


% Calcul du temps total de trajet.
temps_trajet = cumul_temps[n] + distance[chemin_tournee[n-1], chemin_tournee[n]];

% Minimiser le temps cumulé pour achever la tournée
solve :: int_search(chemin_tournee, first_fail, indomain_min, complete)
      minimize cumul_temps[n];


%-----------------------------------------------------------------------------%

output [
  "Chemin de la tournée                   : \(chemin_tournee)\n",
  "Circuit de la tournée                  : \(circuit_tournee)\n",
  "Temps cumulés avant d'entrer en ville  : \(cumul_temps)\n",
  "Temps d'attente avant l'entrée en ville: \(temps_attente)\n",
  "Temps d'attente total                  : \(total_temps_attentes)\n",
  "Temps de trajet total                  : \(temps_trajet)\n",
];
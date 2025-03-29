% Ireina Hedad (2213673)
% Thomas Rouleau (2221053)

include "globals.mzn"; 

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre de tâches
int: n;
% Durée maximal du projet
int: m;
% Limite de ressources pouvant être partagées entre les tâches en cours
int: limite;

% Durée des tâches
array[1..n] of 1..m: duree_tache;
% Ressources requises par les tâches
array[1..n] of 1..m: ressource_tache;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

array[1..n] of var 1..m: debut_tache; % Début des tâches
array[1..n] of var 1..m: fin_tache; % Fin des tâches

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Fin du projet
var int: fin_projet;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
% objectif général : ordonancer les tâches sur horizon des événements, minimiser le temps avant la fin du projet (makespan)
% Calcul fin de tâches
constraint forall(i in 1..n)(
  fin_tache[i] = debut_tache[i] + duree_tache[i]
);

% Pas plus de  2 tâches démaré en même temps
constraint forall(t in 0..m)(
  sum(i in 1..n)(
    bool2int(debut_tache[i] = t)
    ) <= 2
);

% Somme des tâches // plus petite ou égal besoin énergie du projet
constraint cumulative(
  debut_tache,
  duree_tache,
  ressource_tache,
  limite  
);
% Minimiser le makespan
constraint fin_projet = max(fin_tache);
solve minimize fin_projet;

%-----------------------------------------------------------------------------%

output [
  "Envergure du projet  : ", show(fin_projet), "\n",
  "Début des tâches     : ", show(debut_tache), "\n",
  "Fin des tâches       : ", show(fin_tache), "\n",
];
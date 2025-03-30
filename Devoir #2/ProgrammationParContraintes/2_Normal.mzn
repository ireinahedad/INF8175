% Thomas Rouleau (2221053)
% Ireina Hedad (2213673)
include "globals.mzn";

%-----------------------------------------------------------------------------% 
% Données 
%-----------------------------------------------------------------------------% 

% Nombre de tâches
int: n; 
% Durée maximale du projet
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

% Début et fin des tâches
array[1..n] of var 1..m: debut_tache; 
array[1..n] of var 1..m: fin_tache; 

%-----------------------------------------------------------------------------% 
% Objectif 
%-----------------------------------------------------------------------------% 

% Fin du projet (on veut minimiser cette valeur)
var int: fin_projet; 

%-----------------------------------------------------------------------------% 
% Partie étudiant 
%-----------------------------------------------------------------------------% 

% Contrainte sur les débuts et fins des tâches
constraint forall(i, j in 1..n where i < j)(
  (debut_tache[i] + duree_tache[i] <= debut_tache[j]) \/ 
  (debut_tache[j] + duree_tache[j] <= debut_tache[i])
);

% Contrainte de capacité d'énergie: on s'assure qu'à chaque moment, la consommation d'énergie
% des tâches en cours ne dépasse pas la limite de ressources
constraint cumulative(debut_tache, duree_tache, ressource_tache, limite);

% Contrainte sur le nombre de tâches démarrées simultanément (pas plus de deux)
constraint
  forall(t in 1..m) (
    sum([ (debut_tache[i] <= t /\ t < fin_tache[i]) | i in 1..n]) <= 2
  );

% Calcul de la fin du projet: le projet se termine au moment où la dernière tâche se termine
constraint fin_projet = max([fin_tache[i] | i in 1..n]);

%-----------------------------------------------------------------------------% 
% Résolution 
%-----------------------------------------------------------------------------% 

solve minimize fin_projet; 

%-----------------------------------------------------------------------------% 
% Sortie 
%-----------------------------------------------------------------------------% 

output [
  "Envergure du projet  : ", show(fin_projet), "\n",
  "Début des tâches     : ", show(debut_tache), "\n",
  "Fin des tâches       : ", show(fin_tache), "\n"
];

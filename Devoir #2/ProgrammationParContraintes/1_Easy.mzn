% Thomas Rouleau (2221053)
% Ireina Hedad (2213673)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre d'acteurs et de rôles
int: n;
% Couleurs des costumes
enum costumes; 
% Costume demandé pour un rôle i (première dimension) par un acteur j (seconde dimension)
array[1..n,1..n] of costumes: choix_costume;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Variables de décision pour assigner un acteur à un rôle
array [1..n] of var 1..n: assignation_role;

%-----------------------------------------------------------------------------%
% Contraintes
%-----------------------------------------------------------------------------%

constraint all_different(assignation_role); % Chaque acteur a un rôle unique

% Conflit de costumes : pas deux acteurs ne doivent exiger le même costume pour un même rôle
constraint forall(i, j in 1..n where i < j)(
    assignation_role[i] = assignation_role[j] -> choix_costume[assignation_role[i], i] != choix_costume[assignation_role[j], j]
);

% Conflit d'acteurs voisins : pas de rôles adjacents pour les acteurs voisins
constraint forall(i in 1..(n-1))(
    abs(assignation_role[i] - assignation_role[i+1]) > 1
);

%-----------------------------------------------------------------------------%
% Optimisation (Pas d'objectif spécifique ici, juste satisfaction des contraintes)
%-----------------------------------------------------------------------------%

solve satisfy;

%-----------------------------------------------------------------------------%
% Sortie
%-----------------------------------------------------------------------------%

output	
  ["L'acteur " ++ show(i) ++ 
   " prendra le rôle " ++ show(assignation_role[i]) ++ 
   " (costume " ++ show(choix_costume[assignation_role[i], i]) ++ ")\n"  
  | i in 1..n];

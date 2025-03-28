% Ireina Hedad (2213673)
% Thomas Rouleau (2221053)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre d'acteurs et de rôles
int: n;
% Couleurs des costumes
enum costumes; 
% Costume démandé pour un rôle i (première dimension) par un acteur j (seconde dimension)
array[1..n,1..n] of costumes: choix_costume;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Variables de décision pour assigner un acteur à un rôle
array [1..n] of var 1..n: assignation_role;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%

% 1. Un seul acteur (colonnes) par rôles (lignes)
constraint all_different(assignation_role);

% 2. Costume demandé pour rôle choisi unique
array[1..n] of var costumes: costume_acteur; 
constraint forall(i in 1..n)(
    costume_acteur[i] = choix_costume[assignation_role[i], i]
);

% 3. aucun acteur avec rôles adjacent (diagonal, vertical ou horizontal acteurs/colonnes)
constraint forall(i in 1..n-1)(
    abs(assignation_role[i] - assignation_role[i+1]) > 1
);

% 4. Conflit de costume
constraint all_different(costume_acteur);


%-----------------------------------------------------------------------------%

output	
  ["L'acteur " ++ format(i) ++ 
   " prendra le rôle " ++ format(fix(assignation_role[i])) ++ 
   " (costume " ++ format(choix_costume[fix(assignation_role[i]), i]) ++ ")" ++"\n" 
  | i in 1..n];
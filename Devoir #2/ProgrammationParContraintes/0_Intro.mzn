% Ireina Hedad (2213673)
% Thomas Rouleau (2221053)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Nombre devant satisfaire les critères
var 1000..9999: nombre;

% Décomposition du nombre en un ensemble de chiffres
array[1..4] of var 1..9: chiffres;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Variable à minimiser
var int: p;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
% 1. Nombre pair
constraint nombre mod 2 = 0;
% 2. chiffre 0 non présent dans le nombre
% Contrainte de décomposition assurant que les chiffres en position équivalent = nombre.
% puisque chiffres est du domainre 1..9 => aucun chiffre dans nombre = 0 avece cette contrainte.
constraint nombre = 1000 * chiffres[1] + 100 * chiffres[2] + 10 * chiffres[3] + chiffres[4];

% 3. les 4 chiffres différents
constraint alldifferent(chiffres);

% 4. chiffre milliers > chiffre centaines
constraint chiffres[1] > chiffres[2];

% 5. chiffre dizaines < chiffre unités
constraint chiffres[3] < chiffres[4];

% 6. chiffre centaines > chiffre unités
constraint chiffres[2] > chiffres[4];

% 7. Somme 4 chiffres > 15
constraint sum(chiffres) > 15;

% 8. Produit 3 derniers chiffres minimisé => 
p = chiffres[2] * chiffres[3] * chiffres[4];

solve minimize p;

%-----------------------------------------------------------------------------%

output [
  show(nombre)
];


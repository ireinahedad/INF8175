% Thomas Rouleau (2221053)
% Ireina Hedad (2213673)

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

constraint nombre = chiffres[1] * 1000 + chiffres[2] * 100 + chiffres[3] * 10 + chiffres[4];
constraint all_different(chiffres); % Tous les chiffres doivent être différents
constraint nombre mod 2 = 0; % Nombre pair
constraint chiffres[1] > chiffres[2]; % Milliers > Centaines
constraint chiffres[3] < chiffres[4]; % Dizaines < Unités
constraint chiffres[2] > chiffres[4]; % Centaines > Unités
constraint sum(chiffres) > 15; % Somme des chiffres > 15

% Définition du produit des trois derniers chiffres
constraint p = chiffres[2] * chiffres[3] * chiffres[4];

%-----------------------------------------------------------------------------%
% Optimisation
%-----------------------------------------------------------------------------%

solve minimize p;

%-----------------------------------------------------------------------------%
% Sortie
%-----------------------------------------------------------------------------%

output [show(nombre)];

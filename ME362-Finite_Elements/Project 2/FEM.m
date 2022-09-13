clear all
close all
clc;

%%%%%% PRE-PROCESS %%%%%%

format long

%PD : Problem Dimension
%NPE : Number of Nodes per Element

%NoN : Number of Nodes
%VoE : Number of Elements

%NL : Node List [NoN x Pd] (Coordinates)
%EL : Element List [NoE x NPE]

%ENL : Extended Node List [NoN x (6xPD)]

%DOFs : Degrees of Freedom
%DOCs : Degrees of Constraint

%PRs : Material Properties [NoE x 2], column1 = E and column2 = A values

PRs = [10^6 0.01 0
       10^6 0.01 0
       10^6 0.01 0];
NL = [0 0; 1 0; 0.5 1];
EL = [1 2; 2 3; 1 3];
BCs = [-1 -1 0 0 0 0
        1 -1 0 0 0 0
        1  1 0 0 0 -20];

[ENL, DOFs, DOCs] = assign_BCs(NL,BCs);

K = assemble_stiffness(ENL, EL, NL, PRs);

Fp = assemble_forces(ENL, NL);

Up = assemble_displacements(ENL, NL);

Kpu = K(1:DOFs,1:DOFs);
Kpp = K(1:DOFs,DOFs+1:DOFs+DOCs);
Kuu = K(DOFs+1:DOCs+DOFs,1:DOFs);
Kup = K(DOFs+1:DOCs+DOFs,DOFs+1:DOCs+DOFs);

F = Fp - Kpp * Up;

Uu = inv(Kpu)*F;

Fu = Kuu*Uu + Kup*Up;

ENL = update_nodes(ENL,Uu,NL,Fu);

Node_flag = 'on'; %off
Element_flag = 'on'; %off

mag = 1; %magnification factor

post_process(NL, EL, ENL, PRs, Node_flag, Element_flag, mag)

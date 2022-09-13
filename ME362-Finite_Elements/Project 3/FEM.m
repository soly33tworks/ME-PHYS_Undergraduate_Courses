clear all
close all
clc;

%%%%%% PRE-PROCESS %%%%%%

format long

d1 = 1;
d2 = 1;
p = 9;
m = 9;
R = 0.2;
element_type = 'D2QU4N';%'D2TR3N' 'D2TR6N' 'D2QU4N' 'D2QU8N' 'D2QU9N'
inclusion = 0;
inclusion_type = 'circle'; %circle, square, rhombu
PR = [80/3 1/3; 4 0.3];
magnitude = 0.1;
scale = 2;

%PD : Problem Dimension
%NPE : Number of Nodes per Element

%NoN : Number of Nodes
%NoE : Number of Elements

%NL : Node List [NoN x Pd] (Coordinates)
%EL : Element List [NoE x NPE]

%ENL : Extended Node List [NoN x (6xPD)]

%DOFs : Degrees of Freedom
%DOCs : Degrees of Constraint

[NL, EL] = void_mesh(d1, d2, p, m, R, element_type, inclusion, inclusion_type);

%%%%%%%%%%%%% PROCESS %%%%%%%%%%%%%%%

BC_type = 'Shear'; % Extension, Shear, Expansion

[ENL, DOFs, DOCs] = assign_BCs(NL, BC_type, magnitude);

K = assemble_stiffness(ENL, EL, NL, PR, p, m);

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

post_process(NL, EL, ENL, PR, p, m, scale)

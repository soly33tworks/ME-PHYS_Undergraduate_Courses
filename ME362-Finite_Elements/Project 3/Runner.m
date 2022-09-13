%clc
%clear all
%close all

E = 8/3;
v = 1/3;

%x = [0 0; 2 0; 1 2];  % 3 nodes --> D2TR3N

x = [2 0; 1 2; 0 0];

%x = [0 0; 1 0; 1 1; 0 1]; % 4 nodes --> D2QU4N

%x = [2 0; 0 2; 0 0; 1 1; 0 1; 1 0]; % 6 nodes --> D2TR6N

%x = [0 0; 2 0; 2 2; 0 2; 0 1; 2 1; 1 2; 0 1]; % 8 nodes --> D2QU8N

%x = [0 0; 2 0; 2 2; 0 2; 0 1; 2 1; 1 2; 0 1; 1 1]; % 9 nodes --> D2QU9N

GPE = 1; % Gauss Points per element, (use 4 for quadrilateral better results)

Stiffness(x,GPE,E,v)


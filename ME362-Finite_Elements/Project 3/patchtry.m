% clf
% 
% X = [0;2;2;0];
% Y = [0;0;2;2];
% C = [5;1;1;1];
% 
% f1 = figure(1);
% patch(X,Y,C)
% colorbar
% colormap jet
% f2 = figure(2);
% patch(X,Y,C)
% colorbar
% colormap jet(4096)

% v = [2 4; 2 8; 8 8; 8 4; 5 0; 5 2; 8 2; 8 0];
% f = [1 2 3 4; 5 6 7 8];
% col = [0; 6; 4; 3; 3; 4; 6; 9];
% figure
% patch('Faces',f,'Vertices',v,'FaceVertexCData',col,'FaceColor','interp');
% colorbar

A = [1 2 3 4 5 6 7 8];

A1 = A(1:4)
A2 = A(5:8)
A3 = [A1(1) A2(1) A1(2) A2(2) A1(3) A2(3) A1(4) A2(4)]

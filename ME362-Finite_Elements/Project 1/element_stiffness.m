function k = element_stiffness(nl, ENL, PR)


X(1) = ENL(nl(1),1); % x coordinate of the first node of the element
Y(1) = ENL(nl(1),2); % y     "             first
X(2) = ENL(nl(2),1); % x     "             second
Y(2) = ENL(nl(2),2); % y     "             second

L = sqrt((X(1)-X(2))^2 + (Y(1)-Y(2))^2);

C = (X(2)-X(1))/L;
S = (Y(2)-Y(1))/L;

k = (PR(2)*PR(1)/L)* [C^2 C*S -C^2 -C*S
              C*S S^2 -C*S -S^2
              -C^2 -C*S C^2 C*S
              -C*S -S^2 C*S S^2];
end
function [ENL] = update_nodes(ENL, Uu, NL, Fu)
NoN = size(NL,1);
PD = size(NL,2);
DOFs = 0;
DOCs = 0;

for i = 1:NoN
    for j = 1:PD
        if ENL(i,PD+j) == 1
            
            DOFs = DOFs+1;
            ENL(i,4*PD+j) = Uu(DOFs,1);
        end
    end
end

for i = 1:NoN
    for j = 1:PD
        if ENL(i,PD+j) == -1
            
            DOCs = DOCs +1;
            ENL(i,5*PD+j) = Fu(DOCs,1);
        end
    end
end

end
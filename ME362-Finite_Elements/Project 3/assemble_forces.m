function [Fp] = assemble_forces(ENL, NL)

NoN = size(NL,1);
PD = size(NL,2);

DOF = 0;
%Fp = zeros(NoN, PD);

for i = 1:NoN
    for j = 1:PD
        if ENL(i,PD+j) == 1
            
            DOF = DOF +1;
            Fp(DOF,1) = ENL(i,5*PD+j);
            
        end
    end
end

end
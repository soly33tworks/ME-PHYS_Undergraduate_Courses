function [ENL , DOFs, DOCs] = assign_BCs(NL,BCs)


NoN = size(NL,1); % Number of Nodes
PD = size(NL,2); % Problem Dimension

ENL = zeros(NoN,PD*6);

ENL(:,1:2) = NL; % Coordinates

for i = 1 : NoN
    ENL(i,3) = BCs(i,1); % BC type of x
    ENL(i,4) = BCs(i,2); % BC type of y
    
    ENL(i,9) = BCs(i,3); % Prescribed (OR unknown) Disp. of x
    ENL(i,10) = BCs(i,4); % Prescribed (OR unknown) Disp. of y
    
    ENL(i,11) = BCs(i,5); % Prescribed (OR unknown) Force of x
    ENL(i,12) = BCs(i,6); % Prescribed (OR unknown) Force of y
end

DOFs = 0;
DOCs = 0;
       
for i = 1:NoN
    
    for j = 1:PD
        
        if (ENL(i,(PD+j)) == -1)
            
            DOCs = DOCs - 1;
            ENL(i,2*PD+j) = DOCs;
            
        else
            
            DOFs = DOFs + 1;
            ENL(i,2*PD+j) = DOFs;
        end
    end
end

for i = 1:NoN
    
    for j = 1:PD
    
        if (ENL(i,(2*PD+j))<0)
            
            ENL(i,PD*3+j) = DOFs + abs(ENL(i,(2*PD+j)));
            
        else
            
            ENL(i,PD*3+j) = ENL(i,(2*PD+j));
            
        end
    end
end

DOCs = abs(DOCs);

end
    
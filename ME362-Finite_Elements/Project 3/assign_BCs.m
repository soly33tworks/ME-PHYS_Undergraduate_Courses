function [ENL , DOFs, DOCs] = assign_BCs(NL, BC_type, mag)

NoN = size(NL,1); % Number of Nodes
PD = size(NL,2); %Problem Dimension

ENL = zeros(NoN,PD*6);

ENL(:,1:PD) = NL; %Coordinates

switch BC_type
    case 'Extension'
        
        for i = 1 : NoN
            
            if ENL(i,1) == 0
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = -mag;
                ENL(i,4*PD+2) = 0;
                
            elseif ENL(i,1) == 1 % The x coordinate of right side (maybe max(NL(:,1)) will work, or "a")
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag;
                ENL(i,4*PD+2) = 0;
            
            else
                
                ENL(i,PD+1) = 1;
                ENL(i,PD+2) = 1;
                
                ENL(i,4*PD+1) = 0;
                ENL(i,4*PD+2) = 0;
            end
        end
    
        
    case 'Expansion'
        
        for i = 1 : NoN
            
            if ENL(i,1) == 0
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag*ENL(i,1);
                ENL(i,4*PD+2) = mag*ENL(i,2);
                
            elseif ENL(i,1) == 1 % The x coordinate of right side
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag*ENL(i,1);
                ENL(i,4*PD+2) = mag*ENL(i,2);
                
            elseif ENL(i,2) == 0
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag*ENL(i,1);
                ENL(i,4*PD+2) = mag*ENL(i,2);
                
            elseif ENL(i,2) == 1 % The y coordinate of right side
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag*ENL(i,1);
                ENL(i,4*PD+2) = mag*ENL(i,2);
                
            else
                
                ENL(i,PD+1) = 1;
                ENL(i,PD+2) = 1;
                
                ENL(i,4*PD+1) = 0;
                ENL(i,4*PD+2) = 0;
            end
        end
        
    case 'Shear'
        
        for i = 1 : NoN
            
            if ENL(i,2) == 0
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = 0;
                ENL(i,4*PD+2) = 0;
                
            elseif ENL(i,2) == 1 % The y coordinate of right side
                
                ENL(i,PD+1) = -1;
                ENL(i,PD+2) = -1;
                
                ENL(i,4*PD+1) = mag;
                ENL(i,4*PD+2) = 0;
                
            else
                
                ENL(i,PD+1) = 1;
                ENL(i,PD+2) = 1;
                
                ENL(i,4*PD+1) = 0;
                ENL(i,4*PD+2) = 0;
            end
        end

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
    
      
        
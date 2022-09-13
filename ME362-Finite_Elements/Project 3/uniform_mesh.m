function [NL, EL] = uniform_mesh(d1, d2, p, m, element_type)

PD = 2;

q = [0 0; d1 0; 0 d2; d1 d2];

NoN = (p+1)*(m+1);

NoE = p*m;

NPE = 4;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Nodes   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

NL = zeros(NoN, PD);

a = d1/p;
b = d2/m;

n=1;

for i = 1:m+1
    
   for j = 1:p+1
       
       NL(n,1) = q(1,1) + (j-1)*a;
       NL(n,2) = q(1,2) + (i-1)*b;
       n = n+1;
       
   end
   
end
       

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Elements   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       
EL = zeros(NoE, NPE);

for i = 1:m
    
    for j = 1:p
        
        if j == 1
            
            EL((i-1)*p+j,1) = (i-1)*(p+1)+j;
            EL((i-1)*p+j,2) = EL((i-1)*p+j,1) + 1;
            EL((i-1)*p+j,4) = EL((i-1)*p+j,1) + (p+1);
            EL((i-1)*p+j,3) = EL((i-1)*p+j,4) + 1;
            
        else
            
            EL((i-1)*p+j,1) = EL((i-1)*p+j-1,2);
            EL((i-1)*p+j,4) = EL((i-1)*p+j-1,3);
            EL((i-1)*p+j,2) = EL((i-1)*p+j,1) + 1;
            EL((i-1)*p+j,3) = EL((i-1)*p+j,4) + 1;
            
        end
        
    end
    
end

if isequal(element_type, 'D2TR3N')
    
    NPE_new = 3;
    EL_new = zeros(2*NoE, NPE_new);
    
    for i = 1:NoE
        
        EL_new(2*(i-1)+1,1) = EL(i,1); % Lower triangle
        EL_new(2*(i-1)+1,2) = EL(i,2);
        EL_new(2*(i-1)+1,3) = EL(i,3);
        
        EL_new(2*(i-1)+2,1) = EL(i,1); % Upper triangle
        EL_new(2*(i-1)+2,2) = EL(i,3);
        EL_new(2*(i-1)+2,3) = EL(i,4);
        
    end
    
    EL = EL_new;
    
end

end
        
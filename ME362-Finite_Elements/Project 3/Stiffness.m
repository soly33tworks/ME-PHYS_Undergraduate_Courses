function output = Stiffness(x, GPE, E, v)

    NPE = size(x,1);
    PD = size(x,2);
    
    coor = x';
    if (NPE == 4)||(NPE == 8)||(NPE == 9)
        factor = 1;
    else
        factor = 1/2;
    end

    K = zeros(NPE*PD, NPE*PD); % Stiffness of each element
    
    for i=1:NPE
        
        for j=1:NPE
            
            k = zeros(PD,PD);
            
            for gp = 1:GPE
                
                J = zeros(PD, PD); % Jacobian
                
                grad = zeros(PD, NPE);
                
                [xi, eta, alpha] = GaussPoint(NPE, GPE, gp);
                
                grad_nat = grad_N_nat(NPE, xi, eta);
                
                J = coor * grad_nat';
                
                grad = inv(J)' * grad_nat;
                
                for a = 1:PD
                    for c = 1:PD
                        for b = 1:PD
                            for d = 1:PD
                                k(a,c) = k(a,c) + grad(b,i) * constitutive(a,b,c,d, E, v) * grad(d,j) * det(J)*alpha*factor;  %factor = 1/2 for triangular
                            end
                        end
                    end
                end
                
            end
            
            K(((i-1)*PD+1):i*PD, ((j-1)*PD+1):j*PD) = k;
            
        end
        
    end
        
    output = K;
    
end
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function result = grad_N_nat(NPE, xi, eta)

    PD = 2;
    
    result = zeros(PD,NPE);
    
    if (NPE == 3)
        
        result(1,1) = 1;
        result(1,2) = 0;
        result(1,3) = -1;
        
        result(2,1) = 0;
        result(2,2) = 1;
        result(2,3) = -1;
    
    elseif (NPE == 6)
        
        result(1,1) = -1+4*xi;
        result(1,2) =  0;
        result(1,3) =  -3+4*xi+4*eta;
        result(1,4) =  4*eta;
        result(1,5) =  -4*eta;
        result(1,6) =  -4*(-1+eta+2*xi);
        
        result(2,1) =  0;
        result(2,2) =  -1+4*eta;
        result(2,3) =  -3+4*xi+4*eta;
        result(2,4) =  4*xi;
        result(2,5) =  -4*(-1+2*eta+xi);
        result(2,6) =  -4*xi;
        
    elseif (NPE == 4)
        
        result(1,1) = -1/4*(1-eta);
        result(1,2) =  1/4*(1-eta);
        result(1,3) =  1/4*(1+eta);
        result(1,4) = -1/4*(1+eta);
        
        result(2,1) = -1/4*(1-xi);
        result(2,2) = -1/4*(1+xi);
        result(2,3) =  1/4*(1+xi);
        result(2,4) =  1/4*(1-xi);
        
    elseif (NPE == 8)
        
        result(1,1) =  1/4*(1-eta)*(2*xi+eta);
        result(1,2) =  1/4*(1-eta)*(2*xi-eta);
        result(1,3) =  1/4*(1+eta)*(2*xi+eta);
        result(1,4) =  1/4*(1+eta)*(2*xi-eta);
        result(1,5) =  -xi*(1-eta);
        result(1,6) =  1/2*(1-eta)*(1+eta);
        result(1,7) =  -xi*(1+eta);
        result(1,8) = -1/2*(1-eta)*(1+eta);
        
        result(2,1) =  1/4*(1-xi)*(xi+2*eta);
        result(2,2) =  1/4*(1+xi)*(-xi+2*eta);
        result(2,3) =  1/4*(1+xi)*(xi+2*eta);
        result(2,4) =  1/4*(1-xi)*(-xi+2*eta);
        result(2,5) = -1/2*(1-xi)*(1+xi);
        result(2,6) = -eta*(1+xi);
        result(2,7) =  1/2*(1-xi)*(1+xi);
        result(2,8) =  -eta*(1-xi);
        
    elseif (NPE == 9)
        
        result(1,1) =  1/4*(1-2*xi)*(1-eta)*eta;
        result(1,2) = -1/4*(1+2*xi)*(1-eta)*eta;
        result(1,3) =  1/4*(1+2*xi)*(1+eta)*eta;
        result(1,4) = -1/4*(1-2*xi)*(1+eta)*eta;
        result(1,5) =  xi*eta*(1-eta);
        result(1,6) =  1/2*(1+2*xi)*(1-eta)*(1+eta);
        result(1,7) =  -xi*eta*(1+eta);
        result(1,8) = -1/2*(1-2*xi)*(1-eta)*(1+eta);
        result(1,9) = -2*xi*(1-eta)*(1+eta);
        
        result(2,1) =  1/4*(1-xi)*xi*(1-2*eta);
        result(2,2) = -1/4*(1+xi)*xi*(1-2*eta);
        result(2,3) =  1/4*(1+xi)*xi*(1+2*eta);
        result(2,4) = -1/4*(1-xi)*xi*(1+2*eta);
        result(2,5) =  1/2*(1-xi)*(1+xi)*(2*eta-1);
        result(2,6) =  -xi*eta*(1+xi);
        result(2,7) =  1/2*(1-xi)*(1+xi)*(2*eta+1);
        result(2,8) =  xi*eta*(1-xi);
        result(2,9) =  -2*eta*(1-xi)*(1+xi);
        
    end
    
end
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [xi, eta, alpha] = GaussPoint(NPE, GPE, gp)

    if (NPE == 4)||(NPE == 8)||(NPE == 9)
        if (GPE == 1)
            
            xi = 0; eta = 0; alpha = 4;
            
        elseif (GPE == 4)
            
            if (gp == 1)
                xi = -1/sqrt(3); eta = -1/sqrt(3); alpha = 1;
            elseif(gp == 2)
                xi = 1/sqrt(3); eta = -1/sqrt(3); alpha = 1;
            elseif(gp == 3)
                xi = 1/sqrt(3); eta = 1/sqrt(3); alpha = 1;
            elseif(gp == 4)
                xi = -1/sqrt(3); eta = 1/sqrt(3); alpha = 1;
            end
        
        elseif (GPE == 9)
            
            if (gp == 1)
                xi = -sqrt(3/5); eta = -sqrt(3/5); alpha = 25/81;
            elseif(gp == 2)
                xi = sqrt(3/5); eta = -sqrt(3/5); alpha = 25/81;
            elseif(gp == 3)
                xi = sqrt(3/5); eta = sqrt(3/5); alpha = 25/81;
            elseif(gp == 4)
                xi = -sqrt(3/5); eta = sqrt(3/5); alpha = 25/81;
            elseif(gp == 5)
                xi = 0; eta = -sqrt(3/5); alpha = 40/81;
            elseif(gp == 6)
                xi = sqrt(3/5); eta = 0; alpha = 40/81;
            elseif(gp == 7)
                xi = 0; eta = sqrt(3/5); alpha = 40/81;
            elseif(gp == 8)
                xi = -sqrt(3/5); eta = 0; alpha = 40/81;
            elseif(gp == 9)
                xi = 0; eta = 0; alpha = 64/81;
            end
            
        end
    end
    
    if (NPE == 3)||(NPE == 6)
        
        if (GPE == 1)
            
            xi = 1/3; eta = 1/3; alpha = 1;
            
        elseif (GPE == 3)
            
            if (gp == 1)
                xi = 1/6; eta = 1/6; alpha = 1/3;
            elseif(gp == 2)
                xi = 4/6; eta = 1/6; alpha = 1/3;
            elseif(gp == 3)
                xi = 1/6; eta = 4/6; alpha = 1/3;
            end
            
        end
        
    end
    
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function C = constitutive(i,j,k,l, E, nu)

    C = (E/(2*(1+nu))) * (delta(i,l)*delta(j,k) + delta(i,k)*delta(j,l)) + ((E*nu)/(1-nu^2)) * (delta(i,j)*delta(k,l));
              
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function delta = delta(i,j)

    if (i == j)
        delta = 1;
    else
        delta = 0;
    end
    
end
                
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                              
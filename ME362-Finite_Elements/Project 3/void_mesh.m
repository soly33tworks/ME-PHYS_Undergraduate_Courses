function [NL, EL] = void_mesh(d1, d2, p, m, R, element_type, inc, inclusion_type)

q = [0 0; d1 0; 0 d2; d1 d2];

if inclusion_type == 'circle'
    q_inc = [d1/2-R/4 d2/2-R/4; d1/2+R/4 d2/2-R/4; d1/2-R/4 d2/2+R/4; d1/2+R/4 d2/2+R/4];
    a_i = R/(2*p);
else
    a_i = R/(4*p);
    q_inc = [d1/2-R/8 d2/2-R/8; d1/2+R/8 d2/2-R/8; d1/2-R/8 d2/2+R/8; d1/2+R/8 d2/2+R/8];
end

gamma = pi/4; % Angle of the rhombus inclusion

PD = 2;

if inc
    NoN = 2*(p+1)*(2*m+1) + 2*(p-1)*(2*m+1) + (p-1)^2;
    NoE = 8*p*m+p^2;
    
else
    NoN = 2*(p+1)*(m+1) + 2*(p-1)*(m+1);
    NoE = 4*p*m;
end


NPE = 4;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Nodes   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

NL = zeros(NoN, PD);

a = d1/p;
b = d2/p;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Region 1  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if inc
    coor11 = zeros((p+1)*(2*m+1), PD);
else
    coor11 = zeros((p+1)*(m+1), PD);
end


for i = 1:p+1
    
    coor11(i,1) = q(1,1) + (i-1)*a;
    coor11(i,2) = q(1,2);
    
end

for i = 1:p+1
    
    if inclusion_type == 'circle'
        coor11(m*(p+1)+i,1) = R*cos((5*pi/4) + (i-1)*(pi/2)/p) + (d1/2);
        coor11(m*(p+1)+i,2) = R*sin((5*pi/4) + (i-1)*(pi/2)/p) + (d2/2);
    
    elseif inclusion_type == 'square'
        coor11(m*(p+1)+i,1) = (R/p)*(i-1) + (d1/2) - R/2;
        coor11(m*(p+1)+i,2) = -R/2 + (d2/2);
        
    elseif inclusion_type == 'rhombu'
        coor11(m*(p+1)+i,1) = (R/(2*sqrt(2)))*(2*((i-1)/p)-1) + (d1/2);
        coor11(m*(p+1)+i,2) = tan(gamma)*abs((R/(2*sqrt(2)))*(2*((i-1)/p)-1)) - R*sin(gamma) + (d2/2);    
    end
end

%%%% DEBUGGING PLOT %%%%
% for i = 1:(p+1)*(m+1)
%     hold on;
%     plot(coor11(i,1),coor11(i,2),'o','MarkerSize',30, 'MarkerEdgeColor','k','MarkerFaceColor',[0,0,1])
%     text(coor11(i,1),coor11(i,2), num2str(i), 'Color','w','FontSize',20,'HorizontalAlignment','center')
% end
% 
% axis equal

for i = 1:m-1
    
    for j = 1:p+1
        
        dx = (coor11(m*(p+1)+j,1) - coor11(j,1))/m;
        dy = (coor11(m*(p+1)+j,2) - coor11(j,2))/m;
        
        coor11(i*(p+1)+j,1) = coor11(((i-1)*(p+1))+j,1) + dx;
        coor11(i*(p+1)+j,2) = coor11(((i-1)*(p+1))+j,2) + dy;
        
    end
    
end

if inc
    for i = ((p+1)*(2*m)+1):(p+1)*(2*m+1)
        
        coor11(i,1) = q_inc(1,1) + (i-1-(p+1)*(2*m))*(a_i);
        coor11(i,2) = q_inc(1,2);
        
    end
    
    for i = m+1:2*m-1
        
        for j = 1:p+1
            
            dx = (coor11(2*m*(p+1)+j,1) - coor11(m*(p+1)+j,1))/m;
            dy = (coor11(2*m*(p+1)+j,2) - coor11(m*(p+1)+j,2))/m;
            
            coor11(i*(p+1)+j,1) = coor11(((i-1)*(p+1))+j,1) + dx;
            coor11(i*(p+1)+j,2) = coor11(((i-1)*(p+1))+j,2) + dy;
            
        end
        
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Region 2  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if inc
    coor22 = zeros((p+1)*(2*m+1), PD);
else
    coor22 = zeros((p+1)*(m+1), PD);
end

for i = 1:p+1
    
    coor22(i,1) = q(3,1) + (i-1)*a;
    coor22(i,2) = q(3,2);
    
end

for i = 1:p+1
    
    if inclusion_type == 'circle'
        coor22(m*(p+1)+i,1) = R*cos((3*pi/4) - (i-1)*(pi/2)/p) + (d1/2);
        coor22(m*(p+1)+i,2) = R*sin((3*pi/4) - (i-1)*(pi/2)/p) + (d2/2);
    
    elseif inclusion_type == 'square'
        coor22(m*(p+1)+i,1) = (R/p)*(i-1) + (d1/2) - R/2;
        coor22(m*(p+1)+i,2) = R/2 + (d2/2);
        
    elseif inclusion_type == 'rhombu'
        coor22(m*(p+1)+i,1) = (R/(2*sqrt(2)))*(2*((i-1)/p)-1) + (d1/2);
        coor22(m*(p+1)+i,2) = -tan(gamma)*abs((R/(2*sqrt(2)))*(2*((i-1)/p)-1)) + R*sin(gamma) + (d2/2);  
    end
end


for i = 1:m-1
    
    for j = 1:p+1
        
        dx = (coor22(m*(p+1)+j,1) - coor22(j,1))/m;
        dy = (coor22(m*(p+1)+j,2) - coor22(j,2))/m;
        
        coor22(i*(p+1)+j,1) = coor22(((i-1)*(p+1))+j,1) + dx;
        coor22(i*(p+1)+j,2) = coor22(((i-1)*(p+1))+j,2) + dy;
        
    end
    
end
   

if inc
    for i = ((p+1)*(2*m)+1):(p+1)*(2*m+1)
        
        coor22(i,1) = q_inc(3,1) + (i-1-(p+1)*(2*m))*(a_i);
        coor22(i,2) = q_inc(3,2);
        
    end
    
    for i = m+1:2*m-1
        
        for j = 1:p+1
            
            dx = (coor22(2*m*(p+1)+j,1) - coor22(m*(p+1)+j,1))/m;
            dy = (coor22(2*m*(p+1)+j,2) - coor22(m*(p+1)+j,2))/m;
            
            coor22(i*(p+1)+j,1) = coor22(((i-1)*(p+1))+j,1) + dx;
            coor22(i*(p+1)+j,2) = coor22(((i-1)*(p+1))+j,2) + dy;
            
        end
        
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Region 3  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if inc
    coor33 = zeros((p-1)*(2*m+1), PD);
else
    coor33 = zeros((p-1)*(m+1), PD);
end


for i = 1:p-1
    
    coor33(i,1) = q(1,1);
    coor33(i,2) = q(1,2) + (i)*b;
    
end


for i = 1:p-1
    
    if inclusion_type == 'circle'
        coor33(m*(p-1)+i,1) = R*cos((5*pi/4) - (i)*(pi/2)/p) + (d1/2);
        coor33(m*(p-1)+i,2) = R*sin((5*pi/4) - (i)*(pi/2)/p) + (d2/2);
    
    elseif inclusion_type == 'square'
        coor33(m*(p-1)+i,1) = -R/2 + (d1/2);
        coor33(m*(p-1)+i,2) = (R/p)*(i) + (d2/2) - R/2;
        
    elseif inclusion_type == 'rhombu'
        coor33(m*(p-1)+i,2) = (R/(2*sqrt(2)))*(((2*i)/p)-1) + (d1/2);
        coor33(m*(p-1)+i,1) = tan(gamma)*abs((R/(2*sqrt(2)))*(((2*i)/p)-1)) - R*sin(gamma) + (d2/2);
    end
end

for i = 1:m-1
    
    for j = 1:p-1
        
        dx = (coor33(m*(p-1)+j,1) - coor33(j,1))/m;
        dy = (coor33(m*(p-1)+j,2) - coor33(j,2))/m;
        
        coor33(i*(p-1)+j,1) = coor33(((i-1)*(p-1))+j,1) + dx;
        coor33(i*(p-1)+j,2) = coor33(((i-1)*(p-1))+j,2) + dy;
        
    end
    
end

if inc
    for i = ((p-1)*(2*m)+1):(p-1)*(2*m+1)
        
        coor33(i,1) = q_inc(1,1);
        coor33(i,2) = q_inc(1,2) + (i-(p-1)*(2*m))*(a_i);
        
    end
    
    for i = m+1:2*m-1
        
        for j = 1:p-1
            
            dx = (coor33(2*m*(p-1)+j,1) - coor33(m*(p-1)+j,1))/m;
            dy = (coor33(2*m*(p-1)+j,2) - coor33(m*(p-1)+j,2))/m;
            
            coor33(i*(p-1)+j,1) = coor33(((i-1)*(p-1))+j,1) + dx;
            coor33(i*(p-1)+j,2) = coor33(((i-1)*(p-1))+j,2) + dy;
            
        end
        
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Region 4  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if inc
    coor44 = zeros((p-1)*(2*m+1), PD);
else
    coor44 = zeros((p-1)*(m+1), PD);
end


for i = 1:p-1
    
    coor44(i,1) = q(2,1);
    coor44(i,2) = q(2,2) + (i)*b;
    
end

for i = 1:p-1
    
    coor44(m*(p-1)+i,1) = R*cos((7*pi/4) + (i)*(pi/2)/p) + (d1/2);
    coor44(m*(p-1)+i,2) = R*sin((7*pi/4) + (i)*(pi/2)/p) + (d2/2);
    
end

for i = 1:p-1
    
    if inclusion_type == 'circle'
        coor44(m*(p-1)+i,1) = R*cos((7*pi/4) + (i)*(pi/2)/p) + (d1/2);
        coor44(m*(p-1)+i,2) = R*sin((7*pi/4) + (i)*(pi/2)/p) + (d2/2);
    
    elseif inclusion_type == 'square'
        coor44(m*(p-1)+i,1) = R/2 + (d1/2);
        coor44(m*(p-1)+i,2) = (R/p)*(i) + (d2/2) - R/2;
        
    elseif inclusion_type == 'rhombu'
        coor44(m*(p-1)+i,2) = (R/(2*sqrt(2)))*(((2*i)/p)-1) + (d1/2);
        coor44(m*(p-1)+i,1) = -tan(gamma)*abs((R/(2*sqrt(2)))*(((2*i)/p)-1)) + R*sin(gamma) + (d2/2);
    end
end

for i = 1:m-1
    
    for j = 1:p-1
        
        dx = (coor44(m*(p-1)+j,1) - coor44(j,1))/m;
        dy = (coor44(m*(p-1)+j,2) - coor44(j,2))/m;
        
        coor44(i*(p-1)+j,1) = coor44(((i-1)*(p-1))+j,1) + dx;
        coor44(i*(p-1)+j,2) = coor44(((i-1)*(p-1))+j,2) + dy;
        
    end
    
end

if inc
    for i = ((p-1)*(2*m)+1):(p-1)*(2*m+1)
        
        coor44(i,1) = q_inc(2,1);
        coor44(i,2) = q_inc(2,2) + (i-(p-1)*(2*m))*(a_i);
        
    end
    
    for i = m+1:2*m-1
        
        for j = 1:p-1
            
            dx = (coor44(2*m*(p-1)+j,1) - coor44(m*(p-1)+j,1))/m;
            dy = (coor44(2*m*(p-1)+j,2) - coor44(m*(p-1)+j,2))/m;
            
            coor44(i*(p-1)+j,1) = coor44(((i-1)*(p-1))+j,1) + dx;
            coor44(i*(p-1)+j,2) = coor44(((i-1)*(p-1))+j,2) + dy;
            
        end
        
    end
end


for i = 1:(1+inc)*m+1 % 2m+1 if there is inclusion, m+1 without inclusion
    
    NL((i-1)*4*p+1:(i)*4*p,:) = [coor11((i-1)*(p+1)+1:(i)*(p+1),:);
                                 coor44((i-1)*(p-1)+1:(i)*(p-1),:);
                                 flipud(coor22((i-1)*(p+1)+1:(i)*(p+1),:));
                                 flipud(coor33((i-1)*(p-1)+1:(i)*(p-1),:))];
    
end


if inc
    n=2*(p+1)*(2*m+1) + 2*(p-1)*(2*m+1); % Number of nodes up to now (without the inner square bit)

    for i = 1:p-1
        for j = 1:p-1
            
            NL(n+1,1) = q_inc(1,1) + (j)*a_i;
            NL(n+1,2) = q_inc(1,2) + (i)*a_i;
            n = n+1;
        end
        
    end
    
end

NoN = size(NL,1);

% for i = 1:size(NL,1)
%     hold on;
%     plot(NL(i,1),NL(i,2),'o','MarkerSize',15,'MarkerEdgeColor','k','MarkerFaceColor',[0,0,1])
%     text(NL(i,1),NL(i,2),num2str(i),'Color','w','FontSize',12,'HorizontalAlignment','center')
% end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Elements   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

EL = zeros(NoE, NPE);

for i = 1:m*(1+inc) % 2m if there is inclusion, m without inclusion
    
    for j = 1:4*p
        
        if j == 1
            
            EL((i-1)*(4*p)+j,1) = (i-1)*(4*p) + 1;
            EL((i-1)*(4*p)+j,2) = EL((i-1)*(4*p)+j,1) + 1;
            EL((i-1)*(4*p)+j,4) = EL((i-1)*(4*p)+j,1) + 4*p;
            EL((i-1)*(4*p)+j,3) = EL((i-1)*(4*p)+j,4) + 1;
            
        elseif j == 4*p
            
            EL((i-1)*(4*p)+j,1) = (i)*(4*p);
            EL((i-1)*(4*p)+j,2) = (i-1)*(4*p) + 1;
            EL((i-1)*(4*p)+j,3) = EL((i-1)*(4*p)+j,1) + 1;
            EL((i-1)*(4*p)+j,4) = EL((i-1)*(4*p)+j,1) + 4*p;
            
        else
            
            EL((i-1)*(4*p)+j,1) = EL((i-1)*(4*p)+j-1,2);
            EL((i-1)*(4*p)+j,4) = EL((i-1)*(4*p)+j-1,3);
            EL((i-1)*(4*p)+j,3) = EL((i-1)*(4*p)+j,4) + 1;
            EL((i-1)*(4*p)+j,2) = EL((i-1)*(4*p)+j,1) + 1;
            
        end
    end
end

if inc
    n=8*p*m; % Number of elements up to now
    NN = 2*(p+1)*(2*m+1) + 2*(p-1)*(2*m+1) - p*4 + 1; % Node number of the down-left corner
    
    for i = 1:p
        for j = 1:p
            
            if (i == 1)&&(j == 1)
                EL((i-1)*p+j+n,1) = NN;
                EL((i-1)*p+j+n,2) = NN+1;
                EL((i-1)*p+j+n,4) = NN+4*p-1;
                EL((i-1)*p+j+n,3) = NN+4*p;
            elseif (i == 1)&&(j == p)
                EL((i-1)*p+j+n,1) = NN+p-1;
                EL((i-1)*p+j+n,2) = NN+p;
                EL((i-1)*p+j+n,4) = NN+4*p+(p-2);
                EL((i-1)*p+j+n,3) = NN+p+1;
            elseif (j == 1)&&(i == p)
                EL((i-1)*p+j+n,1) = NN+3*p+1;
                EL((i-1)*p+j+n,2) = NoN-(p-2);
                EL((i-1)*p+j+n,4) = NN+3*p;
                EL((i-1)*p+j+n,3) = NN+3*p-1;
            elseif (j == p)&&(i == p) 
                EL((i-1)*p+j+n,1) = NoN;
                EL((i-1)*p+j+n,2) = NN+2*p-1;
                EL((i-1)*p+j+n,4) = NN+2*p+1;
                EL((i-1)*p+j+n,3) = NN+2*p;
            
            elseif i==1
                EL((i-1)*p+j+n,1) = NN+j-1;
                EL((i-1)*p+j+n,2) = NN+j;
                EL((i-1)*p+j+n,4) = NN+4*p-2+j;
                EL((i-1)*p+j+n,3) = NN+4*p-1+j;
            elseif i==p
                EL((i-1)*p+j+n,1) = NoN-(p-2)-2+j;
                EL((i-1)*p+j+n,2) = NoN-(p-2)-1+j;
                EL((i-1)*p+j+n,4) = NN+3*p+1-j;
                EL((i-1)*p+j+n,3) = NN+3*p-j;
            elseif j == 1
                EL((i-1)*p+j+n,1) = NN+4*p+1-i;
                EL((i-1)*p+j+n,2) = NN+4*p+(p-1)*(i-2);
                EL((i-1)*p+j+n,4) = EL((i-1)*p+j+n,1) - 1;
                EL((i-1)*p+j+n,3) = EL((i-1)*p+j+n,2) + (p-1);
            elseif j == p
                EL((i-1)*p+j+n,1) = NN+4*p+(p-2)+(p-1)*(i-2);
                EL((i-1)*p+j+n,2) = NN+p-1+i;
                EL((i-1)*p+j+n,4) = EL((i-1)*p+j+n,1) + (p-1);
                EL((i-1)*p+j+n,3) = EL((i-1)*p+j+n,2) + 1;
            else
                
                EL((i-1)*p+j+n,1) = EL((i-1)*p+j-1+n,2);
                EL((i-1)*p+j+n,4) = EL((i-1)*p+j-1+n,3);
                EL((i-1)*p+j+n,2) = EL((i-1)*p+j+n,1) + 1;
                EL((i-1)*p+j+n,3) = EL((i-1)*p+j+n,4) + 1;
                
            end
            
        end
    end
    
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if isequal(element_type,'D2QU8N')
    
    New_Nodes = zeros(4*NoE, PD);
    for e = 1:NoE
        New_Nodes(5*(e-1)+1,1) = 0.5*(NL(EL(e,1),1) + NL(EL(e,2),1));
        New_Nodes(5*(e-1)+1,2) = 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2));
        
        New_Nodes(5*(e-1)+2,1) = 0.5*(NL(EL(e,2),1) + NL(EL(e,3),1));
        New_Nodes(5*(e-1)+2,2) = 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2));
        
        New_Nodes(5*(e-1)+3,1) = 0.5*(NL(EL(e,3),1) + NL(EL(e,4),1));
        New_Nodes(5*(e-1)+3,2) = 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2));
        
        New_Nodes(5*(e-1)+4,1) = 0.5*(NL(EL(e,4),1) + NL(EL(e,1),1));
        New_Nodes(5*(e-1)+4,2) = 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2));

    end
    
    New_Nodes = unique(New_Nodes,'rows');
    
    NL = [NL; New_Nodes];
    NoN_new = size(NL,1);
    NPE_new = 8;
    EL_new = [EL zeros(NoE,4)];

    for e = 1:NoE
        c5 = [0.5*(NL(EL(e,1),1) + NL(EL(e,2),1)), 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2))];
        c6 = [0.5*(NL(EL(e,2),1) + NL(EL(e,3),1)), 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2))];
        c7 = [0.5*(NL(EL(e,3),1) + NL(EL(e,4),1)), 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2))];
        c8 = [0.5*(NL(EL(e,4),1) + NL(EL(e,1),1)), 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2))];
        
        for i = NoN+1:NoN_new
            if ismember(NL(i,:),c5,'rows')
                EL_new(e,5) = i;
            end
            if ismember(NL(i,:),c6,'rows')
                EL_new(e,6) = i;
            end
            if ismember(NL(i,:),c7,'rows')
                EL_new(e,7) = i;
            end
            if ismember(NL(i,:),c8,'rows')
                EL_new(e,8) = i;
            end     
        end
        
    end
    
    EL = EL_new;
    NoN = NoN_new;
    
end

if isequal(element_type,'D2QU9N')
    
    New_Nodes = zeros(5*NoE, PD);
    for e = 1:NoE
        New_Nodes(5*(e-1)+1,1) = 0.5*(NL(EL(e,1),1) + NL(EL(e,2),1));
        New_Nodes(5*(e-1)+1,2) = 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2));
        
        New_Nodes(5*(e-1)+2,1) = 0.5*(NL(EL(e,2),1) + NL(EL(e,3),1));
        New_Nodes(5*(e-1)+2,2) = 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2));
        
        New_Nodes(5*(e-1)+3,1) = 0.5*(NL(EL(e,3),1) + NL(EL(e,4),1));
        New_Nodes(5*(e-1)+3,2) = 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2));
        
        New_Nodes(5*(e-1)+4,1) = 0.5*(NL(EL(e,4),1) + NL(EL(e,1),1));
        New_Nodes(5*(e-1)+4,2) = 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2));
        
        New_Nodes(5*(e-1)+5,1) = 0.25*(NL(EL(e,1),1) + NL(EL(e,2),1) + NL(EL(e,3),1) + NL(EL(e,4),1));
        New_Nodes(5*(e-1)+5,2) = 0.25*(NL(EL(e,1),2) + NL(EL(e,2),2) + NL(EL(e,3),2) + NL(EL(e,4),2));
    end
    
    New_Nodes = unique(New_Nodes,'rows');
    
    NL = [NL; New_Nodes];
    NoN_new = size(NL,1);
    NPE_new = 9;
    EL_new = [EL zeros(NoE,5)];

    for e = 1:NoE
        c5 = [0.5*(NL(EL(e,1),1) + NL(EL(e,2),1)), 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2))];
        c6 = [0.5*(NL(EL(e,2),1) + NL(EL(e,3),1)), 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2))];
        c7 = [0.5*(NL(EL(e,3),1) + NL(EL(e,4),1)), 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2))];
        c8 = [0.5*(NL(EL(e,4),1) + NL(EL(e,1),1)), 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2))];
        c9 = [0.25*(NL(EL(e,1),1) + NL(EL(e,2),1) + NL(EL(e,3),1) + NL(EL(e,4),1)), 0.25*(NL(EL(e,1),2) + NL(EL(e,2),2) + NL(EL(e,3),2) + NL(EL(e,4),2))];
        
        for i = NoN+1:NoN_new
            if ismember(NL(i,:),c5,'rows')
                EL_new(e,5) = i;
            end
            if ismember(NL(i,:),c6,'rows')
                EL_new(e,6) = i;
            end
            if ismember(NL(i,:),c7,'rows')
                EL_new(e,7) = i;
            end
            if ismember(NL(i,:),c8,'rows')
                EL_new(e,8) = i;
            end     
            if ismember(NL(i,:),c9,'rows')
                EL_new(e,9) = i;
            end
        end
        
    end
    
    EL = EL_new;
    NoN = NoN_new;
    
end

if isequal(element_type,'D2TR3N')

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

if isequal(element_type,'D2TR6N')
    
    New_Nodes = zeros(5*NoE, PD);
    for e = 1:NoE
        New_Nodes(5*(e-1)+1,1) = 0.5*(NL(EL(e,1),1) + NL(EL(e,2),1));
        New_Nodes(5*(e-1)+1,2) = 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2));
        
        New_Nodes(5*(e-1)+2,1) = 0.5*(NL(EL(e,2),1) + NL(EL(e,3),1));
        New_Nodes(5*(e-1)+2,2) = 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2));
        
        New_Nodes(5*(e-1)+3,1) = 0.5*(NL(EL(e,3),1) + NL(EL(e,4),1));
        New_Nodes(5*(e-1)+3,2) = 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2));
        
        New_Nodes(5*(e-1)+4,1) = 0.5*(NL(EL(e,4),1) + NL(EL(e,1),1));
        New_Nodes(5*(e-1)+4,2) = 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2));
        
        New_Nodes(5*(e-1)+5,1) = 0.5*(NL(EL(e,1),1) + NL(EL(e,3),1));
        New_Nodes(5*(e-1)+5,2) = 0.5*(NL(EL(e,1),2) + NL(EL(e,3),2));
    end
    
    New_Nodes = unique(New_Nodes,'rows');
    
    NL = [NL; New_Nodes];
    NoN_new = size(NL,1);
    NPE_new = 9;
    EL_new = [EL zeros(NoE,5)];
    
    for e = 1:NoE
        c5 = [0.5*(NL(EL(e,1),1) + NL(EL(e,2),1)), 0.5*(NL(EL(e,1),2) + NL(EL(e,2),2))];
        c6 = [0.5*(NL(EL(e,2),1) + NL(EL(e,3),1)), 0.5*(NL(EL(e,2),2) + NL(EL(e,3),2))];
        c7 = [0.5*(NL(EL(e,3),1) + NL(EL(e,4),1)), 0.5*(NL(EL(e,3),2) + NL(EL(e,4),2))];
        c8 = [0.5*(NL(EL(e,4),1) + NL(EL(e,1),1)), 0.5*(NL(EL(e,4),2) + NL(EL(e,1),2))];
        c9 = [0.5*(NL(EL(e,1),1) + NL(EL(e,3),1)), 0.5*(NL(EL(e,1),2) + NL(EL(e,3),2))];
        
        for i = NoN+1:NoN_new
            if ismember(NL(i,:),c5,'rows')
                EL_new(e,5) = i;
            end
            if ismember(NL(i,:),c6,'rows')
                EL_new(e,6) = i;
            end
            if ismember(NL(i,:),c7,'rows')
                EL_new(e,7) = i;
            end
            if ismember(NL(i,:),c8,'rows')
                EL_new(e,8) = i;
            end
            if ismember(NL(i,:),c9,'rows')
                EL_new(e,9) = i;
            end
        end
        
    end
    
    EL = EL_new;
    NoN = NoN_new;
    
    NPE_new = 6;
    EL_new = zeros(2*NoE, NPE_new);
    
    for i = 1:NoE
        
        EL_new(2*(i-1)+1,1) = EL(i,1); % Lower triangle
        EL_new(2*(i-1)+1,2) = EL(i,2);
        EL_new(2*(i-1)+1,3) = EL(i,3);
        EL_new(2*(i-1)+1,4) = EL(i,5);
        EL_new(2*(i-1)+1,5) = EL(i,6);
        EL_new(2*(i-1)+1,6) = EL(i,9);
        
        EL_new(2*(i-1)+2,1) = EL(i,3); % Upper triangle
        EL_new(2*(i-1)+2,2) = EL(i,4);
        EL_new(2*(i-1)+2,3) = EL(i,1);
        EL_new(2*(i-1)+2,4) = EL(i,7);
        EL_new(2*(i-1)+2,5) = EL(i,8);
        EL_new(2*(i-1)+2,6) = EL(i,9);
    end
    
    EL = EL_new;
    
end

end

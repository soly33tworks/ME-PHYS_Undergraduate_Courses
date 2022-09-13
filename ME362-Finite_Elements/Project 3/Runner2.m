clc;
clear all;
clf;

d1 = 1;
d2 = 1;
p = 3;
m = 4;
element_type = 'D2QU4N'; %'D2TR3N' 'D2TR6N' 'D2QU4N' 'D2QU8N' 'D2QU9N'
inclusion_type = 'circle'; %circle, square, rhombu
inclusion = 1;
R = 0.2;  % Radius of the circular void


%[NL, EL] = uniform_mesh(d1, d2, p, m, element_type);
[NL, EL] = void_mesh(d1, d2, p, m, R, element_type,inclusion, inclusion_type);


%%%%%%%


NoN = size(NL,1);
NoE = size(EL,1);
NPE = size(EL,2);

switch element_type
    case {'D2TR3N', 'D2TR6N'}
        
        for i = 1:NoE
            hold on;
            plot([NL(EL(i,1),1), NL(EL(i,2),1)], [NL(EL(i,1),2), NL(EL(i,2),2)],'m');
            plot([NL(EL(i,2),1), NL(EL(i,3),1)], [NL(EL(i,2),2), NL(EL(i,3),2)],'m');
            plot([NL(EL(i,3),1), NL(EL(i,1),1)], [NL(EL(i,3),2), NL(EL(i,1),2)],'m');
            x = (NL(EL(i,1),1) + NL(EL(i,2),1) + NL(EL(i,3),1))/3;
            y = (NL(EL(i,1),2) + NL(EL(i,2),2) + NL(EL(i,3),2))/3;
            text(x,y,num2str(i), 'Color', 'k', 'FontSize', 12, 'HorizontalAlignment','center')
        end
        
        for i = 1:NoN
            hold on;
            plot(NL(i,1),NL(i,2),'o','MarkerSize',15, 'MarkerEdgeColor','k','MarkerFaceColor',[0,0,1])
            text(NL(i,1),NL(i,2), num2str(i), 'Color','w','FontSize',12,'HorizontalAlignment','center')
        end
        
        axis equal
        
    case {'D2QU4N', 'D2QU8N', 'D2QU9N'}
        
        for i = 1:NoE
            hold on;
            plot([NL(EL(i,1),1), NL(EL(i,2),1)], [NL(EL(i,1),2), NL(EL(i,2),2)],'m');
            plot([NL(EL(i,2),1), NL(EL(i,3),1)], [NL(EL(i,2),2), NL(EL(i,3),2)],'m');
            plot([NL(EL(i,3),1), NL(EL(i,4),1)], [NL(EL(i,3),2), NL(EL(i,4),2)],'m');
            plot([NL(EL(i,4),1), NL(EL(i,1),1)], [NL(EL(i,4),2), NL(EL(i,1),2)],'m');
            x = (NL(EL(i,1),1) + NL(EL(i,2),1) + NL(EL(i,3),1) + NL(EL(i,4),1))/4;
            y = (NL(EL(i,1),2) + NL(EL(i,2),2) + NL(EL(i,3),2) + NL(EL(i,4),2))/4;
            text(x,y,num2str(i), 'Color', 'k', 'FontSize', 12, 'HorizontalAlignment','center')
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        for i = 1:NoN
            hold on;
            plot(NL(i,1),NL(i,2),'o','MarkerSize',15,'MarkerEdgeColor','k','MarkerFaceColor',[0,0,1])
            text(NL(i,1),NL(i,2),num2str(i),'Color','w','FontSize',12,'HorizontalAlignment','center')
        end
        
        axis equal
        
end


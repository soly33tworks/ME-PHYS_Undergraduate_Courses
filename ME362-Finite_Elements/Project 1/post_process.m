function post_process(NL, EL, ENL, PRs, Node_flag, Element_flag, mag)

NoN = size(NL,1);
NoE = size(EL,1);

%%%%%%%%%%%%%%%%% draw the undeformed configuration %%%%%%%%%%%%%%%%%%%%

% axis equal
hold on
% plot elements
for i = 1: NoE
    H=plot([NL(EL(i,1),1),NL(EL(i,2),1)], [NL(EL(i,1),2),NL(EL(i,2),2)], 'LineWidth',3,'Color','k');
    H.Color(4)=0.2;
end

% plot nodes
for i = 1 : NoN
    plot(NL(i,1),NL(i,2),'o','MarkerSize',20,'MarkerEdgeColor','k','MarkerFaceColor','r')
end

%%%%%%%%%%%%%%%% draw the deformed configuration %%%%%%%%%%%%%%%%%%%%%%%

colorMap = jet; %get multiple choices (e.g. winter, copper, cool)
colormap(colorMap);

%%%%%%%%%%% plot elements with stress distribution %%%%%%%%%%%%%%%%%%%%%

for i = 1 : NoE
    
    x = [ENL(EL(i,1),1)+mag*ENL(EL(i,1),9) ENL(EL(i,2),1)+mag*ENL(EL(i,2),9)];
    y = [ENL(EL(i,1),2)+mag*ENL(EL(i,1),10) ENL(EL(i,2),2)+mag*ENL(EL(i,2),10)];
    z = zeros(size(x));
    sigma = PRs(i,1) * (sqrt((ENL(EL(i,1),9)-ENL(EL(i,2),9))^2 + (ENL(EL(i,1),10)-ENL(EL(i,2),10))^2)...
    /(sqrt((ENL(EL(i,1),1)-ENL(EL(i,2),1))^2 + (ENL(EL(i,1),2)-ENL(EL(i,2),2))^2)));
    
    col = [sigma sigma];
    figure(1)
    surface([x;x],[y;y],[z;z],[col;col],'facecol','no','edgecol','interp','linew',4);
end

axis equal
colorbar

%%%%%%%%%%%%%%%%%%%%% plot elements with displacement distribution%%%%%%%%%
%SIMILAR PROCESS, BUT THE DISPLACEMENT DISTRIBUTION WILL NOT BE CONSTANT

%%%%%%%%%%%%%%%%%%%%%% Plot Element numbers and symbol %%%%%%%%%%%%%%%%%%%%%

if isequal(Element_flag,'on')
    
    for i = 1 : NoE
        
        plot((ENL(EL(i,1),1)+mag*ENL(EL(i,1),9)+ENL(EL(i,2),1)+mag*ENL(EL(i,2),9))/2, (ENL(EL(i,1),2)+mag*ENL(EL(i,1),10)+ENL(EL(i,2),2)+mag*ENL(EL(i,2),10))/2,'o','MarkerSize',16,'MarkerEdgeColor','k','MarkerFaceColor',[1,1,0])
        text((ENL(EL(i,1),1)+mag*ENL(EL(i,1),9)+ENL(EL(i,2),1)+mag*ENL(EL(i,2),9))/2, (ENL(EL(i,1),2)+mag*ENL(EL(i,1),10)+ENL(EL(i,2),2)+mag*ENL(EL(i,2),10))/2,num2str(i),'Color','k','FontSize',12,'HorizontalAlignment','center')
    end
end

%%%%%%%%%%%%%%%%%%%% Plot Nodes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i = 1 : NoN
    
    plot(ENL(i,1)+mag*ENL(i,9),ENL(i,2)+mag*ENL(i,10),'o','MarkerSize',16,'MarkerEdgeColor','k','MarkerFaceColor',[0,0.7,0.9])
end

%%%%%%%%%%%%%%%%% Plot Node Numbers %%%%%%%%%%%%%%%%%%%%%%%%%%%%

if isequal(Node_flag,'on')
    
    for i = 1:NoN
        
        text(ENL(i,1)+mag*ENL(i,9),ENL(i,2)+mag*ENL(i,10),num2str(i),'Color','k','FontSize',12,'HorizontalAlignment','center')
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

hold off

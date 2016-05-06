function x = analysis(delta, b,e, noshow)

% predicting the temperature in the room from delta to the end. 

%% data extraction
[time_vector, data_matrix] = data_out(b,e); % extracting data

appart = data_matrix(:,1);
outside = data_matrix(:,2);
room = data_matrix(:,3);
heater_state = data_matrix(:,4);
t_delta = size(data_matrix,1);
fts = 14;

data = zeros(t_delta - delta,4);
for t = 1 : t_delta - delta
    t_actual = room(t);
    appart_room = appart(t) - t_actual;
    outside_room = sum(outside(t:t+delta)-t_actual)/1000;
    heater_percent = sum(heater_state(t:t+delta))/delta;
    data(t,:) = [t_actual, outside_room, appart_room, heater_percent];
end
x0 = [0,0,0];

%% curve fitting
% x = lsqcurvefit(fun,x0,xdata,ydata)
% computing min_x (fun(xdata) - ydata)^2
x = lsqcurvefit(@thermo,x0,data,room(delta+1:end));
%x = [0.320613288390638,-0.0960586089151054,2.03608732460974]
%% plotting
if ~noshow
    figure
    hold on;
    t_predicted = thermo(x,data);
    plot(time_vector(delta:end),room(delta:end),'r-')
    plot(time_vector(delta+1:end),t_predicted(1:end),'b-')
    %plot(time_vector(delta:end),heater_state(delta:end),'g-')
    h_legend = legend('Temperature from sensor',['Temperature predicted ~',num2str(delta),' minutes before'])%,'Heater on/off')
    set(gca,'FontSize',fts-3)
    set(h_legend,'FontSize',14);
    title('Room temperature','FontSize', fts)
    ylabel('Temperature [°C]','FontSize', fts)
    xlabel('Time','FontSize', fts)
    l = axis
    axis([l(1), l(2), 15,30])
    dif = -room(delta+1:end)+thermo(x,data);
    prc = prctile(dif,90)
    avg = mean(abs(dif))
    mean_diff = median(abs(dif))


    figure
    histogram(-room(delta+1:end)+thermo(x,data),21,'Normalization', 'probability' )
            set(gca,'FontSize',fts-3)
    title(['Histogram of the error for a ',num2str(delta),' minutes prediction'],'FontSize', fts)
    xlabel('< 0 => too cold','FontSize', fts)
    ylabel('Percentage of error','FontSize', fts)
end
end

function fun = thermo(p,data_line)
% return the predicted temperature of the room at time t + delta
room_at_t = data_line(:,1); % room temperature a time t
outside_room_diff = data_line(:,2); % integral over the difference of temperature between the outside and the room 
appart_room_diff = data_line(:,3); % integral over the difference of temperature between the outside and the room 
heater = data_line(:,4); % percentage of delta on

fun = room_at_t + p(1) * appart_room_diff + p(2) * outside_room_diff + p(3) * heater;

end


function [ avg, mean_diff ] = ab()
%UNTITLED Summary of this a goes here
%   Detailed explanation goes here
%% data extraction
b = datetime(2016,3,11,0,0,0);
e = datetime(2016,3,19,11,59,59);
for i = 1 : 7
    lul(i,:) = [num2str(i),' days of training'];
end
fts = 14
figure('Position',[100,100,600,750]); 
subplot(2,1,2) , hold on;
set(gca,'FontSize',fts-3)
title('Median error','FontSize', fts)
xlabel('Time to prediction','FontSize', fts)
ylabel('Error in °C','FontSize', fts)

subplot(2,1,1), hold on;
set(gca,'FontSize',fts-3)
title('Mean error','FontSize', fts)
xlabel('Time to prediction','FontSize', fts)
ylabel('Error in °C','FontSize', fts)

for i = 7:-1:1
    x_mat = analysis_delta(300,b+days(i),e);
    [time_vector, data_matrix] = data_out(b,e); % extracting data

    appart = data_matrix(:,1);
    outside = data_matrix(:,2);
    room = data_matrix(:,3);
    heater_state = data_matrix(:,4);
    t_delta = size(data_matrix,1);





    n = size(x_mat,1);
    avg = zeros(n,1);
    median_diff = zeros(n,1);
    for i = 1 : n
        delta = 5*i;
        data = zeros(t_delta - delta,4);
        for t = 1 : t_delta - delta
            t_actual = room(t);
            appart_room = appart(t) - t_actual;
            outside_room = sum(outside(t:t+delta)-t_actual)/1000;
            heater_percent = sum(heater_state(t:t+delta))/delta;
            data(t,:) = [t_actual, outside_room, appart_room, heater_percent];
        end
        x= x_mat(i,:);
        %% plotting

        dif = room(delta+1:end)-thermo(x,data);
        avg(i,1) = mean(abs(dif));
        median_diff(i,1) = median(abs(dif));


    end

    subplot(2,1,1), hold on;
    plot((1:n)*5, avg)

    subplot(2,1,2), hold on;
    plot((1:n)*5, median_diff)
    
    



end

subplot(2,1,2) , hold on;
h_legend = legend(lul)
set(h_legend,'FontSize',12);
subplot(2,1,1), hold on;
h_legend = legend(lul)
set(h_legend,'FontSize',12);
function fun = thermo(p,data_line)
% return the predicted temperature of the room at time t + delta
room_at_t = data_line(:,1); % room temperature a time t
outside_room_diff = data_line(:,2); % integral over the difference of temperature between the outside and the room 
appart_room_diff = data_line(:,3); % integral over the difference of temperature between the outside and the room 
heater = data_line(:,4); % percentage of delta on

fun = room_at_t + p(1) * appart_room_diff + p(2) * outside_room_diff + p(3) * heater;

end

end


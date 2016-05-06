function [] = data_plot(begin_date,  end_date )
% plot the temperature between datetime value b and e
% begin_date and end_date are datetime value
% for example : datetime(2016,2,27,0,0,0),datetime(2016,4,20,23,59,59)
fts = 15;
if end_date <= begin_date
    print 'error, end date earlier that begin';
end

load ('data.mat');
load ('date_time.mat');

[~, b_index] = min(abs(dateAndTime-begin_date)); %index of closest value
[~, e_index] = min(abs(dateAndTime-end_date));

figure('Position',[100,100,600,600]); 
positionVector1 = [0.08, 0.35, 0.9, 0.6];
subplot('Position',positionVector1);hold on;
set(gca,'FontSize',fts-4)
title('Temperature traces','FontSize', fts)
xlabel('Time','FontSize', fts)
ylabel('Temperature [°C]','FontSize', fts)
axis([-inf inf 0 30])

for i = 1 : 4
    if i == 4
        positionVector2 = [0.08, 0.1, 0.9, 0.15];
        subplot('Position',positionVector2)
        plot(dateAndTime(b_index:e_index), data(b_index:e_index,i),'r','LineWidth',2);
        set(gca,'FontSize',fts-4)
        legend('Heater state','FontSize', fts)
        xlabel('Time','FontSize', fts)
        ylabel('On/Off = 1/0','FontSize', fts)
    else
        plot(dateAndTime(b_index:e_index), data(b_index:e_index,i),'LineWidth',3);

        h_legend = legend('Appartment','Outside','Room','FontSize', fts);
    end


end
set(h_legend,'FontSize',14);
figure

plot(dateAndTime(b_index:e_index), data(b_index:e_index,5)/1000,'LineWidth',2);
set(gca,'FontSize',fts-3)
xlabel('Time','FontSize', fts)
ylabel('Power [W]','FontSize', fts)
title('Heater event','FontSize', fts)

end


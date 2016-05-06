b = 82350;%46710
e = 84060;%48870
b2 = 84061;%42390
e2 = 90650;%44550



mean_out_2 = mean([data(b:e,2);data(b2:e2,2)]);
std_out_2 = std([data(b:e,2);data(b2:e2,2)]);
median_out_2 = median([data(b:e,2);data(b2:e2,2)]);



energy_tot_mJ = sum((data(b:e,5)+3000)*60)+ sum((data(b2:e2,5)+3000)*60);
energy_tot_kJ= energy_tot_mJ/1000/1000;
h = (e-b+e2-b2)/60;
h_on=(sum(data(b:e,4))+sum(data(b2:e2,4)))/60;




power_w = energy_tot_kJ/h_on/3600*1000
cons_kwh = energy_tot_kJ/3600;
cons_day_kwh = cons_kwh/h*24


b = 42390;
e = 44550;
b2 = 46710;
e2 = 48870;




mean_out = mean([data(b:e,2);data(b2:e2,2)]);
std_out = std([data(b:e,2);data(b2:e2,2)]);
median_out = median([data(b:e,2);data(b2:e2,2)]);

disp([num2str(mean_out),' vs ',num2str(mean_out_2)])
disp([num2str(std_out),' vs ',num2str(std_out_2)])
disp([num2str(median_out),' vs ',num2str(median_out_2)])
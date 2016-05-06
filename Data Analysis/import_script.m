% script importing all the 6 data column in data 
% appartment, outside, room, state, actual_power, total_power
% import the time vector  in dateAndTime
import_matlab_data
% dateAndTime;appartment;outside;room;state;actual_power;total_power
data = [appartment, outside,room,state,actual_power,total_power];
save 'data.mat' data;
save 'date_time.mat' dateAndTime;


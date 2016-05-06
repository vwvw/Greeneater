function [ date_time_i, data_i ] = data_out(  begin_date,  end_date )
% output the temperature between datetime value b and e. Time vector and
% temperature
% begin_date and end_date are datetime value
% for example : datetime(2016,2,27,0,0,0),datetime(2016,4,20,23,59,59)

if end_date <= begin_date
    print 'error, end date earlier that begin';
end


load ('data.mat');
load ('date_time.mat');
[~, b_index] = min(abs(dateAndTime-begin_date)); %index of closest value
[~, e_index] = min(abs(dateAndTime-end_date));
date_time_i = dateAndTime(b_index:e_index);
data_i = data(b_index:e_index,:);
end


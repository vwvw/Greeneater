function [ minute ] = dateTime_to_min_interval( dt )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
minute = zeros(size(dt));
d = diff(dt);
for i = 2 : length(d)+1;
   [h,m,s] = hms(d(i-1));
   minute(i) = s+60*(m+60*h);
end
minute = minute/60;
histogram(minute);
moyenne = mean(minute)
media = median(minute)
maximum =max(minute)
minimum = min (minute)
end


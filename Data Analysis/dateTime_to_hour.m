function [ min ] = dateTime_to_hour( dt )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
min = zeros(size(dt));
d = diff(dt);
for i = 2 : length(d)+1;
   [h,m,s] = hms(d(i-1));
   min(i) = min(i-1)+s+60*(m+60*h);
end
min = min/3600;
end


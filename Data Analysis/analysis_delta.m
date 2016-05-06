function x = analysis_delta (delta_max, b,e)

if delta_max < 10
   disp('delta_max too small');
   return;
end
x = zeros(1,3);
for delta = 5 : 5 : delta_max
    x = [x;analysis(delta, b,e, true)];
end
x = x(2:end,:);
end


clear all; close; clc;

R_serie = @(t) 1 - (1 - exp(-400.*t)).^3;
R_parallelo = @(t) (1 - (1 - exp(-100.*t)).^3).^4;

tempi = linspace(0,3/100);

figure;
plot(tempi,R_serie(tempi)); hold on;
plot(tempi,R_parallelo(tempi));
legend('R_{serie}','R_{parallelo}');
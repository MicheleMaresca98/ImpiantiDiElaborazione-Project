clear all; close; clc;

R_coverage = @(t,c) exp(-(53.*t)./11250).*((2.*exp(t./60000) - 1).^2).*(2.*exp(t./4500) - 1).*(4.*exp(t./2000) - 6.*exp(t./1000) + 3.*exp((3.*t)./2000) + exp((7.*t)/2000) - 1).*(c.*exp(t./10000) - c + exp(t./10000));
f = @(c) R_coverage(1,c);
a = 0;
b = 1;
target = 0.99999;
m = b - (b - a) / 2;
n = 0;
res = f(m);

while res ~= target && n < 1000
     if res < target
         a = m;
         m = b - (b - a) / 2;
     else
         b = m;
         m = b - (b - a) / 2;
     end
     res = f(m);
     n = n + 1;
end

c = m;
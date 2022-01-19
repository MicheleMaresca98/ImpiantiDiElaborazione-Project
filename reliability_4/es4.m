clear all; close; clc;

lambda_a = 1/1000;
lambda_b = 1/9000;
lambda_c = 1/2000;

Ra = @(x) exp(-lambda_a.*x);
Rb = @(x) exp(-lambda_b.*x);
Rc = @(x) exp(-lambda_c.*x);

R1a = @(t) Ra(t).*Rc(t) + Ra(t).*Rb(t) - (Ra(t).^2).*Rb(t).*Rc(t);
R1b = @(t) Ra(t).*Rb(t) + Ra(t).*Rc(t) - Ra(t).*Rb(t).*Rc(t);
R2a = @(t) Ra(t).*Rb(t) +  Ra(t).^2 - (Ra(t).^2).*Rb(t);
R2b = @(t) Ra(t);
R3a = @(t) Ra(t).*(Rb(t).^2) +  (Ra(t).^2).*Rb(t) -  (Ra(t).*Rb(t)).^2;
R3b = @(t) Ra(t).*Rb(t); 
R4a = @(t) Ra(t).*Rb(t) + Ra(t) - (Ra(t).^2).*Rb(t); 
R4b = @(t) Ra(t);

tempi = linspace(0,7000);

MTTF = zeros(4,2);
MTTF(1,1) = 1/(lambda_a+lambda_c) + 1/(lambda_a + lambda_b) - 1/(2*lambda_a+lambda_b+lambda_c);
MTTF(1,2) = 1/(lambda_a+lambda_b) + 1/(lambda_a+lambda_c) - 1/(lambda_a + lambda_b + lambda_c);
MTTF(2,1) = 1/(lambda_a+lambda_b) + 1/(2*lambda_a) - 1/(2*lambda_a+lambda_b);
MTTF(2,2) = 1/lambda_a;
MTTF(3,1) = 1/(lambda_a + 2*lambda_b) + 1/(lambda_b + 2*lambda_a) - 1/(lambda_b + 2*lambda_a);
MTTF(3,2) = 1/(lambda_a + lambda_b);
MTTF(4,1) = 1/(lambda_a + lambda_b) + 1/lambda_a - 1/(lambda_b + 2*lambda_a);
MTTF(4,2) = 1/lambda_a;


figure;
subplot(2,2,1);plot(tempi,R1a(tempi));hold on;plot(tempi,R1b(tempi));legend('R1a','R1b');
subplot(2,2,2);plot(tempi,R2a(tempi));hold on;plot(tempi,R2b(tempi));legend('R2a','R2b');
subplot(2,2,3);plot(tempi,R3a(tempi));hold on;plot(tempi,R3b(tempi));legend('R3a','R3b');
subplot(2,2,4);plot(tempi,R4a(tempi));hold on;plot(tempi,R4b(tempi));legend('R4a','R4b');

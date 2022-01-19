clear; clc; close all;
r1 = table2array(readtable("risultati_fisso.csv"));
r2 = table2array(readtable("risultati_portatile.csv"));
r1 = r1(:, 2);
r2 = r2(:, 2);
[h, p] = ttest(r1, r2);
 

function [C,Cg,Cr] = harris(img_blue,img_green,img_red)
fsize = 5;
sigma = 0.5;
%% for BLUE
[Ix, Iy] = imgradientxy(img_blue);
Ix2 = imgaussfilt(Ix.^2, 2);
Iy2 = imgaussfilt( Iy.^2, 2);
IxIy = imgaussfilt(Ix .* Iy, 2);
% Compute cornerness
det = Ix2.*Iy2 - IxIy.^2;
trace = (Ix2 + Iy2).^2;
alpha = 0.02;
Har = det - (alpha * trace);
corner_k = 0.01; % cornerness threshold
Har__ = (Har == max(Har)) & (Har > corner_k);
[x,y] = find(Har__ == 1);
C = cat(2,x,y);
C = C(1:200,:);
%% for green
[Ix_G, Iy_G] = imgradientxy(img_green);
Ix2_G = imgaussfilt(Ix_G.^2, 2);
Iy2_G = imgaussfilt( Iy_G.^2, 2);
IxIy_G = imgaussfilt(Ix_G .* Iy_G, 2);
% Compute cornerness
det_G = Ix2_G.*Iy2_G - IxIy_G.^2;
trace_G = (Ix2_G + Iy2_G).^2;
% Harris is det(H) - a * trace(H) 
Har_G = det_G - (alpha * trace_G);
Har__G = (Har_G == max(Har_G)) & (Har_G > corner_k);
[x_G,y_G] = find(Har__G == 1);
Cg = cat(2,x_G,y_G);
Cg = Cg(1:200,:);
%% RED
[Ix_R, Iy_R] = imgradientxy(img_red);
f = fspecial('gaussian', fsize, sigma);
Ix2_R = imgaussfilt(Ix_R.^2, 2);
Iy2_R = imgaussfilt( Iy_R.^2, 2);
IxIy_R = imgaussfilt(Ix_R .* Iy_R, 2);
% Compute cornerness
det_R = Ix2_R.*Iy2_R - IxIy_R.^2;
trace_R = (Ix2_R + Iy2_R).^2;
% Harris is det(H) - a * trace(H) 
Har_R = det_R - (alpha * trace_R);
Har__R = (Har_R == max(Har_R)) & (Har_R > corner_k);
[x_R,y_R] = find(Har__R == 1);

Cr = cat(2,x_R,y_R);
Cr = Cr(1:200,:);
end

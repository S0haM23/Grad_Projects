function C = im_align3(img_blue,img_green,img_red,C,Cg,Cr)

%% RANSAC
shift_listX = [];
shift_listY = [];
inlier_list = [];

for z = 1:5000
X = randi(length(C),1:2); 
A = (C(X(1),:));
Aa = (Cr(X(2),:));
shift = A-Aa;
C_shift = Cr+shift;
inliers=0;
for i = 1:200
    x_R= C_shift(i,1)-1;    y_R=C_shift(i,2)-1;
    X_R=C_shift(i,1)+1;    Y_R=C_shift(i,2)+1 ;
    [row,~] = find(C(:,1)>=x_R & C(:,1)<=X_R & C(:,2)>=y_R & C(:,2)<=Y_R);% creates a window to search for inliers
    if ~isempty(row)
        inliers = inliers+1;
    end
end
    inlier_list(end+1) = inliers;
    shift_listX(end+1) = shift(1);
    shift_listY(end+1) = shift(2);
end
max_index = find(inlier_list==max(inlier_list(:)));
x_red = shift_listX(max_index);
y_red = shift_listY(max_index);
%%
shift_listX_G = [];
shift_listY_G = [];
inlier_list_G = [];

for o = 1:5000
X = randi(length(C),1:2);
A = (C(X(1),:));
Aa = (Cg(X(2),:));
shift = A-Aa;
C_shift_G = Cg+shift;
inliers=0;
for i = 1:200
    x_G = C_shift_G(i,1)-1;    y_G=C_shift_G(i,2)-1;
    X_G=C_shift_G(i,1)+1;    Y_G=C_shift_G(i,2)+1 ;
    [row,~] = find(C(:,1)>=x_G & C(:,1)<=X_G & C(:,2)>=y_G & C(:,2)<=Y_G);
    if ~isempty(row)
        inliers = inliers+1;
    end
end
    inlier_list_G(end+1) = inliers;
    shift_listX_G(end+1) = shift(1);
    shift_listY_G(end+1) = shift(2);
end
max_index_G = find(inlier_list_G==max(inlier_list_G(:)));
x_green = shift_listX_G(max_index_G);
y_green = shift_listY_G(max_index_G);
RR = circshift(img_red,[x_red(1) y_red(1)]);
fprintf('Harris Red Offsets : %i , %i \n',x_red(1),y_red(1))
fprintf('Harris Green Offsets : %i , %i \n',x_green(1),y_green(1))
GG = circshift(img_green,[x_green(1) y_green(1)]);
C = cat(3,RR,GG,img_blue);
end

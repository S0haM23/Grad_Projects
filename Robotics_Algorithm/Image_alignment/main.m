image_dir = dir('image*.jpg');
image_list = length(image_dir);
images = cell(1,image_list);

for k = 1:image_list
     if any(ismember(image_dir(k).name, '-')) == 0
    images{k} = imread(image_dir(k).name);
     end
end
K = 1;
for k = 1:image_list
    if ~isempty(images{k})
    im = im2gray(images{k});
    im  = im2double(im);
    [row,~]=size(im);   % im is your image
    height=fix(row/3);

    img_blue = im(1:height,:);
    img_green =im(height+1:2*height,:);
    img_red = im(2*height+1:row,:);
    img_red(end,:) = [];
    
    Color = cat(3,img_red,img_blue,img_blue);
    filename = ['image',num2str(K),'-color.jpg'];
    imwrite(Color,filename)
    
    fprintf('Image %i \n',k)
    C_ssd = im_align1(img_blue,img_green,img_red);
    filename = ['image',num2str(K),'-ssd.jpg'];
    imwrite(C_ssd,filename)
    
    C_ncc = im_align2(img_blue,img_green,img_red);
    filename = ['image',num2str(K),'-ncc.jpg'];
    imwrite(C_ncc,filename)
    
    [C,Cg,Cr] = harris(img_blue,img_green,img_red);
    C_harris = im_align3(img_blue,img_green,img_red,C,Cg,Cr);
    filename = ['image',num2str(K),'-corner.jpg'];
    imwrite(C_harris,filename)
    fprintf('\n')
    end
    K = K+1;
end
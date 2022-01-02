function C = im_align1(img_blue,img_green,img_red)

   [img_blue_row,img_blue_col] = size(img_blue);
    % checking SSD for cropped part of the images for faster calculation 
    roi = [ fix((img_blue_row-50)/2) fix((img_blue_col-50)/2)  30 30]; 
    red_window = imcrop(img_red,roi);
    base_window = imcrop(img_blue,roi);
    green_window = imcrop(img_green,roi);
    % figure,imshow(green_window),figure,imshow(green_window_cr)
    MiN = 10000;
    r_x_adjust = 0; g_x_adjust = 0;
    r_y_adjust = 1; g_y_adjust = 1;
    %SSD on red image
    for i = -15:15
        for j = -15:15
        x = double(base_window)-double(circshift(red_window,[i,j]));
        ssd = sum(x(:).^2);
        if ssd < MiN
            MiN = ssd;
            r_x_adjust = i;
            r_y_adjust = j;
        end
        end
    end
    Min = 10000;
    % SSD on green image
    for i_g = -15:15
        for j_g = -15:15
        x = double(base_window)-double(circshift(green_window,[i_g,j_g]));
        ssd = sum(x(:).^2);
        if ssd < Min
            Min = ssd;
            g_x_adjust = i_g;
            g_y_adjust = j_g;
        end
        end
    end
    aligned_red = circshift(img_red,[r_x_adjust,r_y_adjust]);
    aligned_green = circshift(img_green,[g_x_adjust,g_y_adjust]);
    C = cat(3,aligned_red,aligned_green,img_blue);
    fprintf('SSD Red Offsets : %i , %i \n',r_x_adjust,r_y_adjust)
    fprintf('SSD Green Offsets : %i , %i \n',g_x_adjust, g_y_adjust)
end




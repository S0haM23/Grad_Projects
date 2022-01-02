function C = im_align2(im_blue,im_green,im_red)
roi = [150 170  60 60]; 
im_red_crop = imcrop(im_red,roi);
im_blue_crop = imcrop(im_blue,roi);
im_green_crop = imcrop(im_green,roi);
%% looks for a correlation of red  image wrt blue
maxim = 0;
    for i_g = -15:15
    for j_g = -15:15
        g_shifted = circshift(im_green_crop,[i_g,j_g]);
        NCC_G = sum(im_blue_crop.*g_shifted) / sqrt(sum(im_blue_crop.^2).*(sum(g_shifted).^2));
        if NCC_G > maxim
            maxim = NCC_G;
            g_x_adjust = i_g;
            g_y_adjust = j_g;
        end
    end
    end
    
max = 0;
    for i_r = -15:15
    for j_r = -15:15
        r_shifted = circshift(im_red_crop,[i_r,j_r]);
        NCC_R = sum(im_blue_crop.*r_shifted) / sqrt(sum(im_blue_crop.^2).*(sum(r_shifted).^2));
        if NCC_R > max
            max = NCC_R;
            r_x_adjust = i_r;
            r_y_adjust = j_r;
        end
    end
    end
im_green_shifted = circshift(im_green, [g_x_adjust ,g_y_adjust]);
im_red_shifted = circshift(im_red, [r_x_adjust,r_y_adjust]);
C = cat(3,im_red_shifted,im_green_shifted,im_blue);
fprintf('NCC Red Offsets : %i , %i \n',r_x_adjust,r_y_adjust)
fprintf('NCC Green Offsets : %i , %i \n',g_x_adjust, g_y_adjust)
end

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 15:08:48 2019
Python Version = 3.6.9

@author: Xi Bi

COMP9517 Computer Vision ass_1

"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# task_1
def band_transf(image):
    hight,width,_ = image.shape
    new_img = list()
    for i in range(hight):
        new_row = list()
        for j in range(width):
            pixel = 0.299*image[i][j][2] + 0.587*image[i][j][1] + 0.114*image[i][j][0]
            new_row.append(pixel)
        new_img.append(new_row)
    return np.array(new_img).astype(int)

# draw the distribution of the grey level in the image 
def histogram_show(image):
    try:
        plt.subplot(2,2,1),plt.imshow(image,'gray')
        plt.subplot(2,2,2),plt.hist(image.ravel(),256,[0,256])
        return True
    except:
        return False

# task_2 && task_2
def oil_painting(img_ori,image,window_size,grey_level,level_size,step=1):
    hight,width = image.shape[:2]
    window_length = int((window_size**0.5 - 1)/2)
    image = ((image/grey_level)*level_size).astype(int)
    most_img = np.zeros(image.shape,np.uint8)
    oil_img = np.zeros(img_ori.shape,np.uint8)
    for i in range(0,hight,step):
        edge_top = i - window_length
        edge_bottom = i + window_length + 1
        if edge_top < 0:
            edge_top = 0
        if edge_bottom >= hight:
            edge_bottom = hight - 1
        for j in range(0,width,step):
            edge_left = j - window_length
            edge_right = j + window_length + 1
            if edge_left < 0:
                edge_left = 0
            if edge_right >= width:
                edge_right = width - 1
            
            level_histogram = np.zeros(level_size,np.uint8)
            
            for m in range(edge_top,edge_bottom):
                for n in range(edge_left,edge_right):
                    pix_level = image[m][n]
                    level_histogram[pix_level] += 1
                    
            most_level = np.max(level_histogram)
            most_index = np.argmax(level_histogram)
            aver_color = [0,0,0]
    
            for m in range(edge_top,edge_bottom):
                for n in range(edge_left,edge_right):
                    pix_level = image[m][n]
                    if pix_level == most_index:
                        aver_color += img_ori[m][n]
            aver_color = (aver_color/most_level).astype(int)
            
            for m in range(step):
                for n in range(step):
                    if (i + m < hight) and (j + n < width):
                        oil_img[i+m][j+n] = aver_color
                        most_img[i+m][j+n] = most_index*32
            
    return most_img,oil_img
           


if __name__ == '__main__':
    np.seterr(divide='ignore', invalid='ignore')
    img_ori = cv2.imread('Assignment_1_images/light_rail.jpg')
    img_band = band_transf(img_ori)
    cv2.imwrite('result/light_rail_band.jpg',img_band)
    grey_level = np.max(img_band) - np.min(img_band) + 1
    level_size = 8
    for i in range(2,7,2):
        window_size = (i*2+1)**2
        img_most,img_oil = oil_painting(img_ori,img_band,window_size,grey_level,level_size)
        cv2.imwrite('result/light_rail_oil_'+str(window_size)+'.jpg',img_oil)
        cv2.imwrite('result/light_rail_most_'+str(window_size)+'.jpg',img_most)
   
    
    
    
    

import sys
import numpy as np
import cv2
import time
import os
import threading
import pytesseract
import imutils

import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"                      

def get_string(img_path):
    img = cv2.imread(img_path)
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]
    
    output_path = os.path.join('output_path', "ocr")

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    if img is None:
        raise ValueError(f"Resim dosyası '{img_path}' okunamadı. Lütfen dosya yolunu ve formatını kontrol edin.")
    
    img = cv2.resize(img, (int(img.shape[1] * 1.5), int(img.shape[0] * 1.5)), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []

    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)
    
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1) 
    
    #Apply blur to smooth out the edges
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    save_path = os.path.join(output_path, file_name + "_filter_" + str('as') + ".png")
    cv2.imwrite(save_path, img)
    
    result = pytesseract.image_to_string(img, lang="eng")
    return result


def save_img_to_txt(img_path, output_txt_path):
    text = get_string(img_path)
    satir = text.split(sep='\n')
    
    with open(output_txt_path, "w", encoding="utf-8") as file:
        for line in satir:
            file.write(line + "\n")
    
    print(f"Metin başarıyla '{output_txt_path}' dosyasına kaydedildi.")


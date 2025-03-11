import streamlit as st
from OCR_img_to_text import get_string
import os
from PIL import Image

st.title("OCR İşlemi ve Metin Kaydetme")
uploaded_file = st.file_uploader("Bir resim dosyası yükleyin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Görseli yükle
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Görsel", use_container_width=True)
    
    # OCR işlemi yap
    img_path = "temp_image.jpg"     ############
    image.save(img_path)
    text = get_string(img_path)
    
    # OCR sonucunu göster
    st.subheader("OCR Sonucu")
    st.text_area("Metin", text, height=200)

    if text:
        file_name = st.text_input("Dosya Adı")

        # Metni dosyaya yaz
        st.download_button(
            label="Dosyayı İndir",
            data=text,
            file_name = f"{file_name}.txt",
            mime="text/plain"
        )
    else:
        st.error("Lütfen bir metin girin.")

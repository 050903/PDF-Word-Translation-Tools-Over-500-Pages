![image](https://github.com/user-attachments/assets/ea6ddc55-c650-4f52-a6ba-48480314da9f)![image](https://github.com/user-attachments/assets/295feea5-55e2-42fa-9c24-a61acfc7e2b0)# Tool-translate-PDF
Format-Preserving PDF Translator is a powerful desktop application built in Python that translates large PDF documents (hundreds of pages) from one language to another 

# 📘 Format-Preserving PDF Translator Tool (v5.2)

## General Description

**Format-Preserving PDF Translator** is a powerful desktop application built in Python that translates large PDF documents (hundreds of pages) from one language to another **while preserving the original layout and formatting**. This tool is especially useful for translating books, technical manuals, and research papers without breaking their visual structure.

## How it work?

---
![image](https://github.com/user-attachments/assets/eeac10a1-ea2c-4501-b31d-8d6445af40db)
![image](https://github.com/user-attachments/assets/81cab6be-0afe-4581-9994-43e2553b592d)
![image](https://github.com/user-attachments/assets/61f25b3a-9a7c-44f1-95e1-adcfb9c5555c)
![image](https://github.com/user-attachments/assets/7f690e2e-b544-448d-950f-c74b417ec58a)
![image](https://github.com/user-attachments/assets/ce5d4c23-ba94-4fc9-9995-aa6c0f17b4b6)
![image](https://github.com/user-attachments/assets/a80b28cb-158b-4917-8e35-03094c1e51af)
![image](https://github.com/user-attachments/assets/131b31d6-ee7c-44e4-bec1-8937cbd690b0)
![image](https://github.com/user-attachments/assets/1bde55fa-4736-4fb8-a151-0680bdd69b46)
![image](https://github.com/user-attachments/assets/52764771-3131-401d-868b-e3b199aa07e3)
![image](https://github.com/user-attachments/assets/bd59982e-b964-4a9a-a56c-18b3075da4de)
![image](https://github.com/user-attachments/assets/fea1e0d9-573b-42e8-a864-d1883d2b2ef4)
![image](https://github.com/user-attachments/assets/5aa05d9d-5701-49af-884f-a281d9cd6d96)
![image](https://github.com/user-attachments/assets/0d712ce1-e80e-4476-af85-7ad977167f89)
![image](https://github.com/user-attachments/assets/5e645a5a-7655-4592-9d32-dd1fc6d9886c)
![image](https://github.com/user-attachments/assets/5ffa8828-3406-49ff-baeb-4b7fdb6f63fc)
![image](https://github.com/user-attachments/assets/4c355e66-575d-4929-9d74-03ea0d8c67fc)
![image](https://github.com/user-attachments/assets/75370c45-4ca3-4e07-bfd7-27d92c482bbc)
![image](https://github.com/user-attachments/assets/e10df560-38ac-44ee-b4ee-2c7e4cce5764)
![image](https://github.com/user-attachments/assets/15d5a60b-c3db-4c54-822c-88aaa2ceaa72)
![image](https://github.com/user-attachments/assets/67ec7775-72a0-4a78-84ca-36aa57df4222)
![image](https://github.com/user-attachments/assets/80a80f95-ed6f-4ee1-b1db-a20a90bbfac8)
![image](https://github.com/user-attachments/assets/d5ff5571-9aec-4ac3-8566-c476b1e4de5c)

---

## 🚀 How It Works

The application follows an intelligent **6-step process** for each page:

1. **PDF to Image Conversion**
   Each page is converted into a high-resolution image (customizable DPI).

2. **Optical Character Recognition (OCR)**
   Google's Tesseract OCR engine scans the image to identify every word or phrase and records its precise coordinates (x, y, width, height).

3. **Text Translation**
   The recognized text is translated using the Google Translate API via `deep-translator`. A translation cache significantly speeds up the process by avoiding redundant translations.

4. **Page Reconstruction**
   The original text areas are covered with white rectangles while keeping the page layout intact.

5. **Drawing Translated Text**
   The translated text is drawn back onto the image in the exact positions of the original text. Automatic text wrapping and dynamic font sizing ensure that the translation fits naturally.

6. **Final PDF Assembly**
   All processed images are combined into a single, new PDF file with preserved visual structure.

---

## 🛠️ Libraries & Technologies Used

* **Language**: Python 3
* **GUI**: Tkinter
* **PDF Handling**: `PyMuPDF (fitz)`
* **Image Processing**: `Pillow (PIL)`
* **OCR**: Tesseract OCR via `pytesseract`
* **Translation**: `deep-translator` (supports Google Translate and others)

---

## 🔍 Key Features

* **Format-Preserving Translation**: Keeps the original layout intact
* **Dynamic Text Wrapping & Font Sizing**: Ensures readability
* **Translation Caching**: Avoids repeating translations
* **ETR (Estimated Time of Arrival)**: Predicts completion time
* **Quality vs. Speed Mode**: Choose between high accuracy or fast processing
* **Multithreading**: Keeps the UI responsive during translation

---

## 📘 User Guide

### 🔧 Prerequisites

1. Install Python 3
2. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and required language packs (e.g., Vietnamese, English)
3. Install Python dependencies:

   ```bash
   pip install deep-translator PyMuPDF Pillow pytesseract
   ```
4. Configure the path to `tesseract.exe` in the script file

### ▶️ Running the Application

```bash
python script_name.py
```

### 👛 Using the Tool

1. Click **"Select File..."** to choose your PDF.
2. Select the target language and processing mode (quality vs. speed).
3. Click **"Start Translation"**.
4. Monitor progress through the live preview, stats panel, and progress bar.
5. Upon completion, a translated PDF named `_dich_visual_v5.pdf` will be saved in the same folder.

---

## 👤 Author & License

* **Author**: Tran The Hao
* **Institution**: University of Transport Ho Chi Minh City (UTH)
* **License**: [MIT License](LICENSE)


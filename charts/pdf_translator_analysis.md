## PDF Translation Tool Functionality and Architecture Analysis

### Overview
The provided Python script implements a desktop application for visually translating PDF documents. It leverages OCR to extract text from PDF pages, translates the extracted text, and then overlays the translated text back onto the page, effectively creating a translated version of the original PDF.

### Key Components and Workflow:

1.  **User Interface (UI) - `TranslatorApp` Class (Tkinter)**:
    *   **File Selection**: Allows users to browse and select a PDF file for translation.
    *   **Language Selection**: Provides options to choose the target translation language (e.g., Vietnamese, English, Japanese).
    *   **Quality/Speed Selection**: Enables users to select the DPI (Dots Per Inch) for image conversion, influencing the quality of OCR and output, and thus the processing speed.
    *   **Progress and Status Display**: Shows real-time logs, a progress bar indicating page processing, and statistics like file size, current page, elapsed time, and estimated time remaining.
    *   **Live Preview**: Displays the currently processed page with translated text.
    *   **Start Button**: Initiates the translation process in a separate thread to keep the UI responsive.

2.  **Backend Translation Process - `run_visual_translation_process` Function (Core Logic)**:
    *   **PDF Loading**: Opens the input PDF file using `fitz` (PyMuPDF).
    *   **Page Iteration**: Processes each page of the PDF sequentially.
    *   **Page to Image Conversion**: Converts each PDF page into a high-resolution image using `page.get_pixmap()` based on the selected DPI.
    *   **Optical Character Recognition (OCR)**: Uses `pytesseract.image_to_data()` to detect text regions, extract text, and get bounding box coordinates for each text block on the image. It supports multiple languages (English and Vietnamese in the example).
    *   **Text Translation**: Iterates through the detected text blocks. For each block, it checks a translation cache. If not found, it uses `deep_translator.GoogleTranslator` to translate the text to the target language.
    *   **Image Reconstruction**: For each translated text block:
        *   The original text area on the image is filled with white to erase it.
        *   The translated text is drawn onto the cleared area using `ImageDraw.Draw()` and `draw_text_with_wrapping()`. The `draw_text_with_wrapping` function handles text wrapping and font sizing to fit the translated text within the original bounding box.
    *   **UI Update**: Calls back to the UI to update the live image preview, progress bar, and statistics.
    *   **PDF Saving**: After processing all pages, the translated images are saved as a new PDF file using `PIL.Image.save()` with `save_all=True` and `append_images`.

### External Libraries Used:
*   `tkinter`: For building the graphical user interface.
*   `fitz` (PyMuPDF): For PDF manipulation (opening, loading pages, converting to pixmaps).
*   `PIL` (Pillow): For image processing (creating images from pixmaps, drawing, resizing, saving).
*   `pytesseract`: For Optical Character Recognition (OCR).
*   `deep_translator`: For text translation using Google Translate.
*   `threading`: To run the translation process in a separate thread, preventing the UI from freezing.

### Flow Diagram (Conceptual):

```mermaid
graph TD
    A[User Selects PDF, Language, Quality] --> B{Start Translation}
    B --> C[Load PDF (fitz)]
    C --> D{For Each Page}
    D --> E[Convert Page to Image (fitz)]
    E --> F[Perform OCR (pytesseract)]
    F --> G{For Each Detected Text Block}
    G --> H{Check Translation Cache}
    H -- Cache Hit --> I[Get Translated Text]
    H -- Cache Miss --> J[Translate Text (deep_translator)]
    J --> I
    I --> K[Erase Original Text on Image]
    K --> L[Draw Translated Text on Image (Pillow)]
    L --> M[Update UI (Progress, Preview)]
    M --> D
    D -- All Pages Processed --> N[Save All Translated Images as New PDF]
    N --> O[Translation Complete / Show Success Message]
    O --> P[Enable UI]
```

This analysis will serve as the basis for generating the website content and the interactive chart diagram.


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time
import datetime
import json
import multiprocessing

# --- THƯ VIỆN CẦN THIẾT ---
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageTk, ImageFont
import pytesseract
from deep_translator import GoogleTranslator

# --- CẤU HÌNH QUAN TRỌNG ---
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    FONT_PATH = "arial.ttf"
    CACHE_FILE = "translation_cache.json"
except Exception as e:
    print(f"LỖI CẤU HÌNH: {e}. Vui lòng kiểm tra lại đường dẫn Tesseract và Font.")
    FONT_PATH = None
    CACHE_FILE = "translation_cache.json"

# =====================================================================================
# CÁC HÀM TIỆN ÍCH VÀ XỬ LÝ LÕI
# =====================================================================================

def load_translation_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except (json.JSONDecodeError, IOError): return {}
    return {}

def save_translation_cache(cache):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f: json.dump(cache, f, ensure_ascii=False, indent=2)
    except IOError: print("Không thể lưu file cache.")

# --- BỘ XỬ LÝ CHO CHẾ ĐỘ "CẤU TRÚC" ---
def run_structured_translation_process(input_path, target_lang, status_callback, progress_callback, enable_ui_callback):
    # ... (Hàm này không thay đổi, đã ổn định)
    try:
        status_callback("--- BẮT ĐẦU DỊCH CẤU TRÚC (GIỮ ĐỊNH DẠNG) ---")
        start_time = time.time()
        translation_cache, translator = load_translation_cache(), GoogleTranslator(source='auto', target=target_lang)
        doc = fitz.open(input_path)
        total_pages = len(doc)
        progress_callback(0, total_pages)
        status_callback("Bước 1: Thu thập toàn bộ văn bản từ tài liệu...")
        all_texts, all_spans_by_page = [], []
        for page in doc:
            page_spans, blocks = [], page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]: page_spans.extend(line["spans"])
            all_spans_by_page.append(page_spans)
            all_texts.extend([span["text"].strip() for span in page_spans if span["text"].strip()])
        unique_texts_to_translate = list(set(t for t in all_texts if t not in translation_cache))
        if unique_texts_to_translate:
            status_callback(f"Bước 2: Chuẩn bị dịch {len(unique_texts_to_translate)} cụm từ mới...")
            chunk_size, total_to_translate, translated_count = 100, len(unique_texts_to_translate), 0
            for i in range(0, total_to_translate, chunk_size):
                chunk = unique_texts_to_translate[i:i + chunk_size]
                try:
                    translated_snippets = translator.translate_batch(chunk)
                    for original, translated in zip(chunk, translated_snippets):
                        translation_cache[original] = translated if translated else original
                    translated_count += len(chunk)
                    status_callback(f"Đang dịch... ({translated_count}/{total_to_translate})")
                    save_translation_cache(translation_cache)
                except Exception as e:
                    status_callback(f"Lỗi khi dịch gói {i//chunk_size + 1}. Bỏ qua. Lỗi: {e}")
                    time.sleep(2)
        status_callback("Bước 3: Bắt đầu tái tạo lại các trang...")
        for i, page in enumerate(doc):
            status_callback(f"Đang tái tạo trang {i + 1}/{total_pages}...")
            spans_on_this_page = all_spans_by_page[i]
            for span in spans_on_this_page:
                original_text = span["text"].strip()
                if original_text in translation_cache:
                    translated_text = translation_cache[original_text]
                    page.add_redact_annot(span["bbox"], text=translated_text, fontname=span["font"], fontsize=span["size"], text_color=span["color"], align=fitz.TEXT_ALIGN_LEFT)
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            progress_callback(i + 1, total_pages)
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_translated_structured.pdf"
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        elapsed = time.time() - start_time
        status_callback(f"--- HOÀN THÀNH sau {elapsed:.2f} giây! ---")
        messagebox.showinfo("Thành công", f"Đã dịch và lưu file thành công!\nFile được lưu tại:\n{output_path}")
    except Exception as e:
        import traceback
        error_msg = f"Một lỗi nghiêm trọng đã xảy ra:\n{traceback.format_exc()}"
        status_callback(error_msg)
        messagebox.showerror("Lỗi", error_msg)
    finally:
        enable_ui_callback()

# --- BỘ XỬ LÝ CHO CHẾ ĐỘ "TRỰC QUAN (OCR)" ---
def draw_text_with_wrapping(draw, text, box, font_path):
    # ... (Hàm này không thay đổi)
    x, y, w, h = box
    font_size, font = int(h * 0.9), None
    while font_size > 5:
        try: font = ImageFont.truetype(font_path, size=font_size)
        except (IOError, TypeError): font = ImageFont.load_default()
        words = text.split()
        if not words: return
        lines, current_line = [], words[0]
        for word in words[1:]:
            if font.getbbox(current_line + " " + word)[2] <= w: current_line += " " + word
            else: lines.append(current_line); current_line = word
        lines.append(current_line)
        total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
        if total_height <= h:
            current_y = y
            for line in lines:
                line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
                draw.text((x, current_y), line, font=font, fill='black'); current_y += line_height
            return
        font_size -= 1
    if text:
        if not font:
            try: font = ImageFont.truetype(font_path, size=8)
            except (IOError, TypeError): font = ImageFont.load_default()
        draw.text((x, y), text[:20] + "...", font=font, fill='black')

def process_single_page_visual(args):
    page_num, input_path, quality_dpi, target_lang, shared_cache, font_path = args
    doc = fitz.open(input_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=quality_dpi)
    
    # ==================================================================
    # ĐOẠN MÃ ĐÃ SỬA LỖI UnboundLocalError
    # Tách việc tạo img và draw ra 2 dòng riêng biệt.
    # ==================================================================
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    draw = ImageDraw.Draw(img)
    
    doc.close()
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng+vie')
    text_info_map, texts_to_translate_on_page = [], []
    for i in range(len(ocr_data['level'])):
        if int(ocr_data['conf'][i]) > 60:
            text = ocr_data['text'][i].strip()
            if text:
                if text not in shared_cache: texts_to_translate_on_page.append(text)
                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                text_info_map.append({'box': (x, y, w, h), 'original_text': text})
    if texts_to_translate_on_page:
        translator = GoogleTranslator(source='auto', target=target_lang)
        try:
            unique_texts = list(set(texts_to_translate_on_page))
            translated_texts = translator.translate_batch(unique_texts)
            for original, translated in zip(unique_texts, translated_texts):
                shared_cache[original] = translated if translated else original
        except Exception:
            for text in unique_texts: shared_cache[text] = text # Fallback
    for item in text_info_map:
        translated_text = shared_cache.get(item['original_text'], item['original_text'])
        draw.rectangle([item['box'][0], item['box'][1], item['box'][0] + item['box'][2], item['box'][1] + item['box'][3]], fill='white', outline='white')
        draw_text_with_wrapping(draw, translated_text, item['box'], font_path)
    return (page_num, img)

def run_visual_translation_process(input_path, target_lang, quality_dpi, status_callback, progress_callback, enable_ui_callback):
    try:
        doc = fitz.open(input_path)
        total_pages = len(doc)
        doc.close()

        manager = multiprocessing.Manager()
        shared_cache = manager.dict(load_translation_cache())
        
        num_processes = max(1, multiprocessing.cpu_count() - 1)
        pool = multiprocessing.Pool(processes=num_processes)
        tasks = [(i, input_path, quality_dpi, target_lang, shared_cache, FONT_PATH) for i in range(total_pages)]
        
        translated_pages_images, completed_count = [None] * total_pages, 0
        status_callback(f"Bắt đầu dịch trực quan {total_pages} trang trên {num_processes} nhân CPU...")
        progress_callback(0, total_pages)
        
        for page_num, result_image in pool.imap_unordered(process_single_page_visual, tasks):
            completed_count += 1
            translated_pages_images[page_num] = result_image
            progress_callback(completed_count, total_pages)
            status_callback(f"Đã xử lý xong trang {page_num + 1}/{total_pages}")
            
        pool.close()
        pool.join()
        
        if any(p is not None for p in translated_pages_images):
            status_callback("Đang lưu tất cả các trang vào file PDF mới...")
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_translated_visual.pdf"
            valid_images = [img for img in translated_pages_images if img is not None]
            valid_images[0].save(output_path, save_all=True, append_images=valid_images[1:])
            save_translation_cache(dict(shared_cache))
            status_callback(f"--- HOÀN THÀNH! Đã lưu vào: {output_path} ---")
            messagebox.showinfo("Thành công", f"Đã dịch và lưu file thành công!\nFile được lưu tại:\n{output_path}")
    except Exception as e:
        import traceback
        error_msg = f"Lỗi trong quá trình dịch trực quan:\n{traceback.format_exc()}"
        status_callback(error_msg)
        messagebox.showerror("Lỗi", error_msg)
    finally:
        enable_ui_callback()

# --- LỚP GIAO DIỆN NGƯỜI DÙNG (UI) ---
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Dịch PDF Chuyên Nghiệp v3.6 (Bản ổn định)")
        self.root.geometry("850x700")

        # ... (Toàn bộ phần giao diện không thay đổi)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        file_frame = ttk.LabelFrame(main_frame, text="Bước 1: Chọn File PDF")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        self.filepath_var = tk.StringVar()
        self.filepath_entry = ttk.Entry(file_frame, textvariable=self.filepath_var, state="readonly")
        self.filepath_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.browse_button = ttk.Button(file_frame, text="Chọn File...", command=self.select_file)
        self.browse_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)

        lang_frame = ttk.LabelFrame(settings_frame, text="Bước 2: Chọn Ngôn Ngữ Đích")
        lang_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        self.languages = {"Tiếng Việt": "vi", "Tiếng Anh": "en", "Tiếng Nhật": "ja", "Tiếng Hàn": "ko", "Tiếng Trung (Giản thể)": "zh-cn"}
        self.lang_var = tk.StringVar(value="Tiếng Việt")
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=list(self.languages.keys()), state="readonly")
        lang_menu.pack(padx=5, pady=5, fill=tk.X, expand=True)

        mode_frame = ttk.LabelFrame(settings_frame, text="Bước 3: Chọn Chế Độ Dịch")
        mode_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        self.mode_var = tk.StringVar(value="structured")
        self.mode_var.trace("w", self.on_mode_change)
        ttk.Radiobutton(mode_frame, text="Cấu trúc (Nhanh, Giữ định dạng)", variable=self.mode_var, value="structured").pack(anchor=tk.W, padx=5)
        ttk.Radiobutton(mode_frame, text="Trực quan (OCR cho file scan)", variable=self.mode_var, value="visual").pack(anchor=tk.W, padx=5)

        self.quality_frame = ttk.LabelFrame(main_frame, text="Bước 3.5: Chọn Chất lượng (chỉ cho OCR)")
        self.quality_var = tk.IntVar(value=200)
        ttk.Radiobutton(self.quality_frame, text="Nhanh (150 DPI)", variable=self.quality_var, value=150).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.quality_frame, text="Cân bằng (200 DPI)", variable=self.quality_var, value=200).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.quality_frame, text="Chất lượng cao (300 DPI)", variable=self.quality_var, value=300).pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(main_frame, text="Bước 4: Bắt Đầu Dịch", command=self.start_translation_thread, style="Accent.TButton")
        self.start_button.pack(fill=tk.X, padx=5, pady=10, ipady=5)
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        
        progress_frame = ttk.LabelFrame(main_frame, text="Tiến Độ")
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        log_frame = ttk.LabelFrame(main_frame, text="Nhật ký chi tiết")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state="disabled", height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.on_mode_change()

    def on_mode_change(self, *args):
        if self.mode_var.get() == "visual":
            self.quality_frame.pack(fill=tk.X, padx=5, pady=5, before=self.start_button)
        else:
            self.quality_frame.pack_forget()

    def select_file(self):
        filepath = filedialog.askopenfilename(title="Chọn file PDF", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if filepath: self.filepath_var.set(filepath); self.log(f"Đã chọn file: {os.path.basename(filepath)}")

    def log(self, message): self.root.after(0, self._log_threadsafe, message)
    def _log_threadsafe(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_progress(self, value, maximum): self.root.after(0, self._update_progress_threadsafe, value, maximum)
    def _update_progress_threadsafe(self, value, maximum):
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = value
    
    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        for child in self.root.winfo_children():
            if isinstance(child, (ttk.Frame, ttk.LabelFrame)):
                for sub_widget in child.winfo_children():
                    if isinstance(sub_widget, (ttk.Button, ttk.Entry, ttk.Combobox, ttk.Radiobutton)):
                        try: sub_widget.config(state=state)
                        except tk.TclError: pass
            elif isinstance(child, (ttk.Button)):
                try: child.config(state=state)
                except tk.TclError: pass
        
    def start_translation_thread(self):
        input_path = self.filepath_var.get()
        if not input_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn một file PDF để dịch!")
            return
        self.set_ui_state(False)
        self.log_text.config(state="normal"); self.log_text.delete(1.0, tk.END); self.log_text.config(state="disabled")
        target_lang_code = self.languages[self.lang_var.get()]
        mode = self.mode_var.get()
        thread = None
        if mode == "structured":
            thread = threading.Thread(target=run_structured_translation_process, args=(input_path, target_lang_code, self.log, self.update_progress, lambda: self.set_ui_state(True)))
        elif mode == "visual":
            quality_dpi = self.quality_var.get()
            # Đổi hàm callback cho progress bar trong chế độ visual
            thread = threading.Thread(target=run_visual_translation_process, args=(input_path, target_lang_code, quality_dpi, self.log, self.update_progress, lambda: self.set_ui_state(True)))
        if thread:
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    if os.name == 'nt': multiprocessing.freeze_support()
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

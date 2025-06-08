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
# PHƯƠNG PHÁP 2: DỊCH CẤU TRÚC (GIỮ NGUYÊN ĐỊNH DẠNG)
# =====================================================================================

def load_translation_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_translation_cache(cache):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except IOError:
        print("Không thể lưu file cache.")

def run_structured_translation_process(input_path, target_lang, status_callback, progress_callback, enable_ui_callback):
    try:
        status_callback("--- BẮT ĐẦU DỊCH CẤU TRÚC (GIỮ ĐỊNH DẠNG) ---")
        start_time = time.time()
        
        translation_cache = load_translation_cache()
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        doc = fitz.open(input_path)
        total_pages = len(doc)
        progress_callback(0, total_pages)
        
        status_callback("Bước 1: Thu thập toàn bộ văn bản từ tài liệu...")
        all_texts = []
        all_spans_by_page = []

        for page in doc:
            page_spans = []
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        page_spans.extend(line["spans"])
            all_spans_by_page.append(page_spans)
            all_texts.extend([span["text"].strip() for span in page_spans if span["text"].strip()])

        unique_texts_to_translate = list(set(t for t in all_texts if t not in translation_cache))
        
        # Bước 2: Dịch hàng loạt THEO TỪNG GÓI (CHUNK)
        if unique_texts_to_translate:
            status_callback(f"Bước 2: Chuẩn bị dịch {len(unique_texts_to_translate)} cụm từ mới...")
            
            # ==================================================================
            # SỬA LỖI ĐỨNG HÌNH: Chia danh sách cần dịch thành các gói nhỏ
            # ==================================================================
            chunk_size = 100  # Dịch 100 cụm từ mỗi lần
            total_to_translate = len(unique_texts_to_translate)
            translated_count = 0

            for i in range(0, total_to_translate, chunk_size):
                chunk = unique_texts_to_translate[i:i + chunk_size]
                try:
                    translated_snippets = translator.translate_batch(chunk)
                    # Cập nhật cache sau khi dịch thành công 1 gói
                    for original, translated in zip(chunk, translated_snippets):
                        translation_cache[original] = translated if translated else original
                    
                    translated_count += len(chunk)
                    status_callback(f"Đang dịch... ({translated_count}/{total_to_translate})")
                    
                    # Lưu cache định kỳ để phòng trường hợp lỗi giữa chừng
                    save_translation_cache(translation_cache)

                except Exception as e:
                    status_callback(f"Lỗi khi dịch gói {i//chunk_size + 1}. Bỏ qua gói này. Lỗi: {e}")
                    time.sleep(2) # Chờ một chút trước khi thử lại gói tiếp theo

        status_callback("Bước 3: Bắt đầu tái tạo lại các trang...")
        for i, page in enumerate(doc):
            status_callback(f"Đang tái tạo trang {i + 1}/{total_pages}...")
            
            spans_on_this_page = all_spans_by_page[i]
            
            for span in spans_on_this_page:
                original_text = span["text"].strip()
                if original_text in translation_cache:
                    translated_text = translation_cache[original_text]
                    page.add_redact_annot(span["bbox"], text=translated_text, 
                                          fontname=span["font"], 
                                          fontsize=span["size"],
                                          text_color=span["color"],
                                          align=fitz.TEXT_ALIGN_LEFT)
            
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            progress_callback(i + 1, total_pages)

        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_translated_structured.pdf"
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        
        elapsed = time.time() - start_time
        status_callback(f"--- HOÀN THÀNH sau {elapsed:.2f} giây! ---")
        status_callback(f"Đã lưu thành công vào: {output_path}")
        messagebox.showinfo("Thành công", f"Đã dịch và lưu file thành công!\n\nFile được lưu tại:\n{output_path}")

    except Exception as e:
        import traceback
        error_msg = f"Một lỗi nghiêm trọng đã xảy ra:\n{traceback.format_exc()}"
        status_callback(error_msg)
        messagebox.showerror("Lỗi", error_msg)
    finally:
        enable_ui_callback()
        
# --- LỚP GIAO DIỆN NGƯỜI DÙNG (UI) ---
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Dịch PDF Chuyên Nghiệp v3.3 (Fix Lỗi Đứng Hình)")
        # ... (Phần còn lại của __init__ giữ nguyên như cũ) ...
        self.root.geometry("850x700")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        control_frame.columnconfigure(0, weight=1)

        file_frame = ttk.LabelFrame(control_frame, text="Bước 1: Chọn File PDF")
        file_frame.grid(row=0, column=0, sticky="ew", pady=5)
        file_frame.columnconfigure(0, weight=1)
        self.filepath_var = tk.StringVar()
        self.filepath_entry = ttk.Entry(file_frame, textvariable=self.filepath_var, state="readonly")
        self.filepath_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.browse_button = ttk.Button(file_frame, text="Chọn File...", command=self.select_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        settings_frame = ttk.Frame(control_frame)
        settings_frame.grid(row=1, column=0, sticky="ew", pady=5)
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
        ttk.Radiobutton(mode_frame, text="Cấu trúc (Nhanh, Giữ định dạng)", variable=self.mode_var, value="structured").pack(anchor=tk.W, padx=5)
        ttk.Radiobutton(mode_frame, text="Trực quan (OCR cho file scan)", variable=self.mode_var, value="visual", state="disabled").pack(anchor=tk.W, padx=5)

        self.start_button = ttk.Button(control_frame, text="Bước 4: Bắt Đầu Dịch", command=self.start_translation_thread, style="Accent.TButton")
        self.start_button.grid(row=2, column=0, pady=10, ipady=5, sticky="ew")
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        
        progress_frame = ttk.LabelFrame(main_frame, text="Tiến Độ")
        progress_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        log_frame = ttk.LabelFrame(main_frame, text="Nhật ký chi tiết")
        log_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state="disabled", height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def select_file(self):
        filepath = filedialog.askopenfilename(title="Chọn file PDF", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if filepath:
            self.filepath_var.set(filepath)
            self.log(f"Đã chọn file: {os.path.basename(filepath)}")

    def log(self, message):
        self.root.after(0, self._log_threadsafe, message)

    def _log_threadsafe(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_progress(self, value, maximum):
        self.root.after(0, self._update_progress_threadsafe, value, maximum)

    def _update_progress_threadsafe(self, value, maximum):
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = value
    
    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        for child in self.root.winfo_children():
            for widget in child.winfo_children():
                 if isinstance(widget, (ttk.Frame)):
                     for sub_widget in widget.winfo_children():
                         if isinstance(sub_widget, (ttk.Button, ttk.Entry, ttk.Combobox, ttk.Radiobutton)):
                            try:
                                sub_widget.config(state=state)
                            except tk.TclError:
                                pass
                 elif isinstance(widget, (ttk.Button)):
                    try:
                        widget.config(state=state)
                    except tk.TclError:
                        pass
        
    def start_translation_thread(self):
        input_path = self.filepath_var.get()
        if not input_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn một file PDF để dịch!")
            return

        self.set_ui_state(False)
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")

        target_lang_code = self.languages[self.lang_var.get()]
        mode = self.mode_var.get()

        if mode == "structured":
            thread = threading.Thread(
                target=run_structured_translation_process,
                args=(input_path, target_lang_code, self.log, self.update_progress, lambda: self.set_ui_state(True))
            )
        else:
            messagebox.showinfo("Thông báo", "Chế độ Dịch Trực quan (OCR) chưa được triển khai đầy đủ.")
            self.set_ui_state(True)
            return

        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    if os.name == 'nt':
        multiprocessing.freeze_support()
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

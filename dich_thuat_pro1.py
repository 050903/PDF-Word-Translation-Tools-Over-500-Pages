import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time
import datetime

# Các thư viện xử lý file, ảnh và dịch thuật
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageTk, ImageFont
import pytesseract
from deep_translator import GoogleTranslator

# --- CẤU HÌNH QUAN TRỌNG ---
try:
    pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
    FONT_PATH = "arial.ttf"
except Exception:
    print("LƯU Ý: Không tìm thấy Tesseract hoặc font Arial. Vui lòng chỉnh sửa đường dẫn trong code.")
    FONT_PATH = None

# --- CÁC HÀM LÕI XỬ LÝ DỊCH THUẬT (BACKEND) ---

def draw_text_with_wrapping(draw, text, box, font_path):
    x, y, w, h = box
    font_size = int(h * 0.95) 
    
    while font_size > 5:
        try:
            font = ImageFont.truetype(font_path, size=font_size)
        except IOError:
            font = ImageFont.load_default()

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if font.getbbox(current_line + " " + word)[2] <= w:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())

        total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)

        if total_height <= h:
            current_y = y
            for line in lines:
                line_height = font.getbbox(line)[3] - font.getbbox(line)[1]
                draw.text((x, current_y), line, font=font, fill='black')
                current_y += line_height
            return
        else:
            font_size -= 1
    
    if text:
        draw.text((x, y), text[:20]+"...", font=font, fill='black')

def run_visual_translation_process(input_path, target_lang, quality_dpi, status_callback, image_update_callback, progress_callback, stats_update_callback, enable_ui_callback):
    try:
        doc = fitz.open(input_path)
        total_pages = len(doc)
        translated_pages_images = []
        translation_cache = {}
        start_time = time.time()

        for page_num in range(total_pages):
            status_callback(f"--- Đang xử lý trang {page_num + 1}/{total_pages} ---")
            
            elapsed_time = time.time() - start_time
            if page_num > 0:
                avg_time_per_page = elapsed_time / page_num
                remaining_pages = total_pages - page_num
                etr = avg_time_per_page * remaining_pages
                etr_str = str(datetime.timedelta(seconds=int(etr)))
            else:
                etr_str = "Đang tính toán..."
            
            stats_update_callback({
                "page": f"{page_num + 1} / {total_pages}",
                "elapsed": str(datetime.timedelta(seconds=int(elapsed_time))),
                "etr": etr_str
            })

            status_callback("Bước 1: Chuyển đổi trang thành hình ảnh...")
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=quality_dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            draw = ImageDraw.Draw(img)

            status_callback("Bước 2: Nhận dạng văn bản và vị trí (OCR)...")
            ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng+vie')
            
            num_boxes = len(ocr_data['level'])
            boxes_to_process = []
            
            status_callback("Bước 3: Bắt đầu dịch từng cụm từ...")
            translator = GoogleTranslator(source='auto', target=target_lang)
            
            for i in range(num_boxes):
                if int(ocr_data['conf'][i]) > 60:
                    text = ocr_data['text'][i].strip()
                    h = ocr_data['height'][i]

                    if text and h > 1:
                        (x, y, w) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i])
                        
                        if text in translation_cache:
                            translated_text = translation_cache[text]
                        else:
                            try:
                                translated_text = translator.translate(text)
                                if not translated_text: translated_text = text
                                translation_cache[text] = translated_text
                            except Exception:
                                translated_text = text
                        
                        boxes_to_process.append({'box': (x, y, w, h), 'text': translated_text})

            # ==================================================================
            # ĐOẠN MÃ ĐÃ SỬA LỖI
            # ==================================================================
            status_callback("Bước 4: Tái tạo lại trang đã dịch...")
            for item in boxes_to_process:
                (x, y, w, h) = item['box']
                # SỬA LỖI: Chuyển đổi tọa độ từ (x, y, w, h) sang [x0, y0, x1, y1]
                draw.rectangle([x, y, x + w, y + h], fill='white', outline='white')
                
                # Hàm vẽ chữ vẫn dùng định dạng (x, y, w, h) như cũ
                draw_text_with_wrapping(draw, item['text'], item['box'], FONT_PATH)
            # ==================================================================

            status_callback("Bước 5: Cập nhật giao diện...")
            image_update_callback(img)
            translated_pages_images.append(img)
            progress_callback(page_num + 1)
            time.sleep(0.1)

        if translated_pages_images:
            status_callback("Bước 6: Lưu tất cả các trang đã dịch vào file PDF mới...")
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_dich_visual_v5.1.pdf"
            
            translated_pages_images[0].save(output_path, save_all=True, append_images=translated_pages_images[1:])
            status_callback(f"--- HOÀN THÀNH! ---")
            status_callback(f"Đã lưu thành công vào file: {output_path}")
            messagebox.showinfo("Thành công", f"Đã dịch và lưu file thành công!\n\nFile được lưu tại: {output_path}")
        else:
            status_callback("Không có trang nào được dịch.")

    except Exception as e:
        status_callback(f"Lỗi nghiêm trọng trong quá trình dịch: {e}")
        messagebox.showerror("Lỗi", f"Một lỗi nghiêm trọng đã xảy ra:\n{e}")
    finally:
        enable_ui_callback()

# --- LỚP GIAO DIỆN NGƯỜI DÙNG (UI) ---
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Dịch Thuật Chuyên Nghiệp (v5.1 - Sửa lỗi tọa độ)")
        self.root.geometry("850x800")

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
        lang_menu.pack(padx=5, pady=5, fill=tk.X)

        quality_frame = ttk.LabelFrame(settings_frame, text="Bước 3: Chọn Chất lượng vs. Tốc độ")
        quality_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        self.quality_var = tk.StringVar(value="Cân bằng")
        modes = {"Nhanh (150 DPI)": 150, "Cân bằng (200 DPI)": 200, "Chất lượng cao (300 DPI)": 300}
        for (text, value) in modes.items():
            ttk.Radiobutton(quality_frame, text=text, variable=self.quality_var, value=text.split(' ')[0]).pack(anchor=tk.W, padx=5)
        self.quality_map = {key.split(' ')[0]: value for key, value in modes.items()}

        self.start_button = ttk.Button(control_frame, text="Bước 4: Bắt Đầu Dịch", command=self.start_translation_thread, style="Accent.TButton")
        self.start_button.grid(row=2, column=0, pady=10, ipady=5, sticky="ew")
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        stats_panel = ttk.LabelFrame(main_frame, text="Thông số")
        stats_panel.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        stats_panel.columnconfigure(0, weight=1)
        stats_panel.columnconfigure(1, weight=1)
        stats_panel.columnconfigure(2, weight=1)
        stats_panel.columnconfigure(3, weight=1)

        self.filesize_var = tk.StringVar(value="Dung lượng: N/A")
        ttk.Label(stats_panel, textvariable=self.filesize_var).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.page_var = tk.StringVar(value="Trang: N/A")
        ttk.Label(stats_panel, textvariable=self.page_var).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.elapsed_var = tk.StringVar(value="Thời gian trôi qua: 0:00:00")
        ttk.Label(stats_panel, textvariable=self.elapsed_var).grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.etr_var = tk.StringVar(value="Ước tính còn lại: N/A")
        ttk.Label(stats_panel, textvariable=self.etr_var).grid(row=0, column=3, padx=5, pady=2, sticky="w")

        log_frame = ttk.LabelFrame(main_frame, text="Nhật ký chi tiết")
        log_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state="disabled", height=5)
        self.log_text.pack(fill=tk.X, expand=True)

        progress_frame = ttk.LabelFrame(main_frame, text="Tiến Độ Tổng Thể")
        progress_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, expand=True, padx=5, pady=5)

        image_frame = ttk.LabelFrame(main_frame, text="Xem Trực Tiếp")
        image_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.image_label = ttk.Label(image_frame, text="Bản dịch sẽ được hiển thị ở đây...")
        self.image_label.pack(expand=True)
        self.photo = None

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_image(self, pil_image):
        w, h = pil_image.size
        max_h = 350
        if h > max_h:
            ratio = max_h / h
            new_w = int(w * ratio)
            new_h = max_h
            pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=self.photo, text="")

    def update_progress(self, value):
        self.progress_bar['value'] = value

    def update_stats(self, stats_dict):
        self.page_var.set(f"Trang: {stats_dict.get('page', 'N/A')}")
        self.elapsed_var.set(f"Thời gian trôi qua: {stats_dict.get('elapsed', '0:00:00')}")
        self.etr_var.set(f"Ước tính còn lại: {stats_dict.get('etr', 'N/A')}")
        self.root.update_idletasks()

    def select_file(self):
        filepath = filedialog.askopenfilename(title="Chọn file PDF", filetypes=(("PDF files", "*.pdf"), ("Tất cả file", "*.*")))
        if filepath:
            self.filepath_var.set(filepath)
            self.log(f"Đã chọn file: {os.path.basename(filepath)}")
            try:
                size_in_bytes = os.path.getsize(filepath)
                size_in_mb = size_in_bytes / (1024 * 1024)
                self.filesize_var.set(f"Dung lượng: {size_in_mb:.2f} MB")
            except Exception as e:
                self.filesize_var.set("Dung lượng: Lỗi")
                self.log(f"Không thể lấy dung lượng file: {e}")

    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.browse_button.config(state=state)
        self.start_button.config(state=state)

    def start_translation_thread(self):
        input_path = self.filepath_var.get()
        if not input_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn một file PDF để dịch!")
            return
        
        try:
            doc = fitz.open(input_path)
            total_pages = len(doc)
            doc.close()
            self.progress_bar['maximum'] = total_pages
            self.progress_bar['value'] = 0
            self.update_stats({"page": f"0 / {total_pages}", "elapsed": "0:00:00", "etr": "N/A"})
        except Exception as e:
            messagebox.showerror("Lỗi đọc file", f"Không thể đọc file PDF.\nLỗi: {e}")
            return

        target_lang_code = self.languages[self.lang_var.get()]
        quality_dpi = self.quality_map[self.quality_var.get()]

        self.set_ui_state(False)
        self.log("--- BẮT ĐẦU QUÁ TRÌNH DỊCH CHUYÊN NGHIỆP ---")

        thread = threading.Thread(
            target=run_visual_translation_process,
            args=(input_path, target_lang_code, quality_dpi, self.log, self.update_image, self.update_progress, self.update_stats, lambda: self.set_ui_state(True))
        )
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

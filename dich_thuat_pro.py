import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time

# Các thư viện xử lý file, ảnh và dịch thuật
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageTk, ImageFont
import pytesseract
from deep_translator import GoogleTranslator

# --- CẤU HÌNH QUAN TRỌNG ---
try:
    pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
except Exception:
    print("LƯU Ý: Không tìm thấy Tesseract ở đường dẫn mặc định. Vui lòng chỉnh sửa đường dẫn trong code.")

# --- CÁC HÀM LÕI XỬ LÝ DỊCH THUẬT (BACKEND) ---

def run_visual_translation_process(input_path, target_lang, status_callback, image_update_callback, enable_ui_callback):
    """
    Hàm chính chạy trong một luồng riêng để không làm treo giao diện.
    Thực hiện dịch thuật dựa trên hình ảnh.
    """
    try:
        doc = fitz.open(input_path)
        translated_pages_images = []

        for page_num in range(len(doc)):
            status_callback(f"--- Đang xử lý trang {page_num + 1}/{len(doc)} ---")
            
            status_callback("Bước 1: Chuyển đổi trang thành hình ảnh...")
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            draw = ImageDraw.Draw(img)

            status_callback("Bước 2: Nhận dạng văn bản và vị trí (OCR)...")
            ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng+vie')
            
            num_boxes = len(ocr_data['level'])
            boxes_to_process = []
            
            # ==================================================================
            # THAY ĐỔI LỚN: Dịch từng đoạn một thay vì gộp chung
            # ==================================================================
            status_callback("Bước 3: Bắt đầu dịch từng cụm từ (sẽ chậm hơn)...")
            translator = GoogleTranslator(source='auto', target=target_lang)
            
            for i in range(num_boxes):
                if int(ocr_data['conf'][i]) > 60:
                    text = ocr_data['text'][i].strip()
                    h = ocr_data['height'][i]

                    if text and h > 1:
                        (x, y, w) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i])
                        
                        # Dịch ngay lập tức
                        try:
                            translated_text = translator.translate(text)
                            if not translated_text: # Nếu dịch ra rỗng, giữ lại text gốc
                                translated_text = text
                        except Exception as e:
                            status_callback(f"Lỗi dịch nhỏ: {e}. Giữ lại text gốc.")
                            translated_text = text # Giữ lại text gốc nếu có lỗi
                        
                        # Thêm vào danh sách để vẽ lại sau
                        boxes_to_process.append({'box': (x, y, w, h), 'text': translated_text})
                        
                        # Cập nhật log thường xuyên hơn
                        if len(boxes_to_process) % 10 == 0:
                            status_callback(f"Đã dịch {len(boxes_to_process)} cụm từ...")

            # ==================================================================
            
            status_callback("Bước 4: Tái tạo lại trang đã dịch...")
            for item in boxes_to_process:
                (x, y, w, h) = item['box']
                translated_text = item['text']
                
                draw.rectangle([x, y, x + w, y + h], fill='white', outline='white')
                
                try:
                    font_size = int(h * 0.8)
                    font = ImageFont.truetype("arial.ttf", size=max(1, font_size))
                except IOError:
                    font = ImageFont.load_default()
                
                draw.text((x, y), translated_text, font=font, fill='black')

            status_callback("Bước 5: Cập nhật giao diện...")
            image_update_callback(img)
            translated_pages_images.append(img)
            time.sleep(0.1) # Giảm thời gian nghỉ

        if translated_pages_images:
            status_callback("Bước 6: Lưu tất cả các trang đã dịch vào file PDF mới...")
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_dich_visual.pdf"
            
            translated_pages_images[0].save(
                output_path,
                save_all=True,
                append_images=translated_pages_images[1:]
            )
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
# (Phần giao diện không thay đổi)
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Dịch Thuật Giữ Định Dạng (v3.2 - Ổn định)")
        self.root.geometry("800x700")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        control_frame.columnconfigure(0, weight=1)

        file_frame = ttk.LabelFrame(control_frame, text="Bước 1: Chọn File PDF Cần Dịch")
        file_frame.grid(row=0, column=0, sticky="ew", pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.filepath_var = tk.StringVar()
        self.filepath_entry = ttk.Entry(file_frame, textvariable=self.filepath_var, state="readonly")
        self.filepath_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.browse_button = ttk.Button(file_frame, text="Chọn File...", command=self.select_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        lang_frame = ttk.LabelFrame(control_frame, text="Bước 2: Chọn Ngôn Ngữ Đích")
        lang_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.languages = {"Tiếng Việt": "vi", "Tiếng Anh": "en", "Tiếng Nhật": "ja", "Tiếng Hàn": "ko", "Tiếng Trung (Giản thể)": "zh-cn"}
        self.lang_var = tk.StringVar(value="Tiếng Việt")
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=list(self.languages.keys()), state="readonly")
        lang_menu.pack(padx=5, pady=5, fill=tk.X)

        self.start_button = ttk.Button(control_frame, text="Bước 3: Bắt Đầu Dịch", command=self.start_translation_thread)
        self.start_button.grid(row=2, column=0, pady=10, sticky="ew")

        log_frame = ttk.LabelFrame(main_frame, text="Tiến Trình Dịch")
        log_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state="disabled", height=8)
        self.log_text.pack(fill=tk.X, expand=True)

        image_frame = ttk.LabelFrame(main_frame, text="Xem Trực Tiếp")
        image_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
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
        max_h = 400
        if h > max_h:
            ratio = max_h / h
            new_w = int(w * ratio)
            new_h = max_h
            pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        self.photo = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=self.photo, text="")
        self.image_label.image = self.photo

    def select_file(self):
        filepath = filedialog.askopenfilename(title="Chọn file PDF", filetypes=(("PDF files", "*.pdf"), ("Tất cả file", "*.*")))
        if filepath:
            self.filepath_var.set(filepath)
            self.log(f"Đã chọn file: {os.path.basename(filepath)}")

    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.browse_button.config(state=state)
        self.start_button.config(state=state)

    def start_translation_thread(self):
        input_path = self.filepath_var.get()
        if not input_path:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn một file PDF để dịch!")
            return

        target_lang_name = self.lang_var.get()
        target_lang_code = self.languages[target_lang_name]

        self.set_ui_state(False)
        self.log("--- BẮT ĐẦU QUÁ TRÌNH DỊCH HÌNH ẢNH ---")

        thread = threading.Thread(
            target=run_visual_translation_process,
            args=(input_path, target_lang_code, self.log, self.update_image, lambda: self.set_ui_state(True))
        )
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
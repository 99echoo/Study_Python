import tkinter as tk
from tkinter import messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk, ImageDraw
import random

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(900 / page.rect.width, 600 / page.rect.height))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)

    return pages

def show_random_page(pages):
    if pages:
        random_index = random.randint(0, len(pages) - 1)
        random_page = pages.pop(random_index)
        return random_page
    else:
        return None

class PDFPageViewerApp(tk.Tk):
    def __init__(self, pages):
        super().__init__()
        self.title("이걸왜외우고잇지ㅔㅛ")
        self.pages = pages
        self.current_page = None
        self.original_page = None
        self.label_page = tk.Label(self)
        self.label_page.pack(pady=20)
        self.button_next = tk.Button(self, text="Show Random Page", command=self.next_page)
        self.button_next.pack(pady=20)
        self.button_reveal = tk.Button(self, text="Reveal Answer", command=self.reveal_answer)
        self.button_reveal.pack(pady=20)
        self.next_page()

    def next_page(self):
        if self.pages:
            self.original_page = show_random_page(self.pages)
            if self.original_page:
                self.current_page = self.original_page.copy()
                draw = ImageDraw.Draw(self.current_page)
                draw.rectangle([0, 0, 700, 100], fill="black")
                img_tk = ImageTk.PhotoImage(self.current_page)
                self.label_page.configure(image=img_tk)
                self.label_page.image = img_tk
            else:
                messagebox.showinfo("End", "No more pages left.")
                self.quit()
        else:
            messagebox.showinfo("End", "No more pages left.")
            self.quit()

    def reveal_answer(self):
        if self.current_page and self.original_page:
            img_tk = ImageTk.PhotoImage(self.original_page)
            self.label_page.configure(image=img_tk)
            self.label_page.image = img_tk

# 사용 예시
pdf_path = "C:/Users/user/Desktop/2024-1/생활 원예/원예식물 100가지.pdf"
pages = extract_pages(pdf_path)
if pages:
    app = PDFPageViewerApp(pages)
    app.mainloop()
else:
    print("No pages found in the PDF.")
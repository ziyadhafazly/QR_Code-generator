import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from datetime import datetime
import os
from PIL import Image, ImageTk

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#f0f0f0')
        style.configure('Custom.TLabel', background='#f0f0f0', font=('Helvetica', 12))
        
        # Main container
        main_frame = ttk.Frame(root, style='Custom.TFrame', padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="QR Code Generator", 
                               font=('Helvetica', 20, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        input_label = ttk.Label(input_frame, text="Enter URL or Text:")
        input_label.pack()
        
        self.text_input = ttk.Entry(input_frame, width=50, font=('Helvetica', 11))
        self.text_input.pack(pady=10, ipady=5)
        
        # Generate button
        self.generate_btn = tk.Button(input_frame, 
                                    text="Generate QR Code",
                                    font=('Helvetica', 11, 'bold'),
                                    bg='#2196f3',
                                    fg='white',
                                    activebackground='#1976d2',
                                    cursor='hand2',
                                    relief=tk.FLAT,
                                    pady=10,
                                    padx=20,
                                    command=self.generate_qr)
        self.generate_btn.pack(pady=10)
        
        # Preview frame
        self.preview_frame = ttk.Frame(main_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.preview_label = ttk.Label(self.preview_frame, text="QR Code Preview")
        self.preview_label.pack()
        
        self.qr_preview = ttk.Label(self.preview_frame)
        self.qr_preview.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, 
                                     text="Ready to generate QR code",
                                     font=('Helvetica', 10),
                                     foreground='#666666')
        self.status_label.pack()

    def generate_qr(self):
        data = self.text_input.get().strip()
        
        if not data:
            self.status_label.configure(text="Error: Please enter URL or text", foreground='#f44336')
            messagebox.showerror("Error", "Please enter URL or text")
            return
            
        try:
            self.status_label.configure(text="Generating QR code...", foreground='#2196f3')
            self.root.update()
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            filename = f"qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            qr_image.save(filename)
            
            # Display preview
            preview_size = (300, 300)
            qr_image_resized = qr_image.resize(preview_size, Image.Resampling.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_image_resized)
            self.qr_preview.configure(image=qr_photo)
            self.qr_preview.image = qr_photo
            
            self.status_label.configure(
                text=f"Success! QR Code saved as {filename}",
                foreground='#4caf50'
            )
            self.text_input.delete(0, tk.END)
            
        except Exception as e:
            self.status_label.configure(
                text=f"Error: {str(e)}", 
                foreground='#f44336'
            )
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog


def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
    if file_path:
        image_path.set(file_path)
        resize_button.config(state="normal")


# App window
app = tk.Tk()
app.title("Image Resizer")
app.geometry("400x300")

# StringVars
image_path = tk.StringVar(value="No file selected")

# UI Elements
tk.Label(app, text="Image Resizer", font=("Helvetica", 16)).pack(pady=10)

tk.Button(app, text="Choose Image", command=choose_image).pack()
tk.Label(app, textvariable=image_path, wraplength=350).pack(pady=5)

tk.Label(app, text="Width:").pack()
width_entry = tk.Entry(app)
width_entry.pack()

tk.Label(app, text="Height:").pack()
height_entry = tk.Entry(app)
height_entry.pack()

resize_button = tk.Button(app, text="Resize & Save", state="disabled")
resize_button.pack(pady=10)

# Run
app.mainloop()

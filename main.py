import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def choose_image():
    global target_size_label
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
    if file_path:
        image_path.set(file_path)
        resize_button.config(state="normal")

        # Load and resize image for preview
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Keep aspect ratio
        preview_img = ImageTk.PhotoImage(img)

        # Prevent garbage collection
        preview_label.image = preview_img
        preview_label.config(image=preview_img)

        # Original image size
        original_width, original_height = img.size
        original_size_label.config(text=f"Original: {original_width} x {original_height}")

        # Target size
        target_size_label = tk.Label(app, text="New: -")
        target_size_label.pack()


def resize_image():
    if not image_path.get():
        messagebox.showerror("No Image", "Please choose an image before resizing.")
        return

    if not width_entry.get() or not height_entry.get():
        messagebox.showerror("Missing Input", "Please enter both width and height.")
        return

    try:
        width = int(width_entry.get())
        height = int(height_entry.get())

        target_size_label.config(text=f"New: {width} x {height}")

        img = Image.open(image_path.get())
        print(f"Opened image: {img.format}, Size: {img.size}")

        resized_img = img.resize((width, height))
        print(f"Image resized to: {resized_img.size}")

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("WEBP", "*.webp")]
        )

        if save_path:
            resized_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Resize Failed", f"Something went wrong:\n{str(e)}")


# App window
app = tk.Tk()
app.title("Image Resizer")
app.geometry("500x600")

# StringVars
image_path = tk.StringVar(value="No file selected")
target_size_label = None

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


def update_target_label(*args):
    if width_entry.get().isdigit() and height_entry.get().isdigit():
        target_size_label.config(text=f"New: {width_entry.get()} x {height_entry.get()}")
    else:
        target_size_label.config(text="New: -")


width_entry.bind("<KeyRelease>", update_target_label)
height_entry.bind("<KeyRelease>", update_target_label)

resize_button = tk.Button(app, text="Resize & Save", state="disabled", command=resize_image)
resize_button.pack(pady=10)

# Preview image
preview_label = tk.Label(app)
preview_label.pack(pady=10)

original_size_label = tk.Label(app, text="")
original_size_label.pack()

# Run
app.mainloop()

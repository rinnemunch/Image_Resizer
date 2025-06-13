import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tkinter.font as tkFont


def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
    if file_path:
        image_path.set(file_path)
        resize_button.config(state="normal")

        img = Image.open(file_path)
        preview = img.copy()
        preview.thumbnail((150, 150))
        preview_img = ImageTk.PhotoImage(preview)

        preview_label.image = preview_img
        preview_label.config(image=preview_img)

        # Original image size
        original_width, original_height = img.size
        original_size_label.config(text=f"Original: {original_width} x {original_height}")

        update_target_label()


def resize_image():
    if not image_path.get():
        messagebox.showerror("No Image", "Please choose an image before resizing.")
        return

    try:
        img = Image.open(image_path.get())
        orig_w, orig_h = img.size

        if scale_entry.get().isdigit():
            percent = int(scale_entry.get())
            width = int(orig_w * (percent / 100))
            height = int(orig_h * (percent / 100))
        else:
            if keep_aspect.get():
                if width_entry.get().isdigit():
                    width = int(width_entry.get())
                    height = int(orig_h * (width / orig_w))
                elif height_entry.get().isdigit():
                    height = int(height_entry.get())
                    width = int(orig_w * (height / orig_h))
                else:
                    messagebox.showerror("Missing Input", "Enter width or height to maintain aspect ratio.")
                    return
            else:
                if not width_entry.get().isdigit() or not height_entry.get().isdigit():
                    messagebox.showerror("Missing Input", "Please enter both width and height.")
                    return
                width = int(width_entry.get())
                height = int(height_entry.get())

        target_size_label.config(text=f"New: {width} x {height}")

        resized_img = img.resize((width, height))
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
app.configure(bg="#FFA552")
press_start_font = tkFont.Font(family="Press Start 2P", size=8)

# StringVars
image_path = tk.StringVar(value="No file selected")
target_size_label = None

# UI Elements
tk.Label(app, text="Image Resizer", font=("Helvetica", 20, "bold"), bg="#FFA552", fg="white").pack(pady=(20, 10))

tk.Button(app, text="Choose Image", command=choose_image, bg="lightgray", fg="black").pack()

tk.Label(app, textvariable=image_path, wraplength=350, bg="#FFA552", fg="white", anchor="center").pack(pady=5)

tk.Label(app, text="Width:", bg="#FFA552", fg="white").pack(pady=(10, 2))
width_entry = tk.Entry(app,
                       bg="#FFF5E1", fg="black",
                       insertbackground="black",
                       disabledbackground="#FFA552",
                       disabledforeground="white"
                       )
width_entry.pack(pady=(0, 10))

tk.Label(app, text="Height:", bg="#FFA552", fg="white").pack(pady=(10, 2))
height_entry = tk.Entry(app,
                        bg="#FFF5E1", fg="black",
                        insertbackground="black",
                        disabledbackground="#FFA552",
                        disabledforeground="white"
                        )
height_entry.pack(pady=(0, 10))

target_size_label = tk.Label(app, text="New: -")
target_size_label.pack(pady=(2, 10))

tools_frame = tk.Frame(app)
tools_frame.pack(pady=5)
tools_frame.pack_forget()


def update_target_label(*args):
    if target_size_label is None or not image_path.get():
        return

    try:
        img = Image.open(image_path.get())
        orig_w, orig_h = img.size

        if keep_aspect.get():
            if width_entry.get().isdigit():
                width = int(width_entry.get())
                height = int(orig_h * (width / orig_w))
                target_size_label.config(text=f"New: {width} x {int(height)}")
            elif height_entry.get().isdigit():
                height = int(height_entry.get())
                width = int(orig_w * (height / orig_h))
                target_size_label.config(text=f"New: {int(width)} x {height}")
            else:
                target_size_label.config(text="New: -")
        else:
            if width_entry.get().isdigit() and height_entry.get().isdigit():
                target_size_label.config(text=f"New: {width_entry.get()} x {height_entry.get()}")
            else:
                target_size_label.config(text="New: -")
    except:
        target_size_label.config(text="New: -")


width_entry.bind("<KeyRelease>", update_target_label)
height_entry.bind("<KeyRelease>", update_target_label)

resize_button = tk.Button(app, text="Resize & Save", state="disabled", command=resize_image)
resize_button.pack(pady=10)

# Preview image
preview_label = tk.Label(app)
preview_label.pack(pady=10)

original_size_label = tk.Label(app, text="")
original_size_label.pack(pady=(5, 0))


def toggle_aspect_lock():
    if keep_aspect.get():
        width_entry.config(state="normal")
        height_entry.config(state="disabled")
    else:
        width_entry.config(state="normal")
        height_entry.config(state="normal")
    update_target_label()


# Tools
keep_aspect = tk.BooleanVar(value=True)
tk.Checkbutton(tools_frame, text="Keep Aspect Ratio", variable=keep_aspect, command=toggle_aspect_lock,
               bg="lightgray", fg="black", selectcolor="lightgray", activebackground="lightgray").pack(anchor="w",
                                                                                                       padx=10, pady=2)
tk.Label(tools_frame, text="Scale by %:", bg="lightgray", fg="black").pack(anchor="w", padx=10)
scale_entry = tk.Entry(tools_frame, width=10)
scale_entry.pack(anchor="w", padx=10, pady=(0, 10))


def toggle_tools():
    if tools_frame.winfo_ismapped():
        tools_frame.pack_forget()
        tools_button.config(text="Tools ▼")
    else:
        tools_frame.pack()
        tools_button.config(text="Tools ▲")


tools_button = tk.Button(app, text="Tools ▼", command=toggle_tools)
tools_button.pack(pady=5)

toggle_aspect_lock()
update_target_label()

print(tkFont.families())

# Run
app.mainloop()

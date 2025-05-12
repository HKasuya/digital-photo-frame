import tkinter as tk
import tkinter.filedialog as fd
import random
from pathlib import Path
from PIL import Image, ImageTk

photo = []
root = None
cv = None
btn = None
btn_visible = True
hide_timer = None
hidden = 3000
random_index = 0
current_photoimage = None


def load_images(folder_path):
    global photo, cv, btn
    filetype = [".png", ".jpg", ".jpeg"]
    image_files = [
        str(f)
        for f in Path(folder_path).iterdir()
        if f.is_file() and f.suffix.lower() in filetype
    ]
    for filename in image_files:
        try:
            img = Image.open(filename)
            photo.append(img)
        except tk.TclError as error:
            print(f"Error image : {filename} - {error}")
    if photo:
        photograph_next_image()
        if btn and btn_visible:
            start_hidetimer()
    else:
        cv.delete("PH")
        tk.messagebox.showinfo(
            "フォルダinfo", "選択されたフォルダに画像が見つかりません。"
        )
        show_button()


def photograph_next_image():
    global root, cv, photo, current_photoimage, random_index
    cv.delete("PH")
    if photo:
        random_index = random.randint(0, len(photo) - 1)
        random_photo = photo[random_index]
        width = cv.winfo_width()
        height = cv.winfo_height()
        resize_image = random_photo.resize((width, height))
        img = ImageTk.PhotoImage(resize_image)
        current_photoimage = img  # オブジェクトへの参照を維持
        cv.image = img
        cv.create_image(0, 0, image=img, anchor="nw", tag="PH")
        root.after(7000, photograph_next_image)


def resize_current_image(event):
    global root, cv, photo, current_photoimage, random_index
    cv.delete("PH")
    if photo:
        random_index = random.randint(0, len(photo) - 1)
        random_photo = photo[random_index]
        resize_width = event.width
        resize_height = event.height
        resize_image = random_photo.resize((resize_width, resize_height))
        img = ImageTk.PhotoImage(resize_image)
        current_photoimage = img  # オブジェクトへの参照を維持
        cv.image = img
        cv.create_image(0, 0, image=img, anchor="nw", tag="PH")


def openFile():
    fpath = fd.askdirectory()
    if fpath:
        load_images(fpath)


def hide_button():
    global btn, btn_visible
    if btn.winfo_ismapped():
        btn.place_forget()
        btn_visible = False


def show_button(event):
    global btn, btn_visible, hide_timer
    if not btn.winfo_ismapped():
        btn.place(x=0, y=0)
        btn_visible = True
    if hide_timer:
        root.after_cancel(hide_timer)
        hide_timer = None
    start_hidetimer()


def start_hidetimer():
    global btn, hide_timer
    if btn.winfo_ismapped():
        hide_timer = root.after(hidden, hide_button)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("デジタルフォトフレーム")
    # 起動時にウィンドウを最大化（キャンバスはまだ変わらず）
    root.state("zoomed")
    # ウィンドウのリサイズの許可
    root.resizable(True, True)
    cv = tk.Canvas(root, width=800, height=600)
    # キャンバスサイズをウィンドウサイズに常に適応する
    cv.pack(fill=tk.BOTH, expand=True)
    cv.bind("<Configure>", resize_current_image)

    btn = tk.Button(
        root, text="フォルダを選択してください。", font="Arial,10", command=openFile
    )
    btn.place(x=250, y=350)

    cv.create_text(
        400,
        300,
        text="『フォルダを選択』を押して画像フォルダを選択してください。",
        font=("Arial", 16),
    )

    root.bind("<Motion>", show_button)

    root.mainloop()

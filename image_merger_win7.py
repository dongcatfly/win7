import math
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}

def resize_keep_ratio(img, max_width):
    if max_width and max_width > 0 and img.width > max_width:
        new_h = int(img.height * max_width / img.width)
        return img.resize((max_width, new_h), Image.LANCZOS)
    return img

def merge_images(paths, output, mode, columns, spacing, background, quality, max_width):
    images = []
    for path in paths:
        img = Image.open(path)
        img = img.convert("RGBA")
        img = resize_keep_ratio(img, max_width)
        images.append(img)

    if not images:
        raise ValueError("没有可合并的图片")

    bg = tuple(int(background[i:i+2], 16) for i in (1, 3, 5)) + (255,)

    if mode == "vertical":
        width = max(i.width for i in images)
        height = sum(i.height for i in images) + spacing * (len(images) - 1)
        canvas = Image.new("RGBA", (width, height), bg)
        y = 0
        for img in images:
            canvas.alpha_composite(img, ((width - img.width) // 2, y))
            y += img.height + spacing

    elif mode == "horizontal":
        width = sum(i.width for i in images) + spacing * (len(images) - 1)
        height = max(i.height for i in images)
        canvas = Image.new("RGBA", (width, height), bg)
        x = 0
        for img in images:
            canvas.alpha_composite(img, (x, (height - img.height) // 2))
            x += img.width + spacing

    else:
        columns = max(1, int(columns))
        rows = math.ceil(len(images) / columns)
        cell_w = max(i.width for i in images)
        cell_h = max(i.height for i in images)
        width = columns * cell_w + spacing * (columns - 1)
        height = rows * cell_h + spacing * (rows - 1)
        canvas = Image.new("RGBA", (width, height), bg)
        for n, img in enumerate(images):
            col = n % columns
            row = n // columns
            x = col * (cell_w + spacing) + (cell_w - img.width) // 2
            y = row * (cell_h + spacing) + (cell_h - img.height) // 2
            canvas.alpha_composite(img, (x, y))

    ext = Path(output).suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        canvas = canvas.convert("RGB")
        canvas.save(output, quality=int(quality), optimize=True)
    elif ext == ".webp":
        canvas.save(output, quality=int(quality), method=6)
    else:
        canvas.save(output)

class ImageMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片合并工具 Win7版")
        self.geometry("820x560")
        self.resizable(True, True)

        self.paths = []
        self.mode = tk.StringVar(value="vertical")
        self.columns = tk.IntVar(value=3)
        self.spacing = tk.IntVar(value=20)
        self.quality = tk.IntVar(value=85)
        self.max_width = tk.IntVar(value=1600)
        self.background = tk.StringVar(value="#FFFFFF")
        self.output = tk.StringVar(value=str(Path.home() / "Desktop" / "merged_images.jpg"))

        self.build_ui()

    def build_ui(self):
        title = ttk.Label(self, text="图片合并工具 Win7兼容版", font=("Arial", 18, "bold"))
        title.pack(pady=12)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=20)

        ttk.Button(top, text="选择图片文件", command=self.choose_files).pack(side="left", padx=4)
        ttk.Button(top, text="选择整个文件夹", command=self.choose_folder).pack(side="left", padx=4)
        ttk.Button(top, text="清空列表", command=self.clear_list).pack(side="left", padx=4)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.listbox = tk.Listbox(list_frame)
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scroll.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scroll.set)

        opts = ttk.LabelFrame(self, text="合并设置")
        opts.pack(fill="x", padx=20, pady=5)

        ttk.Label(opts, text="排列方式").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        ttk.Radiobutton(opts, text="竖向长图", variable=self.mode, value="vertical").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(opts, text="横向", variable=self.mode, value="horizontal").grid(row=0, column=2, sticky="w")
        ttk.Radiobutton(opts, text="网格", variable=self.mode, value="grid").grid(row=0, column=3, sticky="w")

        ttk.Label(opts, text="网格列数").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        ttk.Spinbox(opts, from_=1, to=20, textvariable=self.columns, width=8).grid(row=1, column=1, sticky="w")

        ttk.Label(opts, text="图片间距").grid(row=1, column=2, padx=8, pady=6, sticky="w")
        ttk.Spinbox(opts, from_=0, to=300, textvariable=self.spacing, width=8).grid(row=1, column=3, sticky="w")

        ttk.Label(opts, text="最大宽度").grid(row=2, column=0, padx=8, pady=6, sticky="w")
        ttk.Spinbox(opts, from_=0, to=10000, increment=100, textvariable=self.max_width, width=8).grid(row=2, column=1, sticky="w")
        ttk.Label(opts, text="0表示不缩放").grid(row=2, column=2, sticky="w")

        ttk.Label(opts, text="JPG/WebP质量").grid(row=3, column=0, padx=8, pady=6, sticky="w")
        ttk.Spinbox(opts, from_=1, to=100, textvariable=self.quality, width=8).grid(row=3, column=1, sticky="w")

        ttk.Label(opts, text="背景颜色").grid(row=3, column=2, padx=8, pady=6, sticky="w")
        ttk.Entry(opts, textvariable=self.background, width=12).grid(row=3, column=3, sticky="w")
        ttk.Button(opts, text="选择颜色", command=self.choose_color).grid(row=3, column=4, padx=6)

        out = ttk.Frame(self)
        out.pack(fill="x", padx=20, pady=8)
        ttk.Label(out, text="输出文件").pack(side="left")
        ttk.Entry(out, textvariable=self.output).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(out, text="保存为", command=self.choose_output).pack(side="left")

        ttk.Button(self, text="开始合并", command=self.run_merge).pack(pady=12)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for p in self.paths:
            self.listbox.insert(tk.END, str(p))

    def choose_files(self):
        files = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tif *.tiff")]
        )
        if files:
            for f in files:
                p = Path(f)
                if p.suffix.lower() in IMAGE_EXTENSIONS and p not in self.paths:
                    self.paths.append(p)
            self.refresh_list()

    def choose_folder(self):
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if folder:
            files = sorted([p for p in Path(folder).iterdir()
                            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS])
            self.paths = files
            self.refresh_list()

    def clear_list(self):
        self.paths = []
        self.refresh_list()

    def choose_color(self):
        c = colorchooser.askcolor(color=self.background.get())
        if c and c[1]:
            self.background.set(c[1])

    def choose_output(self):
        path = filedialog.asksaveasfilename(
            title="保存合并后的图片",
            defaultextension=".jpg",
            filetypes=[("JPG图片", "*.jpg"), ("PNG图片", "*.png"), ("WebP图片", "*.webp")]
        )
        if path:
            self.output.set(path)

    def run_merge(self):
        try:
            if not self.paths:
                messagebox.showerror("错误", "请先选择需要合并的图片")
                return
            output = self.output.get().strip()
            if not output:
                messagebox.showerror("错误", "请选择输出文件")
                return
            merge_images(
                self.paths,
                output,
                self.mode.get(),
                self.columns.get(),
                self.spacing.get(),
                self.background.get(),
                self.quality.get(),
                self.max_width.get()
            )
            messagebox.showinfo("完成", "图片合并完成")
        except Exception as e:
            messagebox.showerror("错误", str(e))

if __name__ == "__main__":
    ImageMergerApp().mainloop()

from manim import *
import os
import numpy as np

class Part1LBPIntro(Scene):
    def construct(self):
        MY_BLUE = "#0055FF"
        MY_RED = "#FF0000"
        MY_GREEN = "#00AA00"

        # =========================
        # 1. HELPER: DÒ TÌM ĐƯỜNG DẪN ẢNH THÔNG MINH
        # =========================
        def get_image_path(filename):
            paths_to_try = [
                os.path.join("..", "Data", filename),  
                os.path.join("Data", filename),        
                filename                               
            ]
            for path in paths_to_try:
                if os.path.exists(path):
                    return path
            return filename 

        def get_image(filename, fallback_color, h=4.0):
            try:
                img = ImageMobject(get_image_path(filename))
                img.scale_to_fit_height(h)
                return img
            except:
                return Rectangle(height=h, width=h*0.8).set_fill(fallback_color, 1)

        # =========================
        # 2. NỀN TỔNG THỂ (HCMUS RAW)
        # =========================
        try:
            bg_hcmus = ImageMobject(get_image_path("hcmus.jpg"))
            scale_w = config.frame_width / bg_hcmus.width
            scale_h = config.frame_height / bg_hcmus.height
            bg_hcmus.scale(max(scale_w, scale_h))
            self.add(bg_hcmus)
        except:
            self.camera.background_color = WHITE

        def make_label(text_str, font_size=24, color=WHITE, bg_color=BLACK):
            txt = Text(text_str, font_size=font_size, color=color)
            bg = SurroundingRectangle(txt, color=bg_color, fill_opacity=1, stroke_width=0, buff=0.1)
            return Group(bg, txt)

        # =========================
        # 3. TIÊU ĐỀ LBP LÀ GÌ?
        # =========================
        title = make_label("LBP - Local Binary Patterns", font_size=40, bg_color=BLACK)
        subtitle = make_label("Trích xuất đặc trưng kết cấu khuôn mặt", font_size=20, bg_color=DARK_GRAY)
        title_group = Group(title, subtitle).arrange(DOWN, buff=0.2)
        
        self.play(FadeIn(title_group, shift=UP))
        self.wait(1.5)
        
        self.play(
            title_group.animate.scale(0.7).to_corner(UL),
            run_time=1
        )

        # =========================
        # 4. LOAD ẢNH ĐẦU VÀO (IMAGE_1)
        # =========================
        img_color = get_image("image_1.jpg", BLUE_E, h=4.5)
        img_color.move_to(ORIGIN)
        
        label_step1 = make_label("1. Ảnh Gốc (Input)")
        label_step1.next_to(img_color, DOWN, buff=0.3)

        self.play(FadeIn(img_color, scale=0.8), FadeIn(label_step1), run_time=1.5)
        self.wait(1)

        # =========================
        # 5. CHUYỂN ĐỔI ẢNH XÁM (GRAYSCALE)
        # =========================
        try:
            pixel_array = img_color.get_pixel_array()
            gray_array = np.dot(pixel_array[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
            gray_rgba = np.zeros_like(pixel_array)
            for i in range(3):
                gray_rgba[..., i] = gray_array
            gray_rgba[..., 3] = pixel_array[..., 3] 
            
            img_gray = ImageMobject(gray_rgba)
            img_gray.replace(img_color)
        except:
            img_gray = Rectangle(height=4.5, width=4.5*0.8).set_fill(GRAY, 1).move_to(img_color)

        label_step2 = make_label("2. Chuyển về Ảnh Xám (Grayscale)")
        label_step2.move_to(label_step1)

        self.play(
            FadeOut(img_color), FadeIn(img_gray),
            Transform(label_step1, label_step2),
            run_time=1.5
        )
        self.wait(1)

        # =========================
        # 6. RESIZE 128x156 (CẬP NHẬT TỶ LỆ)
        # =========================
        # Tính toán khung chữ nhật dựa trên tỷ lệ 128:156
        # Giả sử chiều rộng là 3.2 thì chiều cao sẽ là 3.2 * (156/128) = 3.9
        box_w = 3.2
        box_h = 3.9
        
        resize_box = Rectangle(width=box_w, height=box_h, color=MY_RED, stroke_width=4)
        resize_box.move_to(img_gray.get_center())
        
        label_step3 = make_label("3. Resize chuẩn: 128 x 156 pixels", bg_color=MY_RED)
        label_step3.move_to(label_step1)

        self.play(Create(resize_box))
        
        self.play(
            img_gray.animate.stretch_to_fit_width(box_w).stretch_to_fit_height(box_h),
            Transform(label_step1, label_step3),
            run_time=1.5
        )
        self.wait(1)

        # =========================
        # 7. TẠO MA TRẬN LƯỚI PIXEL (KHỚP KHUNG 128x156)
        # =========================
        grid = VGroup()
        n_cols = 16 
        step = box_w / n_cols # Kích thước 1 ô pixel vuông để minh họa
        n_rows = int(box_h / step) # Khoảng 19 ô
        
        # Vẽ các đường dọc
        for i in range(1, n_cols):
            grid.add(Line(
                resize_box.get_corner(UL) + RIGHT * i * step,
                resize_box.get_corner(DL) + RIGHT * i * step,
                color=WHITE, stroke_width=1, stroke_opacity=0.5
            ))
            
        # Vẽ các đường ngang
        for i in range(1, n_rows + 1):
            y_offset = DOWN * i * step
            if y_offset[1] >= -box_h: # Tránh vẽ tràn ra ngoài mép dưới
                grid.add(Line(
                    resize_box.get_corner(UL) + y_offset,
                    resize_box.get_corner(UR) + y_offset,
                    color=WHITE, stroke_width=1, stroke_opacity=0.5
                ))

        label_step4 = make_label("Ma trận các con số Pixel", bg_color=MY_BLUE)
        label_step4.move_to(label_step1)

        self.play(
            Create(grid, lag_ratio=0.02),
            Transform(label_step1, label_step4),
            run_time=2
        )
        self.wait(2)
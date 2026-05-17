from manim import *
import numpy as np
import os

class Part3TimeTravel(Scene):
    def construct(self):
        MY_CYAN = "#00FFFF"
        MY_RED = "#FF0000"
        MY_YELLOW = "#FFD700"
        MY_GREEN = "#00AA00"

        # =========================
        # 0. NỀN TỔNG THỂ (HCMUS BACKGROUND)
        # =========================
        def get_image_path(filename):
            paths_to_try = [os.path.join("..", "Data", filename), os.path.join("Data", filename), filename]
            for path in paths_to_try:
                if os.path.exists(path): return path
            return filename 

        try:
            bg_hcmus = ImageMobject(get_image_path("hcmus.jpg"))
            scale_w = config.frame_width / bg_hcmus.width
            scale_h = config.frame_height / bg_hcmus.height
            bg_hcmus.scale(max(scale_w, scale_h)).set_z_index(-10)
            self.add(bg_hcmus)
        except:
            self.camera.background_color = DARK_BLUE # Fallback

        def fit_img(filename, h=3.5, fallback_color=GRAY):
            try:
                img = ImageMobject(get_image_path(filename))
                img.scale_to_fit_height(h)
                return img
            except:
                return Rectangle(height=h, width=h*1.2).set_fill(fallback_color, 0.8)

        def make_label(text_str, font_size=18, color=WHITE, bg_color=BLACK):
            txt = Text(text_str, font_size=font_size, color=color, weight=BOLD)
            bg = SurroundingRectangle(txt, color=bg_color, fill_opacity=0.85, stroke_width=0, buff=0.15, corner_radius=0.1)
            return Group(bg, txt)

        # HÀM CHUYỂN ẢNH SANG GRAYSCALE CHUẨN
        def convert_to_gray(img_color):
            try:
                pixel_array = img_color.get_pixel_array()
                gray_array = np.dot(pixel_array[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
                gray_rgba = np.zeros_like(pixel_array)
                for i in range(3):
                    gray_rgba[..., i] = gray_array
                gray_rgba[..., 3] = pixel_array[..., 3] 
                
                img_gray = ImageMobject(gray_rgba)
                img_gray.replace(img_color)
                return img_gray
            except:
                fallback = Rectangle(height=img_color.height, width=img_color.width).set_fill(GRAY, 1)
                fallback.move_to(img_color)
                return fallback

        # =========================
        # 1. TÁI TẠO CẢNH CUỐI PHẦN 2 (NĂM 2026)
        # =========================
        title_text = Text("CHIẾC HỘP ĐEN CỦA TRÍ TUỆ NHÂN TẠO", font_size=28, color=MY_YELLOW, weight=BOLD)
        title_bg = SurroundingRectangle(title_text, color=BLACK, fill_color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.15, corner_radius=0.1)
        title_grp = Group(title_bg, title_text).to_edge(UP, buff=0.4)

        img_blackbox_jpg = fit_img("blackbox.jpg", h=3.5, fallback_color=BLACK).move_to(ORIGIN)
        lbl_deep = make_label("Deep Learning / Neural Networks", font_size=20).next_to(img_blackbox_jpg, DOWN, buff=0.3)
        warning_question = make_label("?", font_size=150, color=MY_RED, bg_color=None)
        warning_question[0].set_stroke(opacity=0).set_fill(opacity=0)
        warning_question.move_to(img_blackbox_jpg.get_center())

        img_input = fit_img("TBN.jpg", h=2.2)
        lbl_input = make_label("Input", font_size=16).next_to(img_input, DOWN, buff=0.1)
        grp_input = Group(img_input, lbl_input).move_to(LEFT * 5)
        
        img_output = fit_img("TBN.jpg", h=2.2, fallback_color=GREEN_E)
        tag_name = make_label("Trần Bình An", 16).next_to(img_output, UP, buff=0.1) 
        lbl_out_tag = make_label("Output", 16).next_to(img_output, DOWN, buff=0.1)
        grp_output = Group(img_output, tag_name, lbl_out_tag).move_to(RIGHT * 5)

        arrow_in = Arrow(start=grp_input.get_right(), end=img_blackbox_jpg.get_left(), color=MY_RED, stroke_width=8, buff=0.1)
        arrow_out = Arrow(start=img_blackbox_jpg.get_right(), end=grp_output.get_left(), color=MY_RED, stroke_width=8, buff=0.1)

        stuff_to_fade = Group(title_grp, grp_input, grp_output, arrow_in, arrow_out, lbl_deep)
        self.add(stuff_to_fade, img_blackbox_jpg, warning_question)
        self.wait(1)

        # =========================
        # 2. ĐỒNG HỒ QUAY VỀ 1991 (CHẬM & RÕ RÀNG)
        # =========================
        self.play(FadeOut(warning_question), run_time=1)

        clock_face = Circle(radius=0.7, color=MY_CYAN, stroke_width=4).move_to(ORIGIN)
        clock_center = Dot(ORIGIN, color=MY_CYAN)
        clock_hand = Line(ORIGIN, UP*0.5, color=WHITE, stroke_width=4)
        clock_grp = VGroup(clock_face, clock_center, clock_hand)

        year_tracker = ValueTracker(2026)
        year_num = Integer(2026, font_size=40, color=MY_YELLOW).next_to(clock_face, DOWN, buff=0.2)
        year_num.add_updater(lambda m: m.set_value(int(year_tracker.get_value())))

        self.play(FadeIn(clock_grp), FadeIn(year_num), run_time=1)

        self.play(year_num.animate.scale(1.5).set_color(MY_RED), run_time=1)

        lbl_classical = make_label("Classical Methods (Handcrafted Features)", font_size=18, color=MY_CYAN).move_to(lbl_deep.get_center())

        self.play(
            Rotate(clock_hand, angle=-TAU * 5, about_point=clock_center.get_center()),
            year_tracker.animate.set_value(1991), 
            Transform(lbl_deep, lbl_classical),   
            run_time=4, rate_func=rate_functions.ease_in_out_sine
        )
        self.play(Flash(year_num, color=MY_RED, line_length=0.6))
        self.wait(1)

        # =========================
        # 3. INPUT/OUTPUT CHUYỂN XÁM THẬT & HIỆN MATH_BOX
        # =========================
        gray_in = convert_to_gray(img_input)
        gray_out = convert_to_gray(img_output)
        
        title_gray_in = make_label("Kênh màu xám", font_size=14, color=WHITE, bg_color=GRAY).next_to(img_input, UP, buff=0.1)
        title_gray_out = make_label("Kênh màu xám", font_size=14, color=WHITE, bg_color=GRAY).next_to(img_output, UP, buff=0.1)

        img_math_box = fit_img("math_box.jpg", h=3.5, fallback_color=BLUE_E).move_to(ORIGIN)

        self.play(
            FadeOut(img_input), FadeIn(gray_in),
            FadeOut(img_output), FadeIn(gray_out),
            FadeIn(title_gray_in), FadeIn(title_gray_out),
            FadeOut(clock_grp), FadeOut(year_num), 
            FadeOut(img_blackbox_jpg), FadeIn(img_math_box), 
            run_time=1.5
        )
        
        grp_input.add(gray_in, title_gray_in)
        grp_output.add(gray_out, title_gray_out)
        self.wait(1)

        # =========================
        # 4. MATH_BOX THÀNH BACKGROUND RÕ & HIỆN TBN ĐÃ XÁM
        # =========================
        self.play(
            FadeOut(stuff_to_fade), 
            img_math_box.animate.scale(8).set_opacity(1), 
            run_time=2.5 
        )

        img_tbn_color = fit_img("TBN.jpg", h=5.5).move_to(ORIGIN)
        img_tbn_gray = convert_to_gray(img_tbn_color)
        
        title_gray_big = make_label("Kênh màu xám", font_size=24, color=WHITE, bg_color=GRAY).next_to(img_tbn_gray, UP, buff=0.2)
        grp_tbn_gray = Group(img_tbn_gray, title_gray_big)
        
        question_red = Text("?", font_size=180, color=MY_RED, weight=BOLD).move_to(ORIGIN)
        
        self.play(FadeIn(grp_tbn_gray, scale=0.8), run_time=1.5)
        self.play(FadeIn(question_red, scale=0.5))
        self.play(Flash(question_red, color=MY_RED))
        self.wait(1.5)

        # =========================
        # 5. XÓA DẤU HỎI, HIỆN KÍCH THƯỚC VÀ VẼ GRID
        # =========================
        self.play(FadeOut(question_red), run_time=1)

        dim_text = Text("Kích thước: 128 x 156", font_size=20, color=MY_CYAN, weight=BOLD)
        dim_bg = SurroundingRectangle(dim_text, color=BLACK, fill_opacity=0.7, stroke_width=0, buff=0.1)
        dim_grp = Group(dim_bg, dim_text).next_to(img_tbn_gray, DOWN, buff=0.03)
        self.play(FadeIn(dim_grp, shift=UP))

        rows, cols = 16, 16
        cell_w = img_tbn_gray[0].width / cols
        cell_h = img_tbn_gray[0].height / rows
        grid = VGroup()
        for i in range(rows + 1):
            grid.add(Line(img_tbn_gray[0].get_corner(UL) + DOWN * i * cell_h, img_tbn_gray[0].get_corner(UR) + DOWN * i * cell_h, color=WHITE, stroke_width=3))
        for j in range(cols + 1):
            grid.add(Line(img_tbn_gray[0].get_corner(UL) + RIGHT * j * cell_w, img_tbn_gray[0].get_corner(DL) + RIGHT * j * cell_w, color=WHITE, stroke_width=3))

        self.play(Create(grid), run_time=3) 
        self.wait(1)

        # =========================
        # 6. ZOOM SÂU VÀ HIỆN CÁC CON SỐ TRẮNG
        # =========================
        self.play(FadeOut(dim_grp), FadeOut(title_gray_big)) 
        
        zoom_grp = Group(img_tbn_gray, grid) 
        self.play(zoom_grp.animate.scale(5), run_time=3, rate_func=rate_functions.ease_in_out_sine)
        
        scaled_cell_w = cell_w * 5
        scaled_cell_h = cell_h * 5
        numbers = VGroup()
        
        for i in range(rows//2 - 2, rows//2 + 2):
            for j in range(cols//2 - 2, cols//2 + 2):
                val = np.random.randint(50, 240)
                num = Text(
                    str(val), font_size=32, color="#F2FF00", weight=BOLD, 
                ).move_to(
                    zoom_grp[0].get_corner(UL) + DOWN * (i + 0.5) * scaled_cell_h + RIGHT * (j + 0.5) * scaled_cell_w
                )
                numbers.add(num)

        self.play(Write(numbers), run_time=2.5) 
        self.wait(2.5)

        # =========================
        # 7. HIỆU ỨNG TUA NGƯỢC (REWIND VỀ CẢNH GRAY 1991)
        # =========================
        self.play(FadeOut(numbers), run_time=0.4)
        
        self.play(zoom_grp.animate.scale(0.2), run_time=0.8, rate_func=rate_functions.ease_out_sine)
        
        self.play(FadeOut(grid), run_time=0.6)
        
        self.play(
            FadeOut(img_tbn_gray),
            img_math_box.animate.scale(0.125), 
            FadeIn(stuff_to_fade),
            run_time=1.2 
        )
        self.wait(2)

        # =========================
        # 8. OUTRO PHẦN 3: DỌN DẸP KHUNG HÌNH (TRỪ MATH_BOX VÀ TEXT)
        # =========================
        self.play(
            title_grp.animate.shift(UP * 5),
            grp_input.animate.shift(LEFT * 10),
            arrow_in.animate.shift(LEFT * 10),
            grp_output.animate.shift(RIGHT * 10),
            arrow_out.animate.shift(RIGHT * 10),
            # lbl_deep (hiện đang mang text Classical Methods...) và img_math_box được GIỮ NGUYÊN
            run_time=2,
            rate_func=rate_functions.rush_into
        )
        self.wait(1)
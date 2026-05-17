from manim import *
import os

class Part2BlackBox(Scene):
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

        # =========================
        # HELPER FUNCTIONS
        # =========================
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

        # =========================
        # 1. TIÊU ĐỀ PHẦN 2
        # =========================
        title_text = Text("CHIẾC HỘP ĐEN CỦA TRÍ TUỆ NHÂN TẠO", font_size=28, color=MY_YELLOW, weight=BOLD)
        title_bg = SurroundingRectangle(title_text, color=BLACK, fill_color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.15, corner_radius=0.1)
        title_grp = Group(title_bg, title_text).to_edge(UP, buff=0.4)

        self.play(FadeIn(title_grp, shift=DOWN))

        # =========================
        # 2. SO SÁNH: NÃO NGƯỜI (TRÁI) vs DEEP LEARNING (PHẢI)
        # =========================
        # NÃO NGƯỜI
        img_look = fit_img("P2_look.jpg", h=3.5, fallback_color=BLUE_E)
        lbl_look = make_label("Bộ não con người", font_size=20)
        grp_look = Group(img_look, lbl_look).arrange(DOWN, buff=0.3).move_to(LEFT * 3.5)

        # DEEP LEARNING
        img_deep = fit_img("P2_deeplearn.jpg", h=3.5, fallback_color=PURPLE_E)
        lbl_deep = make_label("Deep Learning / Neural Networks", font_size=20)
        # Tách riêng img và lbl để lát nữa animation độc lập dễ hơn
        img_deep.move_to(RIGHT * 3.5 + UP * 0.3)
        lbl_deep.next_to(img_deep, DOWN, buff=0.3)

        self.play(FadeIn(grp_look, shift=RIGHT), FadeIn(img_deep, shift=LEFT), FadeIn(lbl_deep, shift=LEFT), run_time=1.5)
        self.wait(1)
        
        # Nhấp nháy 2 ảnh để thể hiện sự xử lý
        self.play(Flash(img_look, color=WHITE), Flash(img_deep, color=MY_CYAN))
        self.wait(1)

        # =========================
        # 3. CHUYỂN CẢNH: BỊ HÚT VÀO HỘP ĐEN
        # =========================
        # Lấy ảnh Blackbox để ra giữa
        img_blackbox_jpg = fit_img("blackbox.jpg", h=3.5, fallback_color=BLACK)
        img_blackbox_jpg.move_to(ORIGIN)

        # 1. P2_look bay ra khỏi khung hình
        # 2. P2_deeplearn thu nhỏ và bay vào giữa
        # 3. Blackbox hiện ra ở giữa
        # 4. Text di chuyển xuống dưới chân Blackbox
        self.play(
            FadeOut(grp_look, shift=LEFT * 3),
            FadeIn(img_blackbox_jpg),
            img_deep.animate.scale(0.15).move_to(ORIGIN),
            lbl_deep.animate.next_to(img_blackbox_jpg, DOWN, buff=0.3),
            run_time=1.5
        )
        
        # Nuốt chửng (mất P2_deeplearn)
        self.play(FadeOut(img_deep), run_time=0.3)
        self.wait(0.5)

        # =========================
        # 4. MÔ PHỎNG INPUT -> BLACKBOX -> OUTPUT
        # =========================
        # Input
        img_input = fit_img("TBN.jpg", h=2.2)
        lbl_input = make_label("Input", font_size=16).next_to(img_input, DOWN, buff=0.1)
        grp_input = Group(img_input, lbl_input).move_to(LEFT * 5)
        
        # Output
        img_output = fit_img("TBN.jpg", h=2.2, fallback_color=GREEN_E)
        
        # FIX: Text "Trần Bình An" nằm trên đầu ảnh
        tag_name = make_label("Trần Bình An", 16)
        tag_name.next_to(img_output, UP, buff=0.1) 
        
        lbl_out_tag = make_label("Output", 16).next_to(img_output, DOWN, buff=0.1)
        grp_output = Group(img_output, tag_name, lbl_out_tag).move_to(RIGHT * 5)

        # Mũi tên đỏ siêu to
        arrow_in = Arrow(start=grp_input.get_right(), end=img_blackbox_jpg.get_left(), color=MY_RED, stroke_width=8, buff=0.1)
        arrow_out = Arrow(start=img_blackbox_jpg.get_right(), end=grp_output.get_left(), color=MY_RED, stroke_width=8, buff=0.1)

        # Luồng dữ liệu vào
        self.play(FadeIn(grp_input, shift=RIGHT))
        self.play(GrowArrow(arrow_in))
        
        # Xử lý trong hộp đen: Hiện dấu ? to bự
        warning_question = make_label("?", font_size=150, color=MY_RED, bg_color=None)
        warning_question[0].set_stroke(opacity=0).set_fill(opacity=0) # Tắt nền đen của nhãn
        warning_question.move_to(img_blackbox_jpg.get_center())

        self.play(FadeIn(warning_question, scale=0.5))
        self.play(Flash(warning_question, color=MY_RED, line_length=0.6))
        
        # Luồng dữ liệu ra
        self.play(GrowArrow(arrow_out))
        self.play(FadeIn(grp_output, shift=LEFT))
        self.wait(2.5)

        self.wait(1)
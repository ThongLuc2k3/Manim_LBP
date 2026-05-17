from manim import *
import os
import numpy as np

class Part6LBPLimitations(Scene):
    def construct(self):
        MY_BLUE = "#0055FF"
        MY_RED = "#FF0000"
        MY_GREEN = "#00AA00"
        MY_YELLOW = "#FFD700"

        # =========================
        # 1. HELPER & BACKGROUND
        # =========================
        def get_image_path(filename):
            paths_to_try = [os.path.join("..", "Data", filename), os.path.join("Data", filename), filename]
            for path in paths_to_try:
                if os.path.exists(path): return path
            return filename 

        try:
            bg_hcmus = ImageMobject(get_image_path("hcmus.jpg"))
            scale_w, scale_h = config.frame_width / bg_hcmus.width, config.frame_height / bg_hcmus.height
            bg_hcmus.scale(max(scale_w, scale_h)).set_z_index(-10)
            self.add(bg_hcmus)
        except: self.camera.background_color = WHITE

        def make_label(text_str, font_size=18, color=WHITE, bg_color=BLACK):
            txt = Text(text_str, font_size=font_size, color=color)
            bg = SurroundingRectangle(txt, color=bg_color, fill_opacity=1, stroke_width=0, buff=0.1)
            return VGroup(bg, txt)

        def get_img(filename, h=0.8, pos=ORIGIN):
            try:
                return ImageMobject(get_image_path(filename)).scale_to_fit_height(h).move_to(pos)
            except:
                return Rectangle(width=h*0.8, height=h, color=BLACK).set_fill(GRAY, 1).move_to(pos)

        def create_mini_hist(w=1.5, h=0.5, color=MY_BLUE):
            group = VGroup()
            vals = np.random.uniform(0.2, 1.0, 16)
            bar_w = w / 16 
            for val in vals:
                rect = Rectangle(width=bar_w*0.8, height=val*h, fill_color=color, fill_opacity=0.9, stroke_width=0)
                group.add(rect)
            group.arrange(RIGHT, aligned_edge=DOWN, buff=bar_w*0.2)
            base = Line(group.get_corner(DL) + LEFT*0.1, group.get_corner(DR) + RIGHT*0.1, color=WHITE, stroke_width=2)
            return VGroup(base, group).set_z_index(5)

        # Hàm tự động tạo hiệu ứng trích xuất (Neo vào DƯỚI bức ảnh)
        def extract_features_ui(img_mob, raw_str, norm_str):
            step1_lbl = make_label("Trích xuất Histogram", font_size=14, color=WHITE, bg_color=BLACK).next_to(img_mob, DOWN, buff=0.15).align_to(img_mob, LEFT)
            mini_hist = create_mini_hist(w=1.5, h=0.5).next_to(step1_lbl, DOWN, buff=0.1)
            
            step2_lbl = make_label("Chuyển thành Vector thô", font_size=14, color=WHITE, bg_color=BLACK).move_to(step1_lbl)
            v_raw = make_label(raw_str, font_size=14, color=BLACK, bg_color=MY_YELLOW).move_to(mini_hist)
            
            step3_lbl = make_label("Chuẩn hóa Vector", font_size=14, color=WHITE, bg_color=BLACK).move_to(step2_lbl)
            v_norm = make_label(norm_str, font_size=16, color=BLACK, bg_color=MY_YELLOW).move_to(v_raw).set_z_index(10)
            
            def play_anim():
                self.play(FadeIn(step1_lbl), FadeIn(mini_hist), run_time=0.4)
                self.wait(0.2)
                self.play(ReplacementTransform(step1_lbl, step2_lbl), ReplacementTransform(mini_hist, v_raw), run_time=0.5)
                self.wait(0.2)
                self.play(ReplacementTransform(step2_lbl, step3_lbl), ReplacementTransform(v_raw, v_norm), run_time=0.5)
                return VGroup(step3_lbl, v_norm), v_norm
            return play_anim

        # Hàm tạo bảng công thức ở giữa
        def create_calc_box(title, test_math, db_math, d_val):
            calc_str = r"d = \sqrt{ \sum (p_i - q_i)^2 } = " + f"{d_val:.2f}"
            lines = VGroup(
                Text(title, font_size=16, color=BLACK, weight=BOLD),
                MathTex(test_math, font_size=20, color=MY_RED),
                MathTex(db_math, font_size=20, color=MY_BLUE),
                MathTex(calc_str, font_size=26, color=MY_RED) 
            ).arrange(DOWN, buff=0.15)
            bg = SurroundingRectangle(lines, color=MY_RED, fill_color="#ffe6e6", fill_opacity=1, stroke_width=3, buff=0.2)
            return VGroup(bg, lines).move_to(DOWN * 1.5).set_z_index(20)

        # =========================
        # 2. KHAI BÁO BỐ CỤC
        # =========================
        phase_title = make_label("NHƯỢC ĐIỂM CỦA THUẬT TOÁN LBP (LIMITATIONS)", font_size=22, bg_color=MY_RED).to_edge(UP, buff=0.2).set_z_index(20)
        self.play(FadeIn(phase_title, shift=DOWN))

        img_left_x = -4.5
        img_right_x = 4.5
        img_y = 0.7 

        # --- ẢNH GỐC (TRÁI) ---
        img_6_data = {"img": "image_6.jpg", "raw": "[600, 400, ..., 1500]", "norm": "[0.06, 0.04, ..., 0.15]", "v_math": r"V_{Goc} = [0.06, 0.04, \dots, 0.15]"}
        
        img_left = get_img(img_6_data["img"], h=2.5, pos=[img_left_x, img_y, 0]).set_z_index(5)
        lbl_left = make_label("Ảnh Gốc (Anchor)", font_size=16, color=WHITE, bg_color=MY_GREEN).next_to(img_left, UP, buff=0.1)
        self.play(FadeIn(img_left, shift=RIGHT), FadeIn(lbl_left))

        play_left_anim = extract_features_ui(img_left, img_6_data["raw"], img_6_data["norm"])
        left_grp, v_norm_left = play_left_anim()
        
        self.wait(1)

        # =========================
        # 3. TRƯỜNG HỢP 1: NGHIÊNG ĐẦU (POSE)
        # =========================
        title_case1 = make_label("Case 1: Lệch góc xoay/Nghiêng đầu (Pose Variation)", font_size=18, bg_color=MY_BLUE).next_to(phase_title, DOWN, buff=0.1)
        self.play(FadeIn(title_case1))

        img_8_data = {"img": "image_8.jpg", "raw": "[400, 800, ..., 1100]", "norm": "[0.04, 0.08, ..., 0.11]", "v_math": r"V_{Nghieng} = [0.04, 0.08, \dots, 0.11]"}
        img_right_1 = get_img(img_8_data["img"], h=2.5, pos=[img_right_x, img_y, 0]).set_z_index(5)
        lbl_right_1 = make_label("Cùng 1 người (Nghiêng đầu)", font_size=16, color=WHITE, bg_color=BLACK).next_to(img_right_1, UP, buff=0.1)
        
        self.play(FadeIn(img_right_1, shift=LEFT), FadeIn(lbl_right_1))

        play_right_1_anim = extract_features_ui(img_right_1, img_8_data["raw"], img_8_data["norm"])
        right_grp_1, v_norm_right_1 = play_right_1_anim()
        self.wait(0.5)

        calc_box_1 = create_calc_box("So sánh 2 ảnh cùng 1 người:", img_6_data["v_math"], img_8_data["v_math"], 0.72)
        
        arrow_L_to_C = Arrow(start=v_norm_left.get_right(), end=calc_box_1.get_left(), color=MY_YELLOW, stroke_width=4)
        arrow_R_to_C = Arrow(start=v_norm_right_1.get_left(), end=calc_box_1.get_right(), color=MY_YELLOW, stroke_width=4)

        self.play(GrowArrow(arrow_L_to_C), GrowArrow(arrow_R_to_C))
        self.play(FadeIn(calc_box_1, shift=UP))

        res_txt_1 = make_label("KẾT QUẢ: d = 0.72 > 0.65 => TỪ CHỐI NHẬN DIỆN (Lỗi do góc)", font_size=20, color=WHITE, bg_color=MY_RED).move_to(DOWN * 3.2)
        self.play(FadeIn(res_txt_1, shift=UP))
        self.wait(3)

        self.play(FadeOut(Group(title_case1, img_right_1, lbl_right_1, right_grp_1, calc_box_1, arrow_L_to_C, arrow_R_to_C, res_txt_1)))

        # =========================
        # 4. TRƯỜNG HỢP 2: ÁNH SÁNG (ILLUMINATION)
        # =========================
        title_case2 = make_label("Case 2: Nhiễu ánh sáng/Bị chói (Illumination)", font_size=18, bg_color=MY_BLUE).next_to(phase_title, DOWN, buff=0.1)
        self.play(FadeIn(title_case2))

        img_9_data = {"img": "image_9.jpg", "raw": "[150, 1200, ..., 800]", "norm": "[0.01, 0.12, ..., 0.08]", "v_math": r"V_{Choi} = [0.01, 0.12, \dots, 0.08]"}
        img_right_2 = get_img(img_9_data["img"], h=2.5, pos=[img_right_x, img_y, 0]).set_z_index(5)
        lbl_right_2 = make_label("Cùng 1 người (Bị chói sáng)", font_size=16, color=WHITE, bg_color=BLACK).next_to(img_right_2, UP, buff=0.1)
        
        self.play(FadeIn(img_right_2, shift=LEFT), FadeIn(lbl_right_2))

        play_right_2_anim = extract_features_ui(img_right_2, img_9_data["raw"], img_9_data["norm"])
        right_grp_2, v_norm_right_2 = play_right_2_anim()
        self.wait(0.5)

        calc_box_2 = create_calc_box("So sánh 2 ảnh cùng 1 người:", img_6_data["v_math"], img_9_data["v_math"], 0.81)
        
        arrow_L_to_C2 = Arrow(start=v_norm_left.get_right(), end=calc_box_2.get_left(), color=MY_YELLOW, stroke_width=4)
        arrow_R_to_C2 = Arrow(start=v_norm_right_2.get_left(), end=calc_box_2.get_right(), color=MY_YELLOW, stroke_width=4)

        self.play(GrowArrow(arrow_L_to_C2), GrowArrow(arrow_R_to_C2))
        self.play(FadeIn(calc_box_2, shift=UP))

        res_txt_2 = make_label("KẾT QUẢ: d = 0.81 > 0.65 => TỪ CHỐI NHẬN DIỆN (Lỗi ánh sáng)", font_size=20, color=WHITE, bg_color=MY_RED).move_to(DOWN * 3.2)
        self.play(FadeIn(res_txt_2, shift=UP))
        self.wait(3.5)

        # =========================
        # 5. GOM VỀ GIỮA & SHOW IMPROVEMENTS
        # =========================
        mobjects_to_shrink = Group(*[m for m in self.mobjects if m.z_index != -10])
        
        self.play(
            mobjects_to_shrink.animate.scale(0.05).move_to(ORIGIN).set_opacity(0),
            run_time=1.5, rate_func=smooth
        )
        self.remove(mobjects_to_shrink)

        improve_img = get_img("improve.jpg", h=3.0, pos=ORIGIN).set_z_index(5)
        improve_lbl = make_label("CÁC HƯỚNG CẢI TIẾN & PHÁT TRIỂN (FUTURE WORKS)", font_size=24, bg_color=MY_GREEN).to_edge(UP, buff=0.5)
        
        self.play(FadeIn(improve_img, scale=0.5), FadeIn(improve_lbl, shift=DOWN), run_time=1)

        improvements = [
            {"text": "MB-LBP\n(Multi-scale Block LBP)", "color": MY_BLUE, "pos": LEFT * 5.0 + UP * 1.5},
            {"text": "CS-LBP\n(Center-Symmetric LBP)", "color": TEAL_E, "pos": RIGHT * 5.0 + UP * 1.5},
            {"text": "LQP\n(Local Quantized Patterns)", "color": PURPLE, "pos": LEFT * 5.0 + DOWN * 1.5},
            {"text": "LTP\n(Local Ternary Patterns)", "color": ORANGE, "pos": RIGHT * 5.0 + DOWN * 1.5},
            {"text": "Kết hợp AI / Deep Learning\n(CNN, ResNet, FaceNet...)", "color": MY_RED, "pos": DOWN * 2.8}
        ]

        arrows = []
        labels = []
        for imp in improvements:
            lbl = make_label(imp["text"], font_size=16, color=WHITE, bg_color=imp["color"]).move_to(imp["pos"])
            arr = Arrow(start=improve_img.get_center(), end=lbl.get_center(), color=imp["color"], stroke_width=4, buff=1.6)
            labels.append(lbl)
            arrows.append(arr)

        self.play(
            *[GrowArrow(arr) for arr in arrows],
            *[FadeIn(lbl, shift=lbl.get_center() - ORIGIN) for lbl in labels],
            run_time=1.5
        )

        self.wait(4)
        
        # =========================
        # 6. GRAND FINALE: OUTRO CẢM ƠN (FIX LỖI TRANSFORMATION BẰNG CÁCH PHỐI HỢP FADE & GROW)
        # =========================
        outro_title = Text("CẢM ƠN ĐÃ XEM VIDEO!", font_size=50, weight=BOLD, gradient=(MY_BLUE, MY_GREEN))
        outro_author = Text("Người thực hiện: Thông Lúc - 22120196", font_size=30, color=WHITE)
        outro_box = VGroup(outro_title, outro_author).arrange(DOWN, buff=0.4)
        
        outro_bg = SurroundingRectangle(outro_box, color=MY_BLUE, fill_color=BLACK, fill_opacity=0.9, stroke_width=4, buff=0.6, corner_radius=0.3)
        outro_final = VGroup(outro_bg, outro_box).set_z_index(50)

        mobjects_to_transform = Group(*[m for m in self.mobjects if m.z_index != -10])
        
        # FIX: Cho mobjects hiện tại hút về giữa và tàng hình, đồng thời phóng Outro từ giữa ra
        self.play(
            mobjects_to_transform.animate.scale(0.05).move_to(ORIGIN).set_opacity(0),
            GrowFromCenter(outro_final),
            run_time=1.5, rate_func=smooth
        )
        self.remove(mobjects_to_transform)
        
        self.wait(3)

        self.play(FadeOut(Group(*self.mobjects)))
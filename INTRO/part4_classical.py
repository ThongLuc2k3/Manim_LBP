from manim import *
import numpy as np
import os

class Part4ClassicalMethods(Scene):
    def construct(self):
        MY_CYAN = "#00FFFF"
        MY_RED = "#FF0000"
        MY_YELLOW = "#FFD700"
        MY_BLUE = "#0000FF"
        MY_ORANGE = "#FF8C00"

        # =========================
        # 0. NỀN TỔNG THỂ
        # =========================
        def get_image_path(filename):
            paths_to_try = [os.path.join("..", "Data", filename), os.path.join("Data", filename), filename]
            for path in paths_to_try:
                if os.path.exists(path): return path
            return filename 

        bg_hcmus = ImageMobject(get_image_path("hcmus.jpg"))
        scale_w = config.frame_width / bg_hcmus.width
        scale_h = config.frame_height / bg_hcmus.height
        bg_hcmus.scale(max(scale_w, scale_h)).set_z_index(-10)
        self.add(bg_hcmus)

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
        # 1. SETUP BAN ĐẦU
        # =========================
        img_math_box = fit_img("math_box.jpg", h=3.0, fallback_color=BLUE_E).move_to(ORIGIN)
        lbl_classical = make_label("Classical Methods (Handcrafted Features)", font_size=16, color=MY_CYAN).next_to(img_math_box, DOWN, buff=0.2)
        
        main_grp = Group(img_math_box, lbl_classical)
        self.add(main_grp)
        
        self.play(main_grp.animate.scale(0.5).to_edge(UP, buff=0.15), run_time=1.5)
        time_range = make_label("(1991 - 2012)", font_size=20, color=MY_YELLOW).move_to(img_math_box.get_center())
        self.play(FadeIn(time_range, shift=UP), run_time=1)

        # =========================
        # 2. 4 NHÓM PHƯƠNG PHÁP
        # =========================
        def create_detailed_card(title, algs, border_color):
            bg = RoundedRectangle(width=2.8, height=3.2, corner_radius=0.15, color=border_color, stroke_width=2.5).set_fill("#F3E9AF", 0.9)
            t_title = Text(title, font_size=14, color=border_color, weight=BOLD)
            t_algs = VGroup(*[Text(f"• {name}", font_size=11, color=BLACK) for name in algs]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            content = VGroup(t_title, Line(LEFT*0.8, RIGHT*0.8, color=GRAY, stroke_width=1), t_algs).arrange(DOWN, buff=0.2)
            content.move_to(bg.get_center())
            return Group(bg, content)

        card1 = create_detailed_card("Subspace", ["Eigenfaces", "Fisherfaces", "Laplacianfaces"], BLUE)
        card2 = create_detailed_card("Local Texture", ["LBP", "LBPH", "LTP", "BSIF"], MY_ORANGE)
        card3 = create_detailed_card("Filter-based", ["Gabor", "Log-Gabor", "EBGM"], TEAL)
        card4 = create_detailed_card("Keypoint", ["SIFT", "SURF", "ORB"], PURPLE)

        cards_grp = Group(card1, card2, card3, card4).arrange(RIGHT, buff=0.2).shift(DOWN * 1.0)
        arrows_in = VGroup(*[Arrow(start=lbl_classical.get_bottom(), end=c.get_top(), color=MY_RED, stroke_width=3, tip_length=0.15) for c in cards_grp])

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_in], lag_ratio=0.15), FadeIn(cards_grp, shift=UP), run_time=2)
        self.wait(1)

        # =========================
        # 3. PHÓNG TO LOCAL TEXTURE - DỌN DẸP
        # =========================
        stuff_to_fade = Group(card1, card3, card4, arrows_in, main_grp, time_range)
        self.play(
            FadeOut(stuff_to_fade, shift=DOWN*0.3), 
            card2.animate.scale(1.1).move_to(ORIGIN).shift(UP * 0.8),
            run_time=1.5
        )

        def create_sub_box(name, info, pos):
            box = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.1, color=MY_ORANGE).set_fill("#92DCF0", 0.8)
            t_name = Text(name, font_size=15, color="#1900FF", weight=BOLD)
            t_info = Text(info, font_size=10, color=BLACK)
            cnt = VGroup(t_name, t_info).arrange(DOWN, buff=0.1).move_to(box.get_center())
            return Group(box, cnt).move_to(pos)

        sub_lbp = create_sub_box("LBP", "Descriptor", LEFT * 3.8 + UP * 1.8)
        sub_lbph = create_sub_box("LBPH", "Histograms", RIGHT * 3.8 + UP * 1.8)
        sub_ltp = create_sub_box("LTP", "Robust Noise", LEFT * 3.8 + DOWN * 1.2)
        sub_bsif = create_sub_box("BSIF", "Learned", RIGHT * 3.8 + DOWN * 1.2)
        sub_boxes = Group(sub_lbp, sub_lbph, sub_ltp, sub_bsif)
        arrows_out = VGroup(*[Arrow(start=card2.get_center(), end=sb.get_center(), color=MY_RED, stroke_width=3, buff=0.8) for sb in sub_boxes])

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_out], lag_ratio=0.2), FadeIn(sub_boxes, scale=0.7), run_time=2)
        self.wait(2)

        # =========================
        # 4. CHỐT LBP: PHÓNG TO RỒI THU NHỎ BIẾN MẤT
        # =========================
        lbp_final_text = sub_lbp[1][0] # Chữ LBP

        # 4.1 Dọn dẹp các thành phần xung quanh cực nhanh
        self.play(
            FadeOut(card2), FadeOut(arrows_out), FadeOut(sub_lbph), 
            FadeOut(sub_ltp), FadeOut(sub_bsif), FadeOut(sub_lbp[0]), FadeOut(sub_lbp[1][1]),
            lbp_final_text.animate.move_to(ORIGIN).scale(2.5).set_color(MY_BLUE),
            run_time=0.8
        )
        
        # 4.2 Phóng to chữ LBP khổng lồ (Chậm và từ từ hơn)
        self.play(
            lbp_final_text.animate.scale(25), 
            run_time=1.5, # Tăng thời gian lên 1.5s để nhìn rõ quá trình phóng to
            rate_func=rate_functions.ease_in_out_sine
        )

        # 4.3 Thu nhỏ mất tiêu ngay lập tức để trả lại nền sạch (Cực nhanh)
        self.play(
            lbp_final_text.animate.scale(0).set_opacity(0),
            run_time=0.15, # Chỉ mất 0.15s để hút về 0
            rate_func=rate_functions.rush_into
        )

        # =========================
        # 5. KẾT THÚC: NỀN HCMUS SẠCH SẼ
        # =========================
        self.remove(*self.mobjects)
        
        bg_final = ImageMobject(get_image_path("hcmus.jpg"))
        bg_final.scale(max(scale_w, scale_h))
        self.add(bg_final)
        
        self.play(Flash(ORIGIN, color=WHITE, line_length=0.5, flash_radius=1, num_lines=15), run_time=0.1)
        self.wait(0.1)
         
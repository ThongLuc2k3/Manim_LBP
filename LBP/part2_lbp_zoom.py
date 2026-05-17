from manim import *
import os
import numpy as np

class Part2LBPZoom(Scene):
    def construct(self):
        MY_BLUE = "#0055FF"
        MY_RED = "#FF0000"
        MY_GREEN = "#00AA00"

        # =========================
        # 1. HELPER & BACKGROUND
        # =========================
        def get_image_path(filename):
            paths_to_try = [
                os.path.join("..", "Data", filename),  
                os.path.join("Data", filename),        
                filename                               
            ]
            for path in paths_to_try:
                if os.path.exists(path): return path
            return filename 

        try:
            bg_hcmus = ImageMobject(get_image_path("hcmus.jpg"))
            scale_w = config.frame_width / bg_hcmus.width
            scale_h = config.frame_height / bg_hcmus.height
            bg_hcmus.scale(max(scale_w, scale_h))
            self.add(bg_hcmus)
        except:
            self.camera.background_color = WHITE

        def make_label(text_str, font_size=20, color=WHITE, bg_color=BLACK):
            txt = Text(text_str, font_size=font_size, color=color)
            bg = SurroundingRectangle(txt, color=bg_color, fill_opacity=1, stroke_width=0, buff=0.1)
            return Group(bg, txt)

        # =========================
        # 2. TÁI HIỆN LƯỚI PIXEL GỐC
        # =========================
        box_w = 3.2
        box_h = 3.9
        
        try:
            img_color = ImageMobject(get_image_path("image_1.jpg")).scale_to_fit_height(4.5)
            pixel_array = img_color.get_pixel_array()
            gray_array = np.dot(pixel_array[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
            gray_rgba = np.zeros_like(pixel_array)
            for i in range(3): gray_rgba[..., i] = gray_array
            gray_rgba[..., 3] = pixel_array[..., 3] 
            
            img_gray = ImageMobject(gray_rgba)
            img_gray.stretch_to_fit_width(box_w).stretch_to_fit_height(box_h)
        except:
            img_gray = Rectangle(width=box_w, height=box_h).set_fill(GRAY, 1)

        resize_box = Rectangle(width=box_w, height=box_h, color=MY_RED, stroke_width=4)
        
        grid = VGroup()
        step = box_w / 16 
        
        for i in range(1, 16):
            grid.add(Line(resize_box.get_corner(UL) + RIGHT * i * step, resize_box.get_corner(DL) + RIGHT * i * step, color=WHITE, stroke_width=1, stroke_opacity=0.5))
        for i in range(1, int(box_h / step) + 1):
            if (DOWN * i * step)[1] >= -box_h:
                grid.add(Line(resize_box.get_corner(UL) + DOWN * i * step, resize_box.get_corner(UR) + DOWN * i * step, color=WHITE, stroke_width=1, stroke_opacity=0.5))

        last_scene_group = Group(img_gray, resize_box, grid).move_to(ORIGIN)
        self.add(last_scene_group)
        self.wait(0.5)

        # XÓA LỆNH SAVE_STATE Ở ĐÂY ĐỂ TRÁNH LỖI MOBJECT

        # =========================
        # 3. TÍNH TOÁN TỌA ĐỘ VÀ ZOOM IN KHỚP 100%
        # =========================
        ZOOM_FACTOR = 8 
        scaled_step = step * ZOOM_FACTOR 
        
        ul_corner = resize_box.get_corner(UL)
        target_col, target_row = 8, 8
        target_pixel_center = ul_corner + RIGHT * (target_col + 0.5) * step + DOWN * (target_row + 0.5) * step
        
        POS_LEFT = LEFT * 3.5 + UP * 0.5
        shift_vec = POS_LEFT - target_pixel_center

        self.play(
            last_scene_group.animate.scale(ZOOM_FACTOR, about_point=target_pixel_center).shift(shift_vec),
            run_time=2, rate_func=smooth
        )

        values = [[120, 80, 200], [30, 100, 105], [110, 90, 50]]
        squares = [[None for _ in range(3)] for _ in range(3)]
        texts = [[None for _ in range(3)] for _ in range(3)]
        grid_3x3 = VGroup()

        for r in range(3):
            for c in range(3):
                sq = Square(side_length=scaled_step, color=WHITE, stroke_width=2).set_fill(BLACK, 0)
                sq.move_to(POS_LEFT + RIGHT * (c - 1) * scaled_step + DOWN * (r - 1) * scaled_step)
                txt = Text(str(values[r][c]), font_size=36, color=WHITE, stroke_width=1, stroke_color=BLACK).move_to(sq)
                squares[r][c] = sq
                texts[r][c] = txt
                grid_3x3.add(sq, txt)

        self.play(FadeIn(grid_3x3), run_time=1)
        
        fade_anims = [last_scene_group.animate.set_opacity(0.1)]
        for r in range(3):
            for c in range(3):
                fade_anims.append(squares[r][c].animate.set_fill(BLACK, 0.85))
        self.play(*fade_anims, run_time=1.5)

        # =========================
        # 4. TÍNH TOÁN LBP (BÊN PHẢI)
        # =========================
        label_zoom = make_label("Minh họa Thuật toán LBP", bg_color=MY_BLUE).to_edge(UP, buff=0.5)
        self.play(FadeIn(label_zoom))

        center_sq = squares[1][1]
        center_txt = texts[1][1]
        self.play(center_sq.animate.set_fill(MY_BLUE, 0.9), center_txt.animate.set_color(YELLOW))

        POS_RIGHT = RIGHT * 3.0
        rule_box = VGroup(
            Text("Quy tắc (Ngưỡng = 100):", font_size=20, color=WHITE),
            Text("≥ 100 ➔ 1", font_size=32, color=MY_GREEN),
            Text("< 100 ➔ 0", font_size=32, color=MY_RED)
        ).arrange(DOWN, aligned_edge=LEFT)
        rule_group = Group(SurroundingRectangle(rule_box, color=BLACK, fill_opacity=0.85, buff=0.2), rule_box).move_to(POS_RIGHT + UP * 1.5)
        self.play(FadeIn(rule_group))

        start_label = make_label("Bắt đầu", font_size=16, bg_color=MY_RED).next_to(squares[0][0], UP, buff=0.1)
        clock_arrow = Arc(radius=scaled_step*1.2, start_angle=PI/2 + PI/4, angle=-TAU*0.8, color=YELLOW, stroke_width=4).move_to(POS_LEFT)
        clock_arrow.add_tip(tip_length=0.25, tip_width=0.25)
        self.play(FadeIn(start_label), Create(clock_arrow))

        clockwise_indices = [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0)]
        binary_string = ""
        binary_title = make_label("Chuỗi LBP:", font_size=20).move_to(POS_RIGHT + DOWN * 0.3)
        binary_group = VGroup().next_to(binary_title, DOWN, buff=0.2)
        self.play(FadeIn(binary_title))

        for idx, (r, c) in enumerate(clockwise_indices):
            val = values[r][c]
            sq = squares[r][c]
            txt = texts[r][c]
            
            self.play(sq.animate.set_stroke(YELLOW, 4), run_time=0.15)
            bit = "1" if val >= 100 else "0"
            color_bit = MY_GREEN if bit == "1" else MY_RED
            
            new_txt = Text(bit, font_size=42, color=WHITE, weight=BOLD).move_to(sq)
            self.play(Transform(txt, new_txt), sq.animate.set_fill(color_bit, 0.8).set_stroke(WHITE, 1), run_time=0.2)
            
            binary_string += bit
            floating_bit = Text(bit, font_size=32, color=color_bit, weight=BOLD).move_to(sq)
            binary_group.add(floating_bit)
            binary_group.arrange(RIGHT, buff=0.1).next_to(binary_title, DOWN, buff=0.2)
            self.play(floating_bit.animate.move_to(binary_group[-1].get_center()), run_time=0.25)

        dec_val = int(binary_string, 2)
        decimal_text = make_label(f"➔ {dec_val} (Thập phân)", font_size=24, bg_color=MY_RED).next_to(binary_group, DOWN, buff=0.4)
        self.play(FadeIn(decimal_text, shift=UP))

        final_center_txt = Text(str(dec_val), font_size=42, color=WHITE, weight=BOLD).move_to(center_sq)
        self.play(Transform(texts[1][1], final_center_txt), center_sq.animate.set_fill(MY_RED, 0.9), run_time=1)
        self.wait(1)

        # =========================
        # 5. ZOOM OUT & ĐẶT CHẤM ĐỎ VÀO ĐÚNG VỊ TRÍ
        # =========================
        self.play(FadeOut(Group(label_zoom, rule_group, start_label, clock_arrow, binary_title, binary_group, decimal_text)))
        
        self.play(last_scene_group.animate.set_opacity(1), run_time=0.5)

        # CÁCH FIX MỚI TỐI ƯU NHẤT: Ép thủ công ảnh thu nhỏ và lùi về ORIGIN
        self.play(
            last_scene_group.animate.scale(1/ZOOM_FACTOR).move_to(ORIGIN),
            grid_3x3.animate.scale(1/ZOOM_FACTOR, about_point=POS_LEFT).move_to(target_pixel_center),
            run_time=2, rate_func=smooth
        )
        self.wait(0.5)

        red_dot = Square(side_length=step, color=MY_RED, fill_opacity=1).move_to(target_pixel_center)
        dot_label = make_label("178", font_size=12, bg_color=MY_RED).next_to(red_dot, RIGHT, buff=0.05)
        
        self.play(FadeOut(grid_3x3), FadeIn(red_dot), FadeIn(dot_label))
        self.wait(1)

        # =========================
        # 6. ZOOM VÀO GÓC PADDING TÍNH SIÊU TỐC
        # =========================
        self.play(FadeOut(red_dot), FadeOut(dot_label))
        
        pad_pixel_center = ul_corner + RIGHT*(step/2) + DOWN*(step/2)
        pad_shift_vec = POS_LEFT - pad_pixel_center
        
        self.play(
            last_scene_group.animate.scale(ZOOM_FACTOR, about_point=pad_pixel_center).shift(pad_shift_vec),
            run_time=2, rate_func=smooth
        )

        pad_label = make_label("Padding: Thêm ô ảo (Giá trị 0) cho viền ngoài", bg_color=MY_BLUE).to_edge(UP, buff=0.5)
        self.play(FadeIn(pad_label))

        padding_grid = VGroup()
        pad_squares = [[None for _ in range(3)] for _ in range(3)]
        pad_texts = [[None for _ in range(3)] for _ in range(3)]
        pad_values = [[0, 0, 0], [0, 90, 110], [0, 85, 120]] 

        for r in range(3):
            for c in range(3):
                is_padding = (r == 0) or (c == 0)
                
                bg_fill = Square(side_length=scaled_step).set_fill(BLACK, 1).set_stroke(width=0)
                bg_fill.move_to(POS_LEFT + RIGHT * (c - 1) * scaled_step + DOWN * (r - 1) * scaled_step)

                if is_padding:
                    sq = DashedVMobject(Square(side_length=scaled_step, color=YELLOW, stroke_width=4), num_dashes=12)
                    txt = Text("0", font_size=36, color=MY_RED, weight=BOLD)
                    padding_grid.add(bg_fill, sq)
                else:
                    sq = Square(side_length=scaled_step, color=WHITE, stroke_width=2).set_fill(BLACK, 0)
                    txt = Text(str(pad_values[r][c]), font_size=36, color=WHITE, stroke_width=1, stroke_color=BLACK)
                    padding_grid.add(sq)
                
                sq.move_to(bg_fill.get_center())
                txt.move_to(sq)
                padding_grid.add(txt)
                
                pad_squares[r][c] = bg_fill if is_padding else sq
                pad_texts[r][c] = txt

        self.play(FadeIn(padding_grid), run_time=1)

        fade_pad_anims = [last_scene_group.animate.set_opacity(0.1)]
        for r in range(3):
            for c in range(3):
                if not ((r == 0) or (c == 0)):
                    fade_pad_anims.append(pad_squares[r][c].animate.set_fill(BLACK, 0.85))
        self.play(*fade_pad_anims, run_time=1)

        self.play(pad_squares[1][1].animate.set_fill(MY_BLUE, 0.9), pad_texts[1][1].animate.set_color(YELLOW), run_time=0.5)

        fast_binary = ""
        fast_binary_group = VGroup()
        for idx, (r, c) in enumerate(clockwise_indices):
            val = pad_values[r][c]
            bit = "1" if val >= 90 else "0"
            color_bit = MY_GREEN if bit == "1" else MY_RED
            new_txt = Text(bit, font_size=42, color=WHITE, weight=BOLD).move_to(pad_squares[r][c])
            
            fast_binary += bit
            floating_bit = Text(bit, font_size=32, color=color_bit, weight=BOLD).move_to(pad_squares[r][c])
            fast_binary_group.add(floating_bit)
            
            fast_binary_group.arrange(RIGHT, buff=0.1).next_to(pad_label, DOWN, buff=0.3)
            
            self.play(
                Transform(pad_texts[r][c], new_txt), 
                floating_bit.animate.move_to(fast_binary_group[-1].get_center()),
                run_time=0.15
            )

        fast_dec_val = int(fast_binary, 2)
        fast_dec_txt = make_label(f"➔ {fast_dec_val}", bg_color=MY_RED).next_to(fast_binary_group, RIGHT, buff=0.3)
        
        self.play(FadeIn(fast_dec_txt, shift=LEFT), run_time=0.5)

        fast_final_txt = Text(str(fast_dec_val), font_size=42, color=WHITE, weight=BOLD).move_to(pad_squares[1][1])
        self.play(
            Transform(pad_texts[1][1], fast_final_txt), 
            pad_squares[1][1].animate.set_fill(MY_RED, 0.9), 
            run_time=0.5
        )
        self.wait(2)

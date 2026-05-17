from manim import *
import os
import numpy as np
import random

class Part3LBPHistogram(Scene):
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
            bg_hcmus.set_z_index(-10)
            self.add(bg_hcmus)
        except:
            self.camera.background_color = WHITE

        def make_label(text_str, font_size=18, color=WHITE, bg_color=BLACK):
            txt = Text(text_str, font_size=font_size, color=color)
            bg = SurroundingRectangle(txt, color=bg_color, fill_opacity=1, stroke_width=0, buff=0.1)
            return VGroup(bg, txt)

        # =========================
        # 2. XỬ LÝ ẢNH & TÍNH TOÁN LBP THẬT
        # =========================
        box_w = 3.2
        box_h = 3.9
        
        try:
            img_color = ImageMobject(get_image_path("image_1.jpg")).scale_to_fit_height(4.5)
            pixel_array = img_color.get_pixel_array()
            gray_array = np.dot(pixel_array[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
            
            padded = np.pad(gray_array, 1, mode='constant', constant_values=0)
            center = padded[1:-1, 1:-1]
            lbp_real = np.zeros_like(center, dtype=np.uint8)
            
            lbp_real |= np.where(padded[0:-2, 0:-2] >= center, 128, 0).astype(np.uint8)
            lbp_real |= np.where(padded[0:-2, 1:-1] >= center, 64, 0).astype(np.uint8)  
            lbp_real |= np.where(padded[0:-2, 2:] >= center, 32, 0).astype(np.uint8)    
            lbp_real |= np.where(padded[1:-1, 2:] >= center, 16, 0).astype(np.uint8)    
            lbp_real |= np.where(padded[2:, 2:] >= center, 8, 0).astype(np.uint8)       
            lbp_real |= np.where(padded[2:, 1:-1] >= center, 4, 0).astype(np.uint8)       
            lbp_real |= np.where(padded[2:, 0:-2] >= center, 2, 0).astype(np.uint8)       
            lbp_real |= np.where(padded[1:-1, 0:-2] >= center, 1, 0).astype(np.uint8)     

            hist_real, _ = np.histogram(lbp_real.flatten(), bins=32, range=(0, 256))
            max_freq = int(max(hist_real))
            y_step = max(1, max_freq // 4) 
            
            gray_rgba = np.zeros_like(pixel_array)
            for i in range(3): gray_rgba[..., i] = gray_array
            gray_rgba[..., 3] = pixel_array[..., 3] 
            img_gray = ImageMobject(gray_rgba).stretch_to_fit_width(box_w).stretch_to_fit_height(box_h)
        except:
            img_gray = Rectangle(width=box_w, height=box_h).set_fill(GRAY, 1)
            lbp_real = np.random.randint(0, 256, (156, 128))
            hist_real = [np.random.randint(10, 100) for _ in range(32)]
            max_freq = 100
            y_step = 25

        # =========================
        # 3. DỰNG LẠI KHUNG ẢNH GỐC
        # =========================
        img_gray.move_to(ORIGIN)
        resize_box = Rectangle(width=box_w, height=box_h, color=MY_RED, stroke_width=4).move_to(ORIGIN).set_z_index(1)
        
        grid = VGroup().set_z_index(1)
        n_cols = 16
        step = box_w / n_cols 
        n_rows = int(box_h / step)

        for i in range(1, 16):
            grid.add(Line(resize_box.get_corner(UL) + RIGHT * i * step, resize_box.get_corner(DL) + RIGHT * i * step, color=WHITE, stroke_width=1, stroke_opacity=0.4))
        for i in range(1, n_rows + 1):
            if (DOWN * i * step)[1] >= -box_h:
                grid.add(Line(resize_box.get_corner(UL) + DOWN * i * step, resize_box.get_corner(UR) + DOWN * i * step, color=WHITE, stroke_width=1, stroke_opacity=0.4))

        last_scene_group = Group(img_gray, resize_box, grid).move_to(ORIGIN)

        # =========================
        # 4. TÁI HIỆN CẢNH CUỐI PHẦN 2 
        # =========================
        ZOOM_FACTOR = 8
        SCENE_SCALE = 0.9
        UI_SCALE = 1 / SCENE_SCALE 
        scaled_step = step * ZOOM_FACTOR
        ul_corner = resize_box.get_corner(UL)
        pad_pixel_center = ul_corner + RIGHT*(step/2) + DOWN*(step/2)
        POS_LEFT = LEFT * 3.5 + UP * 0.5
        pad_shift_vec = POS_LEFT - pad_pixel_center

        last_scene_group.scale(ZOOM_FACTOR, about_point=pad_pixel_center).shift(pad_shift_vec)
        last_scene_group.set(opacity=0.1)
        self.add(last_scene_group)

        cells = VGroup().set_z_index(2)
        center_cell = VGroup().set_z_index(3)
        for r in range(3):
            for c in range(3):
                cell_group = VGroup()
                is_padding = (r == 0) or (c == 0)
                is_center = (r == 1) and (c == 1)

                bg_fill = Square(side_length=scaled_step).set_fill(MY_RED if is_center else BLACK, 1 if is_center else 1).set_stroke(width=0)
                bg_fill.move_to(POS_LEFT + RIGHT * (c - 1) * scaled_step + DOWN * (r - 1) * scaled_step)

                if is_padding:
                    sq = DashedVMobject(Square(side_length=scaled_step, color=YELLOW, stroke_width=4), num_dashes=12)
                    txt = Text("0", font_size=int(36 * UI_SCALE), color=WHITE, weight=BOLD)
                elif is_center:
                    sq = Square(side_length=scaled_step, color=WHITE, stroke_width=2).set_fill(BLACK, 0)
                    txt = Text("24", font_size=42, color=WHITE, weight=BOLD)
                else:
                    sq = Square(side_length=scaled_step, color=WHITE, stroke_width=2).set_fill(BLACK, 0)
                    txt = Text("1" if (r,c) in [(1,2), (2,2)] else "0", font_size=42, color=WHITE, weight=BOLD)

                sq.move_to(bg_fill.get_center())
                txt.move_to(sq)
                cell_group.add(bg_fill, sq, txt)

                if is_center:
                    center_cell = cell_group
                else:
                    cells.add(cell_group)
        
        self.add(cells, center_cell)

        pad_label = make_label("Padding: Thêm ô ảo (Giá trị 0) cho viền ngoài", font_size=int(18 * UI_SCALE), bg_color=MY_BLUE).to_edge(UP, buff=0.5).set_z_index(5)
        
        fast_binary_group = VGroup().set_z_index(5)
        for bit in "00011000":
            b_color = MY_GREEN if bit == "1" else MY_RED
            fast_binary_group.add(Text(bit, font_size=32, color=b_color, weight=BOLD))
        fast_binary_group.arrange(RIGHT, buff=0.1).next_to(pad_label, DOWN, buff=0.3)
        
        fast_dec_txt = make_label("➔ 24", font_size=int(18 * UI_SCALE), bg_color=MY_RED).next_to(fast_binary_group, RIGHT, buff=0.3).set_z_index(5)
        
        extra_ui = Group(pad_label, fast_binary_group, fast_dec_txt)
        self.add(extra_ui)
        self.wait(0.1)

        # =========================
        # 5. CHUYỂN CẢNH: DỌN DẸP & ZOOM OUT VỀ ẢNH GỐC
        # =========================
        self.play(FadeOut(extra_ui), FadeOut(cells), run_time=1)
        
        self.play(
            last_scene_group.animate.shift(-pad_shift_vec).scale(1/ZOOM_FACTOR, about_point=pad_pixel_center).set(opacity=1), 
            center_cell.animate.scale(1/ZOOM_FACTOR, about_point=POS_LEFT).move_to(pad_pixel_center),
            run_time=2, rate_func=smooth
        )

        dot_24 = Square(side_length=step*0.8, color=MY_RED, fill_opacity=1).move_to(pad_pixel_center).set_z_index(5)
        txt_24 = Text("24", font_size=8, color=WHITE).move_to(pad_pixel_center).set_z_index(6)

        pos_178 = ul_corner + RIGHT * (8 + 0.5) * step + DOWN * (8 + 0.5) * step
        dot_178 = Square(side_length=step*0.8, color=MY_RED, fill_opacity=1).move_to(pos_178).set_z_index(5)
        txt_178 = Text("178", font_size=8, color=WHITE).move_to(pos_178).set_z_index(6)

        self.play(
            FadeOut(center_cell),
            FadeIn(dot_24), FadeIn(txt_24),
            FadeIn(dot_178), FadeIn(txt_178),
            run_time=0.5
        )

        face_group = Group(last_scene_group, dot_24, txt_24, dot_178, txt_178)
        self.play(face_group.animate.move_to(UP * 2.2).scale(0.65), run_time=1.5)

        # =========================
        # 6. MŨI TÊN CHỈ DẪN 2 Ô ĐÃ TÍNH
        # =========================
        arrow_178 = Arrow(start=txt_178.get_center() + RIGHT*1.0 + DOWN*0.5, end=txt_178.get_center() + RIGHT*0.1, color=YELLOW, tip_length=0.15)
        lbl_178 = make_label("Tâm (178)", font_size=10, color=YELLOW, bg_color=BLACK).next_to(arrow_178.get_start(), DOWN, buff=0.05)

        arrow_24 = Arrow(start=txt_24.get_center() + LEFT*1.0 + DOWN*0.3, end=txt_24.get_center() + LEFT*0.1, color=YELLOW, tip_length=0.15)
        lbl_24 = make_label("Padding (24)", font_size=10, color=YELLOW, bg_color=BLACK).next_to(arrow_24.get_start(), DOWN, buff=0.05)

        ptr_group = Group(arrow_178, lbl_178, arrow_24, lbl_24).set_z_index(10)
        self.play(FadeIn(ptr_group))
        self.wait(1.5)
        self.play(FadeOut(ptr_group))

        # =========================
        # 7. CHỚP SÁNG VÀ HIỆN SỐ LBP (FIX Z-INDEX 100)
        # =========================
        label_flash = make_label("Các pixel còn lại được tính toán đồng loạt...", bg_color=MY_BLUE).to_edge(UP, buff=0.1).set_z_index(10)
        self.play(FadeIn(label_flash))

        flash_rect = Rectangle(width=box_w*0.65, height=box_h*0.65, color=WHITE, fill_opacity=0.8).move_to(img_gray.get_center()).set_z_index(10)
        self.play(FadeIn(flash_rect), run_time=0.2)

        lbp_numbers = VGroup().set_z_index(100)
        
        curr_ul = resize_box.get_corner(UL)
        curr_ur = resize_box.get_corner(UR)
        curr_dl = resize_box.get_corner(DL)
        vec_x = (curr_ur - curr_ul) / 16
        vec_y = (curr_dl - curr_ul) / n_rows

        for r in range(n_rows):
            for c in range(16):
                if (r == 8 and c == 8) or (r == 0 and c == 0): continue
                
                row_idx = int((r / n_rows) * lbp_real.shape[0])
                col_idx = int((c / 16) * lbp_real.shape[1])
                real_val = str(lbp_real[row_idx, col_idx])
                
                pos = curr_ul + vec_x * (c + 0.5) + vec_y * (r + 0.5)
                num_txt = Text(real_val, font_size=8, color=MY_BLUE, weight=BOLD).move_to(pos).set_z_index(100)
                lbp_numbers.add(num_txt)

        self.play(
            FadeOut(flash_rect), 
            FadeIn(lbp_numbers),
            img_gray.animate.set(opacity=0.3), 
            run_time=0.3
        )
        self.wait(1)

        # =========================
        # 8. CƠN MƯA DỮ LIỆU & BIỂU ĐỒ HISTOGRAM THẬT
        # =========================
        self.play(Transform(label_flash, make_label("Tổng hợp thành Biểu đồ Histogram", bg_color=MY_RED).to_edge(UP, buff=0.1).set_z_index(10)))

        axes = Axes(
            x_range=[0, 280, 32], 
            y_range=[0, max_freq + int(2 * y_step), y_step], 
            x_length=9,     
            y_length=2.8,   
            axis_config={
                "color": BLACK, 
                "font_size": 14, 
                "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}
            },
        ).move_to(DOWN * 0.8).set_z_index(5)
        
        axes.add_coordinates()

        x_label = Text("Giá trị LBP (0 - 255)", font_size=14, color=BLACK).next_to(axes.x_axis, DOWN, buff=0.4).set_z_index(5)
        y_label = Text("Tần suất", font_size=14, color=BLACK).next_to(axes.y_axis, UP, buff=0.1).set_z_index(5)

        axes_bg = Rectangle(width=10.5, height=4.5, color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(axes).shift(DOWN*0.1)
        axes_bg.set_z_index(-1)

        self.play(FadeIn(axes_bg), Create(axes), FadeIn(x_label), FadeIn(y_label))

        bars = VGroup().set_z_index(2) 
        for i, h in enumerate(hist_real):
            x_val = i * 8 + 4 
            bottom_pos = axes.c2p(x_val, 0)
            top_pos = axes.c2p(x_val, h)
            bar_height = max(top_pos[1] - bottom_pos[1], 0.01) 
            
            bar = Rectangle(width=0.2, height=bar_height, fill_color=MY_BLUE, fill_opacity=0.9, stroke_width=0)
            bar.move_to(axes.c2p(x_val, h/2)) 
            bars.add(bar)

        fall_anims = []
        for num in lbp_numbers:
            fall_anims.append(FadeOut(num, shift=DOWN * np.random.uniform(2, 5)))
        
        fall_anims.append(FadeOut(txt_178, shift=DOWN * 3))
        fall_anims.append(FadeOut(txt_24, shift=DOWN * 3))
        fall_anims.append(FadeOut(dot_178))
        fall_anims.append(FadeOut(dot_24))

        grow_bars = [GrowFromEdge(bar, DOWN) for bar in bars]

        self.play(
            LaggedStart(*fall_anims, lag_ratio=0.005, run_time=3), 
            LaggedStart(*grow_bars, lag_ratio=0.1, run_time=3)     
        )
        self.wait(1)

        # =========================
        # 9. KẾT LUẬN HISTOGRAM
        # =========================
        # CẬP NHẬT FIX LỖI: Chỉ làm mờ last_scene_group (ảnh và lưới), không đụng chạm tới các ô vuông đã tiêu biến
        self.play(last_scene_group.animate.set(opacity=0.1))

        note = make_label("Mỗi khuôn mặt giờ đây là 1 'Biểu đồ' LBP độc nhất", font_size=24, bg_color=BLACK).set_z_index(10)
        note.next_to(label_flash, DOWN, buff=0.2)
        self.play(FadeIn(note, shift=DOWN))
        self.wait(2.5)
from manim import *
import os
import numpy as np

class Part5LBPRecognition(Scene):
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

        # =========================
        # 2. CHUYỂN CẢNH TỪ PHẦN 4
        # =========================
        try:
            csv_icon = ImageMobject(get_image_path("csv.jpg")).scale_to_fit_height(2.0).move_to(UP * 0.5).set_z_index(20)
        except:
            csv_icon = VGroup(
                Rectangle(width=2, height=2.5, color=WHITE).set_fill(MY_BLUE, 0.9),
                Text("CSV", font_size=32, color=WHITE, weight=BOLD)
            ).move_to(UP * 0.5).set_z_index(20)

        title_csv_large = make_label("File: dataset.csv", font_size=20, bg_color=BLACK).next_to(csv_icon, UP, buff=0.2).set_z_index(20)
        final_note = make_label("TRÍCH XUẤT & LƯU TRỮ HOÀN TẤT", font_size=24, bg_color=MY_GREEN).next_to(csv_icon, DOWN, buff=0.3).set_z_index(20)

        self.add(csv_icon, title_csv_large, final_note)
        self.wait(0.1)
        self.play(FadeOut(final_note), FadeOut(csv_icon), FadeOut(title_csv_large), run_time=0.5)

        phase_title = make_label("QUY TRÌNH NHẬN DIỆN (FACE RECOGNITION)", font_size=22, bg_color=MY_RED).to_edge(UP, buff=0.2).set_z_index(20)
        self.play(FadeIn(phase_title, shift=DOWN))

        # =========================
        # 3. VẼ BẢNG DATABASE CỐ ĐỊNH SẮC NÉT (Dữ liệu Part 4)
        # =========================
        db_data = [
            {"label": "A", "f1": "0.07", "f2": "0.05", "f256": "0.14", "v_n": r"V_{A} = [0.07, 0.05, \dots, 0.14]", "id": 1},
            {"label": "B", "f1": "0.06", "f2": "0.06", "f256": "0.10", "v_n": r"V_{B} = [0.06, 0.06, \dots, 0.10]", "id": 2},
            {"label": "C", "f1": "0.07", "f2": "0.07", "f256": "0.13", "v_n": r"V_{C} = [0.07, 0.07, \dots, 0.13]", "id": 3},
            {"label": "D", "f1": "0.05", "f2": "0.06", "f256": "0.08", "v_n": r"V_{D} = [0.05, 0.06, \dots, 0.08]", "id": 4},
            {"label": "E", "f1": "0.05", "f2": "0.05", "f256": "0.11", "v_n": r"V_{E} = [0.05, 0.05, \dots, 0.11]", "id": 5},
        ]

        table_ui = VGroup().set_z_index(10)
        
        top_y = 2.0
        cell_h = 0.55
        table_x = 2.8 
        table_w = 6.4

        db_title = Text("File: dataset.csv", font_size=18, color=BLACK, weight=BOLD)
        db_title_bg = SurroundingRectangle(db_title, color=WHITE, fill_opacity=1, buff=0.05)
        title_csv = VGroup(db_title_bg, db_title).move_to([table_x - table_w/2 + 1.2, top_y + 0.3, 0]).set_z_index(12)

        table_bg = Rectangle(width=table_w, height=cell_h*6, color=BLACK, stroke_width=2).move_to([table_x, top_y - cell_h*3, 0]).set_fill(WHITE, 0.95)
        table_ui.add(table_bg)

        for i in range(1, 6):
            y = top_y - i * cell_h
            table_ui.add(Line([table_x - table_w/2, y, 0], [table_x + table_w/2, y, 0], color=BLACK, stroke_width=1))

        left_x = table_x - table_w/2
        v_lines_x = [left_x + 1.6, left_x + 2.8, left_x + 4.0, left_x + 5.2]
        for vx in v_lines_x:
            table_ui.add(Line([vx, top_y, 0], [vx, top_y - cell_h*6, 0], color=BLACK, stroke_width=1))

        col_centers_x = [left_x + 0.8, left_x + 2.2, left_x + 3.4, left_x + 4.6, left_x + 5.8]

        headers_str = ["Label", "f1", "f2", "...", "f256"]
        for i, h in enumerate(headers_str):
            table_ui.add(Text(h, font_size=18, color=BLACK, weight=BOLD).move_to([col_centers_x[i], top_y - cell_h/2, 0]))

        self.play(FadeIn(table_ui), FadeIn(title_csv))

        table_content = Group().set_z_index(12)
        images_right = Group().set_z_index(12)

        for i, u in enumerate(db_data):
            y_row = top_y - cell_h*1.5 - i*cell_h 
            
            img_x_db = table_x + table_w/2 + 0.8
            img_mob = get_img(f"image_{u['id']}.jpg", h=cell_h*0.9, pos=[img_x_db, y_row, 0])
            images_right.add(img_mob)

            t_lbl = Text(u["label"], font_size=16, color=BLACK, weight=BOLD).move_to([col_centers_x[0], y_row, 0])
            t_f1 = Text(u["f1"], font_size=16, color=BLACK, weight=BOLD).move_to([col_centers_x[1], y_row, 0])
            t_f2 = Text(u["f2"], font_size=16, color=BLACK, weight=BOLD).move_to([col_centers_x[2], y_row, 0])
            t_dots = Text("...", font_size=16, color=BLACK, weight=BOLD).move_to([col_centers_x[3], y_row, 0])
            t_f256 = Text(u["f256"], font_size=16, color=BLACK, weight=BOLD).move_to([col_centers_x[4], y_row, 0])
            
            table_content.add(t_lbl, t_f1, t_f2, t_dots, t_f256)

        self.play(FadeIn(table_content), FadeIn(images_right))
        self.wait(1)

        # =========================
        # 4. CẤU HÌNH 3 BÀI TEST THRESHOLD = 0.65
        # =========================
        tests = [
            {
                "img": "image_5.jpg", "name": "Người E", 
                "raw": "[500, 502, ..., 1100]", "norm": "[0.05, 0.05, ..., 0.11]", 
                "v_math": r"V_{Test1} = [0.05, 0.05, \dots, 0.11]",
                "dists": [0.85, 0.62, 0.74, 0.91, 0.02], "target": "USER E"
            },
            {
                "img": "image_6.jpg", "name": "Người A (Ảnh khác)", 
                "raw": "[600, 400, ..., 1500]", "norm": "[0.06, 0.04, ..., 0.15]", 
                "v_math": r"V_{Test2} = [0.06, 0.04, \dots, 0.15]",
                "dists": [0.25, 0.52, 0.68, 0.71, 0.80], "target": "USER A" 
            },
            {
                "img": "image_7.jpg", "name": "Người lạ (Unknown)", 
                "raw": "[1200, 1500, ..., 1000]", "norm": "[0.12, 0.15, ..., 0.10]", 
                "v_math": r"V_{Test3} = [0.12, 0.15, \dots, 0.10]",
                "dists": [0.75, 0.82, 0.69, 0.77, 0.85], "target": "Unknown" 
            }
        ]

        def create_calc_box(test_math, db_math, d_val, is_min=False):
            calc_str = r"d = \sqrt{ \sum (p_i - q_i)^2 } = " + f"{d_val:.2f}"
            lines = VGroup(
                Text("So sánh khoảng cách (Euclidean Distance):", font_size=16, color=BLACK, weight=BOLD),
                MathTex(test_math, font_size=24, color=MY_RED),
                MathTex(db_math, font_size=24, color=MY_BLUE),
                MathTex(calc_str, font_size=28, color=MY_GREEN if is_min else MY_RED)
            ).arrange(DOWN, buff=0.1)
            bg = SurroundingRectangle(lines, color=MY_GREEN if is_min else MY_YELLOW, fill_color="#e9ffd1", fill_opacity=1, stroke_width=3, buff=0.15)
            return VGroup(bg, lines).move_to([table_x, -2.6, 0]).set_z_index(20)

        # =========================
        # 5. VÒNG LẶP TEST 3 ẢNH
        # =========================
        for t_idx, t_data in enumerate(tests):
            loop_lbl = make_label(f"Test {t_idx+1}/3: Nhận diện {t_data['name']}", font_size=18, bg_color=MY_BLUE).next_to(phase_title, DOWN, buff=0.3)
            self.play(FadeIn(loop_lbl))

            img_x = -4.7 
            img_y = 0.7 
            
            test_img = get_img(t_data["img"], h=2.2, pos=[img_x, img_y, 0]).set_z_index(5)
            lbl_img = make_label("Ảnh Input", font_size=16, color=WHITE, bg_color=BLACK).next_to(test_img, UP, buff=0.1)
            self.play(FadeIn(test_img, shift=RIGHT), FadeIn(lbl_img))

            step1_lbl = make_label("Trích xuất Histogram", font_size=14, color=WHITE, bg_color=BLACK).next_to(test_img, DOWN, buff=0.2).align_to(test_img, LEFT)
            mini_hist = create_mini_hist(w=1.5, h=0.5).next_to(step1_lbl, DOWN, buff=0.15)
            
            self.play(FadeIn(step1_lbl), FadeIn(mini_hist), run_time=0.5)
            self.wait(0.5)

            step2_lbl = make_label("Chuyển thành Vector thô", font_size=14, color=WHITE, bg_color=BLACK).move_to(step1_lbl)
            v_raw_text = make_label(t_data["raw"], font_size=14, color=BLACK, bg_color=MY_YELLOW).move_to(mini_hist)
            
            self.play(
                ReplacementTransform(step1_lbl, step2_lbl),
                ReplacementTransform(mini_hist, v_raw_text),
                run_time=0.8
            )
            self.wait(0.5)

            step3_lbl = make_label("Chuẩn hóa Vector", font_size=14, color=WHITE, bg_color=BLACK).move_to(step2_lbl)
            v_norm_text = make_label(t_data["norm"], font_size=16, color=BLACK, bg_color=MY_YELLOW).move_to(v_raw_text).set_z_index(10)
            
            self.play(
                ReplacementTransform(step2_lbl, step3_lbl),
                ReplacementTransform(v_raw_text, v_norm_text),
                run_time=0.8
            )
            self.wait(1)

            # =========================
            # 6. BẮT ĐẦU SO SÁNH
            # =========================
            scan_box = Rectangle(width=table_w + 0.1, height=cell_h*0.95, color=MY_YELLOW, stroke_width=3).set_z_index(15)
            scan_line = Line(color=MY_YELLOW, stroke_width=2)
            
            start_y_row = top_y - cell_h*1.5
            scan_box.move_to([table_x, start_y_row, 0])

            current_detail_box = VGroup()
            dist_grp = VGroup() 
            
            min_d = float('inf')
            best_idx = -1

            for i in range(5):
                y_row = top_y - cell_h*1.5 - i*cell_h
                dist_val = t_data["dists"][i]
                
                if dist_val < min_d:
                    min_d = dist_val
                    best_idx = i

                new_detail_box = create_calc_box(t_data["v_math"], db_data[i]["v_n"], dist_val, False)
                
                d_x_pos = table_x - table_w/2 - 0.5 
                new_dist_lbl_grp = make_label(f"d={dist_val:.2f}", font_size=16, color=BLACK, bg_color=MY_YELLOW).move_to([d_x_pos, y_row, 0]).set_z_index(16)

                anims = [
                    scan_box.animate.move_to([table_x, y_row, 0]).set_color(MY_YELLOW),
                    scan_line.animate.put_start_and_end_on(v_norm_text.get_right() + RIGHT*0.1, np.array([table_x - table_w/2 - 0.8, y_row, 0])).set_color(MY_YELLOW),
                ]
                
                if len(current_detail_box) == 0:
                    anims.append(FadeIn(new_detail_box))
                    anims.append(FadeIn(new_dist_lbl_grp))
                else:
                    anims.append(ReplacementTransform(current_detail_box, new_detail_box))
                    anims.append(ReplacementTransform(dist_grp, new_dist_lbl_grp))

                self.play(*anims, run_time=0.6)
                current_detail_box = new_detail_box
                dist_grp = new_dist_lbl_grp
                self.wait(0.3)

            threshold = 0.65
            is_matched = min_d < threshold

            best_y = top_y - cell_h*1.5 - best_idx*cell_h
            best_box = create_calc_box(t_data["v_math"], db_data[best_idx]["v_n"], min_d, is_matched)
            
            best_dist_grp = make_label(f"d={min_d:.2f}", font_size=16, color=BLACK, bg_color=MY_YELLOW).move_to([d_x_pos, best_y, 0]).set_z_index(16)

            self.play(
                scan_box.animate.move_to([table_x, best_y, 0]).set_color(MY_GREEN if is_matched else MY_RED),
                scan_line.animate.put_start_and_end_on(v_norm_text.get_right() + RIGHT*0.1, np.array([table_x - table_w/2 - 0.8, best_y, 0])).set_color(MY_GREEN if is_matched else MY_RED),
                ReplacementTransform(current_detail_box, best_box),
                ReplacementTransform(dist_grp, best_dist_grp),
                run_time=0.8
            )

            arrow_color = MY_GREEN if is_matched else MY_RED
            self.play(FadeOut(scan_line))
            
            success_arrow = DoubleArrow(
                start=v_norm_text.get_right() + RIGHT*0.1, 
                end=np.array([table_x - table_w/2, best_y, 0]), 
                color=arrow_color, stroke_width=4
            ).set_z_index(10)
            
            min_lbl = Text("MIN", font_size=14, color=arrow_color, weight=BOLD).next_to(success_arrow, DOWN, buff=0.05)
            self.play(GrowArrow(success_arrow), FadeIn(min_lbl))

            res_y_pos = -2.6 
            if is_matched:
                res_txt1 = make_label(f"Mở Khóa! MIN={min_d:.2f} < 0.65", font_size=16, color=WHITE, bg_color=MY_GREEN)
                res_txt2 = make_label(f"=> Khớp với: {t_data['target']}", font_size=18, color=WHITE, bg_color=MY_GREEN)
                res_grp = VGroup(res_txt1, res_txt2).arrange(DOWN, buff=0.1).move_to([img_x, res_y_pos, 0])
                
                self.play(FadeIn(res_grp, shift=UP))
                self.wait(3.5)
            else:
                res_txt1 = make_label(f"Từ Chối! MIN={min_d:.2f} > 0.65", font_size=16, color=WHITE, bg_color=MY_RED)
                res_txt2 = make_label(f"=> Không tìm thấy người khớp.", font_size=18, color=WHITE, bg_color=MY_RED)
                res_grp = VGroup(res_txt1, res_txt2).arrange(DOWN, buff=0.1).move_to([img_x, res_y_pos, 0])
                
                self.play(FadeIn(res_grp, shift=UP))
                self.wait(3.5)

            self.play(FadeOut(Group(
                test_img, lbl_img, step3_lbl, v_norm_text, scan_box, dist_grp, best_dist_grp, best_box, loop_lbl, res_grp, success_arrow, min_lbl
            )))

        # =========================
        # KẾT THÚC TOÀN BỘ: VĂNG CÁC OBJECT RA THEO LỀ GẦN NHẤT
        # =========================
        out_animations = []
        for m in self.mobjects:
            # Bỏ qua background (được thiết lập z_index = -10 từ đầu)
            if m.z_index == -10:
                continue
            
            x, y, _ = m.get_center()
            # Tính khoảng cách đến các lề (khung chuẩn Manim width~14.2, height~8)
            dist_up = 4.0 - y
            dist_down = y - (-4.0)
            dist_right = 7.1 - x
            dist_left = x - (-7.1)
            
            min_dist = min(dist_up, dist_down, dist_right, dist_left)
            
            # Bay ra hướng nào gần nhất
            if min_dist == dist_up:
                direction = UP * 10
            elif min_dist == dist_down:
                direction = DOWN * 10
            elif min_dist == dist_right:
                direction = RIGHT * 15
            else:
                direction = LEFT * 15
                
            out_animations.append(m.animate.shift(direction))

        if out_animations:
            self.play(*out_animations, run_time=1.5, rate_func=smooth)
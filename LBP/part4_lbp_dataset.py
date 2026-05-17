from manim import *
import os
import numpy as np

class Part4LBPDataset(Scene):
    def construct(self):
        MY_BLUE = "#0055FF"
        MY_RED = "#FF0000"
        MY_GREEN = "#00AA00"

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

        def get_lbp_data(filename):
            try:
                img_c = ImageMobject(get_image_path(filename))
                px = img_c.get_pixel_array()
                gray = np.dot(px[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
                padded = np.pad(gray, 1, mode='constant', constant_values=0)
                center = padded[1:-1, 1:-1]
                lbp = np.zeros_like(center, dtype=np.uint8)
                for dr, dc, bit in [(-1,-1,128), (-1,0,64), (-1,1,32), (0,1,16), (1,1,8), (1,0,4), (1,-1,2), (0,-1,1)]:
                    lbp |= np.where(padded[1+dr:1+dr+gray.shape[0], 1+dc:1+dc+gray.shape[1]] >= center, bit, 0).astype(np.uint8)
                hist, _ = np.histogram(lbp, bins=32, range=(0, 256))
                gray_rgba = np.stack([gray]*3 + [px[..., 3]], axis=-1)
                img_g = ImageMobject(gray_rgba)
                return img_c, img_g, hist
            except:
                img_c = Rectangle(width=3.2, height=3.9).set_fill(WHITE, 1)
                img_g = Rectangle(width=3.2, height=3.9).set_fill(GRAY, 1)
                return img_c, img_g, np.random.randint(10, 100, 32)

        def create_mini_hist(hist_data, w=1.5, h=0.6):
            group = VGroup()
            max_h = max(hist_data) if max(hist_data) > 0 else 1
            bar_w = w / 16 
            for val in hist_data[:16]:
                bh = max((val / max_h) * h, 0.05)
                rect = Rectangle(width=bar_w*0.8, height=bh, fill_color=MY_BLUE, fill_opacity=0.9, stroke_width=0)
                group.add(rect)
            group.arrange(RIGHT, aligned_edge=DOWN, buff=bar_w*0.2)
            base = Line(group.get_corner(DL) + LEFT*0.1, group.get_corner(DR) + RIGHT*0.1, color=BLACK, stroke_width=2)
            return VGroup(base, group).set_z_index(5)

        # =========================
        # 2. TÁI HIỆN CHÍNH XÁC CẢNH CUỐI PHẦN 3
        # =========================
        box_w, box_h = 3.2, 3.9
        _, img_g_1, hist_real_1 = get_lbp_data("image_1.jpg")
        img_g_1.stretch_to_fit_width(box_w).stretch_to_fit_height(box_h).set_z_index(0).set(opacity=0.1)

        red_box = Rectangle(width=box_w, height=box_h, color=MY_RED, stroke_width=4).set_z_index(1)
        grid = VGroup(*[Line(red_box.get_corner(UL) + RIGHT*i*(box_w/16), red_box.get_corner(DL) + RIGHT*i*(box_w/16), stroke_width=1, stroke_opacity=0.4) for i in range(1, 16)]).set_z_index(1)
        for i in range(1, 16): grid.add(Line(red_box.get_corner(UL) + DOWN*i*(box_w/16), red_box.get_corner(UR) + DOWN*i*(box_w/16), stroke_width=1, stroke_opacity=0.4))
        
        face_group_1 = Group(img_g_1, red_box, grid).move_to(UP * 2.2).scale(0.65)
        
        max_freq_1 = int(max(hist_real_1))
        y_step_1 = max(1, max_freq_1 // 4)
        axes = Axes(
            x_range=[0, 280, 32], 
            y_range=[0, max_freq_1 + int(2 * y_step_1), y_step_1], 
            x_length=9, y_length=2.8, 
            axis_config={"color": BLACK, "font_size": 14, "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}
        ).move_to(DOWN * 0.8).set_z_index(5)
        axes.add_coordinates() 
        
        x_label = Text("Giá trị LBP (0 - 255)", font_size=14, color=BLACK).next_to(axes.x_axis, DOWN, buff=0.4).set_z_index(5)
        y_label = Text("Tần suất", font_size=14, color=BLACK).next_to(axes.y_axis, UP, buff=0.1).set_z_index(5)
        axes_bg = Rectangle(width=10.5, height=4.5, color=WHITE, fill_opacity=0.9, stroke_width=0).move_to(axes).shift(DOWN*0.1).set_z_index(-1)
        
        bars = VGroup().set_z_index(2) 
        for i, h in enumerate(hist_real_1):
            x_val = i * 8 + 4 
            bar = Rectangle(width=0.2, height=max(axes.c2p(x_val, h)[1] - axes.c2p(x_val, 0)[1], 0.01), fill_color=MY_BLUE, fill_opacity=0.9, stroke_width=0)
            bar.move_to(axes.c2p(x_val, h/2)) 
            bars.add(bar)
            
        hist_big = Group(axes_bg, axes, x_label, y_label, bars)

        label_flash = make_label("Tổng hợp thành Biểu đồ Histogram", bg_color=MY_RED).to_edge(UP, buff=0.1).set_z_index(10)
        note = make_label("Mỗi khuôn mặt giờ đây là 1 'Biểu đồ' LBP độc nhất", font_size=24, bg_color=BLACK).next_to(label_flash, DOWN, buff=0.2).set_z_index(10)

        self.add(face_group_1, hist_big, label_flash, note)
        self.wait(1.5)

        # =========================
        # 3. DÀN HÀNG NGANG 5 USER (Slower entrance)
        # =========================
        self.play(FadeOut(label_flash), FadeOut(note), FadeOut(red_box), FadeOut(grid), img_g_1.animate.set(opacity=1), run_time=0.5)

        x_coords = [-5.6, -2.8, 0, 2.8, 5.6]
        pos_y_lbl = UP * 3.0
        pos_y_img = UP * 1.8
        pos_y_hist = UP * 0.5 

        hist_A_mini = create_mini_hist(hist_real_1).move_to(pos_y_hist + RIGHT * x_coords[0])
        name_A = make_label("User A", 14, bg_color=MY_RED).move_to(pos_y_lbl + RIGHT * x_coords[0]).set_z_index(10)
        
        self.play(
            img_g_1.animate.scale(0.8).move_to(pos_y_img + RIGHT * x_coords[0]),
            ReplacementTransform(hist_big, hist_A_mini),
            FadeIn(name_A),
            run_time=1.5, rate_func=smooth
        )

        users = [{"name": "User A", "img": img_g_1, "hist": hist_A_mini, "lbl": name_A, "raw": hist_real_1}]
        filenames = ["image_2.jpg", "image_3.jpg", "image_4.jpg", "image_5.jpg"]
        names = ["User B", "User C", "User D", "User E"]

        for i in range(4):
            _, img_temp, h_real = get_lbp_data(filenames[i])
            img_temp.stretch_to_fit_width(box_w).stretch_to_fit_height(box_h)
            img_temp.scale(0.65 * 0.8).move_to(pos_y_img + RIGHT * x_coords[i+1]).set_z_index(5)
            
            h_mini = create_mini_hist(h_real).move_to(pos_y_hist + RIGHT * x_coords[i+1])
            lbl_temp = make_label(names[i], 14, bg_color=MY_RED).move_to(pos_y_lbl + RIGHT * x_coords[i+1]).set_z_index(10)
            
            self.play(FadeIn(img_temp, shift=DOWN*0.5), FadeIn(h_mini), FadeIn(lbl_temp), run_time=0.6)
            users.append({"name": names[i], "img": img_temp, "hist": h_mini, "lbl": lbl_temp, "raw": h_real})
        self.wait(1)

        # =========================
        # 4. HISTOGRAM -> VECTOR THÔ (RAW) VÀ GIẢI THÍCH
        # =========================
        info_txt = make_label("Chuyển Biểu đồ thành Vector tần suất thô", font_size=20, bg_color=MY_BLUE).move_to(DOWN * 1.5).set_z_index(20)
        self.play(FadeIn(info_txt))

        # Vector Thô: Chữ Xanh Dương
        for u in users:
            u["raw_vals"] = [int(x) for x in u["raw"][:3]] + [int(u["raw"][-1])]
            
            u["vec_ui"] = VGroup().set_z_index(15)
            u["ngoac_mo"] = Text("[", font_size=14, color=MY_BLUE, weight=BOLD)
            u["n1"] = Text(str(u["raw_vals"][0]), font_size=14, color=MY_BLUE, weight=BOLD)
            u["c1"] = Text(",", font_size=14, color=MY_BLUE, weight=BOLD)
            u["n2"] = Text(str(u["raw_vals"][1]), font_size=14, color=MY_BLUE, weight=BOLD)
            u["c2"] = Text(",", font_size=14, color=MY_BLUE, weight=BOLD)
            u["dots"] = Text("...", font_size=14, color=MY_BLUE, weight=BOLD)
            u["n256"] = Text(str(u["raw_vals"][3]), font_size=14, color=MY_BLUE, weight=BOLD)
            u["ngoac_dong"] = Text("]", font_size=14, color=MY_BLUE, weight=BOLD)
            
            u["vec_ui"].add(u["ngoac_mo"], u["n1"], u["c1"], u["n2"], u["c2"], u["dots"], u["n256"], u["ngoac_dong"])
            u["vec_ui"].arrange(RIGHT, buff=0.05)
            
            u["c1"].align_to(u["n1"], DOWN).shift(DOWN*0.03)
            u["c2"].align_to(u["n2"], DOWN).shift(DOWN*0.03)
            u["dots"].align_to(u["n2"], DOWN)
            
            u["vec_ui"].move_to(u["hist"].get_center())
            u["raw_grp"] = u["vec_ui"] 

        self.play(ReplacementTransform(users[0]["hist"], users[0]["raw_grp"]), run_time=0.8)
        
        val_0 = users[0]['raw_vals'][0] 
        target_obj = users[0]["n1"]
        
        # Mũi tên và Text được xích ra phải một chút (RIGHT * 0.5) để không bị ép sát lề
        expl_arrow = Arrow(
            start=target_obj.get_bottom() + DOWN*0.9 + RIGHT*0.4, 
            end=target_obj.get_bottom(), 
            color=MY_RED, 
            tip_length=0.15 * 1.5 
        ).scale(1.5).set_z_index(20) 

        expl_txt = make_label(f"f1: LBP=0\nxuất hiện {val_0} lần", font_size=12, color=WHITE, bg_color=BLACK).next_to(expl_arrow.get_start(), DOWN+RIGHT, buff=0.05).shift(LEFT*0.3).set_z_index(20)
        
        self.play(FadeIn(expl_arrow), FadeIn(expl_txt))
        self.wait(2.5)
        self.play(FadeOut(expl_arrow), FadeOut(expl_txt))

        self.play(*[ReplacementTransform(users[i]["hist"], users[i]["raw_grp"]) for i in range(1, 5)], run_time=1)
        self.wait(0.5)

        # =========================
        # 5. CHUẨN HÓA (NORMALIZATION)
        # =========================
        formula_grp = VGroup().set_z_index(30)
        txt_form1 = Text("Chuẩn hóa (Normalization):", font_size=16, color=WHITE)
        math_form = MathTex(r"v_{norm} = \frac{v_i}{\sum_{k=1}^{256} v_k}", font_size=32, color=YELLOW)
        
        total_A = sum(users[0]["raw"])
        ex_A = Text(f"Ví dụ User A (f1): {val_0} / {total_A} = {val_0/total_A:.2f}", font_size=14, color=MY_GREEN)
        
        content_grp = VGroup(txt_form1, math_form, ex_A).arrange(DOWN, buff=0.15)
        bg_form = SurroundingRectangle(content_grp, color=YELLOW, fill_color=BLACK, fill_opacity=0.95, buff=0.2)
        formula_grp.add(bg_form, content_grp).move_to(DOWN * 0.8)

        self.play(FadeOut(info_txt, shift=UP), FadeIn(formula_grp, shift=UP))
        self.wait(2)

        # Vector Chuẩn hóa: Đổi sang CHỮ ĐEN
        for u in users:
            total = sum(u["raw"])
            u["n1_norm"] = Text(f"{u['raw_vals'][0]/total:.2f}", font_size=14, color=BLACK, weight=BOLD).move_to(u["n1"])
            u["n2_norm"] = Text(f"{u['raw_vals'][1]/total:.2f}", font_size=14, color=BLACK, weight=BOLD).move_to(u["n2"])
            u["n256_norm"] = Text(f"{u['raw_vals'][3]/total:.2f}", font_size=14, color=BLACK, weight=BOLD).move_to(u["n256"])

        self.play(
            Transform(users[0]["n1"], users[0]["n1_norm"]),
            Transform(users[0]["n2"], users[0]["n2_norm"]),
            Transform(users[0]["n256"], users[0]["n256_norm"]),
            run_time=0.8
        )
        self.wait(0.5)

        self.play(*[
            AnimationGroup(
                Transform(users[i]["n1"], users[i]["n1_norm"]),
                Transform(users[i]["n2"], users[i]["n2_norm"]),
                Transform(users[i]["n256"], users[i]["n256_norm"])
            ) for i in range(1, 5)
        ], run_time=1)
        self.wait(1)
        self.play(FadeOut(formula_grp))

        # =========================
        # 6. BẢNG DATASET.CSV
        # =========================
        table_top_y = DOWN * 0.4
        row_height = 0.45

        csv_title = Text("File dataset.csv", font_size=18, color=BLACK, weight=BOLD)
        csv_bg = SurroundingRectangle(csv_title, color=WHITE, fill_opacity=1, buff=0.05)
        csv_label = VGroup(csv_bg, csv_title).move_to(table_top_y + UP*0.25 + LEFT*1.8).set_z_index(12)

        table_ui = VGroup().set_z_index(10)
        table_bg = Rectangle(width=8.0, height=2.8, color=BLACK, stroke_width=2).set_fill(WHITE, 0.95).move_to(table_top_y + DOWN*1.4 + LEFT*1.0)
        table_ui.add(table_bg)

        for i in range(1, 6):
            y = table_top_y[1] - i * row_height
            table_ui.add(Line(LEFT*5.0 + UP*y, RIGHT*3.0 + UP*y, color=BLACK, stroke_width=1))
        
        x_lines = [-5.0, -3.2, -1.8, -0.4, 1.2, 3.0]
        for x in x_lines[1:-1]:
            table_ui.add(Line(RIGHT*x + UP*table_top_y[1], RIGHT*x + DOWN*3.3, color=BLACK, stroke_width=1))

        h_y = table_top_y[1] - row_height/2
        headers = [
            Text("Label", font_size=16, color=BLACK, weight=BOLD).move_to([ -4.1, h_y, 0 ]),
            Text("f1", font_size=16, color=BLACK, weight=BOLD).move_to([ -2.5, h_y, 0 ]),
            Text("f2", font_size=16, color=BLACK, weight=BOLD).move_to([ -1.1, h_y, 0 ]),
            Text("...", font_size=16, color=BLACK, weight=BOLD).move_to([ 0.4, h_y, 0 ]),
            Text("f256", font_size=16, color=BLACK, weight=BOLD).move_to([ 2.1, h_y, 0 ])
        ]
        table_ui.add(*headers)

        self.play(FadeIn(table_ui, shift=UP), FadeIn(csv_label))

        # =========================
        # 7. DI CHUYỂN TỪNG SỐ VÀO BẢNG (FIX LỖI LẤY SỐ CHUẨN HÓA)
        # =========================
        all_table_content = Group().set_z_index(15)
        all_images_out = Group().set_z_index(15) 

        for i, u in enumerate(users):
            cell_y = table_top_y[1] - (i + 1) * row_height - row_height/2
            
            dest_label = np.array([-4.1, cell_y, 0])
            dest_f1 = np.array([-2.5, cell_y, 0])
            dest_f2 = np.array([-1.1, cell_y, 0])
            dest_dots = np.array([0.4, cell_y, 0])
            dest_f256 = np.array([2.1, cell_y, 0])
            dest_img = np.array([4.5, cell_y, 0]) 
            
            self.play(
                FadeOut(u["ngoac_mo"]), FadeOut(u["c1"]), FadeOut(u["c2"]), FadeOut(u["ngoac_dong"]),
                run_time=0.2
            )

            t_name = Text(u["name"].replace("User ", ""), font_size=16, color=BLACK, weight=BOLD).move_to(u["lbl"].get_center()).set_z_index(20)
            
            # FIX: Lấy đích danh .text của n1_norm (số đã chuẩn hóa hệ 0.xx) chứ KHÔNG phải text của số đếm thô
            dest_n1 = Text(u["n1_norm"].text, font_size=16, color=BLACK, weight=BOLD).move_to(u["n1"].get_center()).set_z_index(20)
            dest_n2 = Text(u["n2_norm"].text, font_size=16, color=BLACK, weight=BOLD).move_to(u["n2"].get_center()).set_z_index(20)
            dest_ndots = Text(u["dots"].text, font_size=16, color=BLACK, weight=BOLD).move_to(u["dots"].get_center()).set_z_index(20)
            dest_n256 = Text(u["n256_norm"].text, font_size=16, color=BLACK, weight=BOLD).move_to(u["n256"].get_center()).set_z_index(20)

            self.remove(u["lbl"], u["n1"], u["n2"], u["dots"], u["n256"])
            self.add(t_name, dest_n1, dest_n2, dest_ndots, dest_n256)

            self.play(
                t_name.animate.move_to(dest_label),
                dest_n1.animate.move_to(dest_f1),
                dest_n2.animate.move_to(dest_f2),
                dest_ndots.animate.move_to(dest_dots),
                dest_n256.animate.move_to(dest_f256),
                u["img"].animate.scale_to_fit_height(row_height * 0.9).move_to(dest_img),
                run_time=0.6, rate_func=smooth
            )
            all_table_content.add(t_name, dest_n1, dest_n2, dest_ndots, dest_n256)
            all_images_out.add(u["img"])

        # =========================
        # 8. KẾT MÀN (ẢNH LƯỚT RA -> FILE CSV -> HOÀN TẤT)
        # =========================
        self.wait(1)
        self.play(FadeOut(all_images_out, shift=RIGHT), run_time=1)
        self.wait(0.5)

        try:
            csv_img = ImageMobject(get_image_path("csv.jpg")).scale_to_fit_height(2.0).move_to(UP * 0.5).set_z_index(20)
        except:
            csv_img = Group(Rectangle(width=2, height=2.5, color=WHITE).set_fill(MY_BLUE, 0.9), Text("CSV", font_size=32, color=WHITE, weight=BOLD)).move_to(UP * 0.5).set_z_index(20)

        title_csv = make_label("File: dataset.csv", font_size=20, bg_color=BLACK).next_to(csv_img, UP, buff=0.2)
        final_note = make_label("TRÍCH XUẤT & LƯU TRỮ HOÀN TẤT", font_size=24, bg_color=MY_GREEN).next_to(csv_img, DOWN, buff=0.3)

        self.play(
            FadeOut(csv_label),
            table_ui.animate.scale(0.1).move_to(UP * 0.5).set(opacity=0),
            all_table_content.animate.scale(0.1).move_to(UP * 0.5).set(opacity=0),
            run_time=1.2
        )
        
        self.play(
            FadeIn(csv_img, scale=0.5), FadeIn(title_csv, shift=DOWN), FadeIn(final_note, shift=UP),
            run_time=1
        )
        self.wait(1)
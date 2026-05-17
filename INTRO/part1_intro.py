from manim import *
import os

class Part1ModernTech(Scene):
    def construct(self):
        MY_CYAN = "#0088FF"
        MY_RED = "#FF0000"
        MY_YELLOW = "#FF7B00"

        # =========================
        # 0. NỀN TỔNG THỂ (HCMUS BACKGROUND) - SÁNG RÕ 100%
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
        # 0.5 MÀN HÌNH GIỚI THIỆU ĐỒ ÁN
        # =========================
        intro_title = Text("ĐỒ ÁN CÁ NHÂN", font_size=48, color=MY_YELLOW, weight=BOLD)
        intro_subject = Text("Môn học: Nhận Dạng", font_size=36, color="#22FF00")
        intro_author = Text("Sinh viên thực hiện: Thông Lúc - 22120196", font_size=32, color=MY_CYAN)
        
        intro_group = VGroup(intro_title, intro_subject, intro_author).arrange(DOWN, buff=0.5)
        
        # Thêm một lớp nền đen mờ đằng sau chữ để đọc rõ hơn
        intro_bg = SurroundingRectangle(intro_group, color=MY_CYAN, fill_color="#F0EDB4", fill_opacity=0.8, stroke_width=2, buff=0.5, corner_radius=0.2)
        intro_full = Group(intro_bg, intro_group) 

        self.play(DrawBorderThenFill(intro_bg), run_time=1)
        self.play(Write(intro_title), run_time=1)
        self.play(FadeIn(intro_subject, shift=UP), run_time=0.8)
        self.play(FadeIn(intro_author, shift=UP), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(intro_full, shift=DOWN), run_time=1)

        # =========================
        # HỆ QUY CHIẾU TỌA ĐỘ & HELPER 
        # =========================
        PHONE_H = 3.6 
        PHONE_W = 1.9 
        CENTER_Y = -0.8
        LABEL_Y = CENTER_Y - PHONE_H / 2 - 0.4             

        pos1_x = -4.5
        pos2_x = 0
        pos3_x = 4.5

        def create_phone_base():
            body = RoundedRectangle(height=PHONE_H, width=PHONE_W, corner_radius=0.25, color=WHITE).set_fill(BLACK, 0.85)
            screen = Rectangle(height=PHONE_H-0.5, width=PHONE_W-0.15).set_fill(BLACK, 1)
            screen.move_to(body.get_top() + DOWN * (screen.height/2 + 0.1))
            
            btn = Circle(radius=0.1).set_fill(WHITE, 1).set_stroke(width=0)
            btn.move_to(body.get_bottom() + UP * 0.15)
            return VGroup(body, screen, btn), screen 

        def fit_img_to_screen(filename, screen, fallback_color=BLUE):
            try:
                img = ImageMobject(get_image_path(filename))
                img.scale_to_fit_width(screen.width)
                if img.height > screen.height:
                    img.scale_to_fit_height(screen.height)
                img.move_to(screen.get_center())
                return img
            except:
                return Rectangle(height=screen.height, width=screen.width).set_fill(fallback_color, 0.6).move_to(screen.get_center())

        def make_label(text_str):
            txt = Text(text_str, font_size=14, color=WHITE, weight=BOLD)
            bg = SurroundingRectangle(txt, color=BLACK, fill_opacity=0.8, stroke_width=0, buff=0.1)
            return Group(bg, txt)

        # =========================
        # 1. SETUP: FACE ID (Trái)
        # =========================
        phone_ui1, screen1 = create_phone_base()
        
        # Thay đổi: Setup cả 2 ảnh LP và face_ai
        img_lp = fit_img_to_screen("LP.jpg", screen1, GRAY)
        img_face = fit_img_to_screen("face_ai.jpg", screen1, BLUE_E)
        img_face.set_opacity(0) # Ẩn ảnh face_ai ban đầu
        
        phone1_grp = Group(phone_ui1, img_lp, img_face).move_to([pos1_x, CENTER_Y, 0])
        lbl1 = make_label("Mở khóa bằng FaceID").move_to([pos1_x, LABEL_Y, 0])
        g1_all = Group(phone1_grp, lbl1).shift(DOWN * 8) 

        # =========================
        # 2. SETUP: TIKTOK (Giữa)
        # =========================
        phone_ui2, screen2 = create_phone_base()
        tk1 = fit_img_to_screen("tiktok01.jpg", screen2, GRAY)
        tk2 = fit_img_to_screen("tiktok02.jpg", screen2, PINK)
        
        phone2_grp = Group(phone_ui2, tk1, tk2).move_to([pos2_x, CENTER_Y, 0])
        tk2.move_to(tk1) 
        tk2.set_opacity(0) 
        
        lbl2 = make_label("Filter biến hình").move_to([pos2_x, LABEL_Y, 0])
        g2_all = Group(phone2_grp, lbl2).shift(DOWN * 8)

        # =========================
        # 3. SETUP: VISUAL SEARCH (Phải)
        # =========================
        phone_ui3, screen3 = create_phone_base()
        search_img = fit_img_to_screen("search.jpg", screen3, GREEN_E)
        
        phone3_grp = Group(phone_ui3, search_img).move_to([pos3_x, CENTER_Y, 0])
        
        try:
            luffy_img = ImageMobject(get_image_path("luffy.jpg")).scale_to_fit_height(1.4)
        except:
            luffy_img = Rectangle(height=1.4, width=1.4).set_fill(MY_RED, 0.8)
            
        luffy_border = SurroundingRectangle(luffy_img, color=WHITE, buff=0, stroke_width=3)
        luffy_grp = Group(luffy_border, luffy_img).next_to(phone3_grp, UP, buff=0.2)
        
        lbl3 = make_label("Tìm kiếm bằng hình ảnh").move_to([pos3_x, LABEL_Y, 0])
        g3_all = Group(phone3_grp, luffy_grp, lbl3).shift(DOWN * 8)

        # =========================
        # 4. ANIMATION: SỰ HIỆN DIỆN CỦA CÔNG NGHỆ
        # =========================
        main_title_text = Text("SỰ HIỆN DIỆN CỦA CÔNG NGHỆ NHẬN DIỆN", font_size=28, color=MY_YELLOW, weight=BOLD)
        main_title_bg = SurroundingRectangle(main_title_text, color=BLACK, fill_color="#F5F4E1", fill_opacity=0.8, stroke_width=0, buff=0.15, corner_radius=0.1)
        main_title_grp = Group(main_title_bg, main_title_text).to_edge(UP, buff=0.4)

        self.play(FadeIn(main_title_grp, shift=DOWN))
        
        self.play(
            g1_all.animate.shift(UP * 8),
            g2_all.animate.shift(UP * 8),
            g3_all.animate.shift(UP * 8),
            run_time=1.5, rate_func=smooth
        )
        self.wait(0.5)

        # --- Hiệu ứng 1: Quét FaceID ---
        scan_line = Line(LEFT, RIGHT, color=MY_CYAN).set_stroke(width=6).scale(screen1.width/2).move_to(screen1.get_top())
        scan_glow = Rectangle(width=screen1.width, height=0.4, color=MY_CYAN, fill_opacity=0.3, stroke_width=0).next_to(scan_line, UP, buff=0)
        scan_beam = VGroup(scan_line, scan_glow)

        self.play(FadeIn(scan_beam))
        
        # Thay đổi: Thanh quét di chuyển đến cuối khung hình
        self.play(scan_beam.animate.move_to(screen1.get_bottom()), run_time=1.5, rate_func=smooth)
        
        # Thay đổi: Sau khi quét xong mới đồng thời mờ ảnh LP đi và hiện ảnh face_ai lên
        self.play(
            img_lp.animate.set_opacity(0),
            img_face.animate.set_opacity(1),
            run_time=0.3
        )
        
        self.play(FadeOut(scan_beam), Flash(screen1.get_center(), color=MY_CYAN, line_length=0.5))
        self.wait(0.5)

        # --- Hiệu ứng 2: TikTok Filter ---
        self.play(Indicate(phone_ui2, color="#00FFEA", scale_factor=1.05), run_time=1)
        self.play(tk1.animate.set_opacity(0), tk2.animate.set_opacity(1), run_time=0.8)
        self.wait(0.5)

        # --- Hiệu ứng 3: Visual Search ---
        search_beam = Polygon(
            screen3.get_top() + LEFT*0.4,
            screen3.get_top() + RIGHT*0.4,
            luffy_grp.get_corner(DR),
            luffy_grp.get_corner(DL),
            color=MY_CYAN, fill_opacity=0.2, stroke_width=0
        )
        self.play(FadeIn(search_beam))
        
        target_box = SurroundingRectangle(luffy_grp, color=MY_CYAN, stroke_width=4)
        self.play(Create(target_box))
        self.play(Flash(target_box, color=MY_CYAN))
        
        self.play(FadeOut(search_beam), FadeOut(target_box))
        self.wait(2)

        # =========================
        # 5. OUTRO: DI CHUYỂN TẤT CẢ KHỎI KHUNG HÌNH (TRỪ BACKGROUND)
        # =========================
        self.play(
            main_title_grp.animate.shift(UP * 5),       
            g1_all.animate.shift(LEFT * 10),            
            g2_all.animate.shift(DOWN * 10),            
            g3_all.animate.shift(RIGHT * 10),           
            run_time=2,
            rate_func=rush_into
        )
        
        self.wait(1)
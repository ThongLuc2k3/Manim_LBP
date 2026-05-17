import os

# 1. Điền đường dẫn chính xác tới các file mp4 đã render của bạn
# Lưu ý: Sửa lại tên file và đường dẫn cho khớp với cấu trúc máy bạn
video_files = [
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part1_intro/1080p60/Part1ModernTech.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part2_blackbox/1080p60/Part2BlackBox.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part3_timetravel/1080p60/Part3TimeTravel.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part4_classical/1080p60/Part4ClassicalMethods.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part1_lbp_intro/1080p60/Part1LBPIntro.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part2_lbp_zoom/1080p60/Part2LBPZoom.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part3_lbp_histogram/1080p60/Part3LBPHistogram.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part4_lbp_dataset/1080p60/Part4LBPDataset.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part5_lbp_recognition/1080p60/Part5LBPRecognition.mp4",
    "/home/thongluc/Khóa Luận Tốt Nghiệp/Manim_PCA/media/videos/part6_lbp_limitations/1080p60/Part6LBPLimitations.mp4"
]

# 2. Tạo file text chứa danh sách video theo cú pháp của FFmpeg
list_file = "video_list.txt"
with open(list_file, "w", encoding="utf-8") as f:
    for vid in video_files:
        # Nếu đường dẫn có dấu cách, FFmpeg vẫn hiểu nhờ có dấu nháy đơn
        f.write(f"file '{vid}'\n")

print("Đang tiến hành nối video...")

# 3. Chạy lệnh FFmpeg để copy và nối luồng video (Siêu tốc, không làm giảm chất lượng)
output_name = "FULL_VIDEO_LBP_1080p60.mp4"
command = f'ffmpeg -y -f concat -safe 0 -i {list_file} -c copy "{output_name}"'

os.system(command)

# 4. Dọn dẹp file rác
if os.path.exists(list_file):
    os.remove(list_file)

print(f"✅ ĐÃ XONG! Video hoàn chỉnh của bạn là: {output_name}")
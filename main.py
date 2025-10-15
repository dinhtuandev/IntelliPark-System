import cv2
import matplotlib.pyplot as plt
import numpy as np

from util import get_parking_spots_bboxes, empty_or_not, calculate_parking_stats, export_parking_stats, get_parking_status_summary


def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))


mask = './mask_1920_1080.png'
video_path = './data/parking_1920_1080.mp4'


mask = cv2.imread(mask, 0)

cap = cv2.VideoCapture(video_path)
# Thêm cấu hình ghi video đầu ra
writer = None
output_path = './output.mp4'
# tìm các vùng chỗ đỗ xe
connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S) #nhóm vùng trong mask

spots = get_parking_spots_bboxes(connected_components) # trả về danh sách các bbox [x1, y1, w, h] cho từng ô đỗ
# biến trạng thái
spots_status = [None for j in spots] #bool từng trạng thái từng ô (true = trống, false = có xe)
diffs = [None for j in spots] #diff giữa 2 frame (làm tăng độ nhạy của hệ thống)

previous_frame = None

frame_nmr = 0
ret = True
step = 30 #tần suất lấy frame

# Thêm biến để track xe
total_spots = len(spots)
available_spots = 0
occupied_spots = 0

print("=== PARKING SPACE COUNTER ===")
print(f"Total parking spots detected: {total_spots}")
print("Controls:")
print("- Press 'q' to quit")
print("- Press 'e' to export current statistics")
print("- Press 's' to show status summary in console")

while ret:
    ret, frame = cap.read()

    if frame_nmr % step == 0 and previous_frame is not None:
        for spot_indx, spot in enumerate(spots):
            x1, y1, w, h = spot

            spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

            diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w, :])

        print([diffs[j] for j in np.argsort(diffs)][::-1])

    if frame_nmr % step == 0:
        if previous_frame is None:
            arr_ = range(len(spots))
        else:
            arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
        for spot_indx in arr_:
            spot = spots[spot_indx]
            x1, y1, w, h = spot

            spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

            spot_status = empty_or_not(spot_crop)

            spots_status[spot_indx] = spot_status

    if frame_nmr % step == 0:
        previous_frame = frame.copy()

    # Cập nhật số liệu thống kê
    available_spots = sum(spots_status) if any(spots_status) else 0
    occupied_spots = total_spots - available_spots

    for spot_indx, spot in enumerate(spots):
        spot_status = spots_status[spot_indx]
        x1, y1, w, h = spots[spot_indx]

        if spot_status:
            frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        else:
            frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

    # Cải thiện giao diện hiển thị thông tin
    # Background cho thông tin
    cv2.rectangle(frame, (20, 20), (600, 120), (0, 0, 0), -1)
    cv2.rectangle(frame, (20, 20), (600, 120), (255, 255, 255), 2)
    
    # Hiển thị thông tin chi tiết
    cv2.putText(frame, 'PARKING LOT STATUS', (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, 'Available spots: {} / {}'.format(available_spots, total_spots), (30, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, 'Occupied spots: {} / {}'.format(occupied_spots, total_spots), (30, 95), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Hiển thị tỷ lệ sử dụng
    if total_spots > 0:
        occupancy_rate = (occupied_spots / total_spots) * 100
        cv2.putText(frame, 'Occupancy Rate: {:.1f}%'.format(occupancy_rate), (350, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Khởi tạo writer khi có frame đầu tiên
    if writer is None and ret and frame is not None:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps is None or fps <= 0:
            fps = 30.0
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (frame.shape[1], frame.shape[0]))

    if writer is not None:
        writer.write(frame)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)
    
    # Xử lý phím bấm
    key = cv2.waitKey(25) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        # Export thống kê
        if any(spots_status):
            filename = export_parking_stats(spots_status)
            print(f"Statistics exported to: {filename}")
        else:
            print("No data to export yet. Wait for analysis to complete.")
    elif key == ord('s'):
        # Hiển thị summary trong console
        if any(spots_status):
            print(get_parking_status_summary(spots_status))
        else:
            print("No data to show yet. Wait for analysis to complete.")

    frame_nmr += 1

# Hiển thị thống kê cuối cùng
if any(spots_status):
    print("\n=== FINAL STATISTICS ===")
    print(get_parking_status_summary(spots_status))

cap.release()
if writer is not None:
    writer.release()
cv2.destroyAllWindows()

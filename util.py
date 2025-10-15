import pickle
import json
from datetime import datetime

from skimage.transform import resize
import numpy as np
import cv2


EMPTY = True
NOT_EMPTY = False

MODEL = pickle.load(open("model/model.p", "rb"))


def empty_or_not(spot_bgr):

    flat_data = []

    img_resized = resize(spot_bgr, (15, 15, 3))
    flat_data.append(img_resized.flatten())
    flat_data = np.array(flat_data)

    y_output = MODEL.predict(flat_data)

    if y_output == 0:
        return EMPTY
    else:
        return NOT_EMPTY


def get_parking_spots_bboxes(connected_components):
    (totalLabels, label_ids, values, centroid) = connected_components

    slots = []
    coef = 1
    for i in range(1, totalLabels):

        # Now extract the coordinate points
        x1 = int(values[i, cv2.CC_STAT_LEFT] * coef)
        y1 = int(values[i, cv2.CC_STAT_TOP] * coef)
        w = int(values[i, cv2.CC_STAT_WIDTH] * coef)
        h = int(values[i, cv2.CC_STAT_HEIGHT] * coef)

        slots.append([x1, y1, w, h])

    return slots


def calculate_parking_stats(spots_status):
    """
    Tính toán thống kê bãi xe
    """
    if not spots_status:
        return {
            'total_spots': 0,
            'available_spots': 0,
            'occupied_spots': 0,
            'occupancy_rate': 0.0
        }
    
    total_spots = len(spots_status)
    available_spots = sum(spots_status) if any(spots_status) else 0
    occupied_spots = total_spots - available_spots
    occupancy_rate = (occupied_spots / total_spots) * 100 if total_spots > 0 else 0
    
    return {
        'total_spots': total_spots,
        'available_spots': available_spots,
        'occupied_spots': occupied_spots,
        'occupancy_rate': round(occupancy_rate, 1)
    }


def export_parking_stats(spots_status, filename=None):
    """
    Export thống kê bãi xe ra file JSON
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"parking_stats_{timestamp}.json"
    
    stats = calculate_parking_stats(spots_status)
    stats['timestamp'] = datetime.now().isoformat()
    stats['spots_detail'] = [
        {
            'spot_id': i,
            'status': 'empty' if status else 'occupied',
            'coordinates': spots_status[i] if i < len(spots_status) else None
        }
        for i, status in enumerate(spots_status)
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    return filename


def get_parking_status_summary(spots_status): # tạm thời chưa giải quyết được việc hiển thị icon trong console chính sử dụng hàm nay
    """
    Trả về summary text của trạng thái bãi xe
    """
    stats = calculate_parking_stats(spots_status)
    
    summary = f"""
PARKING LOT STATUS SUMMARY
==========================
Total Spots: {stats['total_spots']}
Available Spots: {stats['available_spots']} (🟢)
Occupied Spots: {stats['occupied_spots']} (🔴)
Occupancy Rate: {stats['occupancy_rate']}%

Status: {'🟢 Good' if stats['occupancy_rate'] < 80 else '🟡 Moderate' if stats['occupancy_rate'] < 95 else '🔴 Full'}
    """
    
    return summary.strip()


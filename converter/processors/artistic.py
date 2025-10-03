# converter/processors/artistic.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class OutlineProcessor(BaseImageProcessor):
    """아웃라인만 추출"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        gray = self.to_gray(image)
        edges = cv2.Canny(gray, 50, 150)
        
        # 흰 배경에 검은 선
        white_bg = np.ones_like(image) * 255
        white_bg[edges != 0] = 0
        
        return white_bg


class PointillismProcessor(BaseImageProcessor):
    """점묘화 효과"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        
        # 흰 캔버스
        canvas = np.ones((h, w, 3), dtype=np.uint8) * 255
        
        # 랜덤하게 점 찍기
        num_points = (h * w) // 50  # 점의 개수 조절
        
        for _ in range(num_points):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            
            # 해당 위치의 색상 가져오기
            color = tuple(map(int, image[y, x]))
            
            # 점 그리기
            cv2.circle(canvas, (x, y), 2, color, -1)
        
        return canvas


class VintageProcessor(BaseImageProcessor):
    """빈티지/세피아 효과"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # 세피아 변환 매트릭스
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        
        return sepia
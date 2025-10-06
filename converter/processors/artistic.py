# converter/processors/artistic.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class OutlineProcessor(BaseImageProcessor):
    """아웃라인만 추출"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'threshold1',
                'type': 'int',
                'default': 50,
                'min': 10,
                'max': 150,
                'step': 10,
                'description': '낮은 임계값'
            },
            {
                'name': 'threshold2',
                'type': 'int',
                'default': 150,
                'min': 50,
                'max': 300,
                'step': 10,
                'description': '높은 임계값'
            }
        ]
    
    def process(self, image: np.ndarray, threshold1=50, threshold2=150) -> np.ndarray:
        gray = self.to_gray(image)
        edges = cv2.Canny(gray, threshold1, threshold2)
        
        # 흰 배경에 검은 선
        white_bg = np.ones_like(image) * 255
        white_bg[edges != 0] = 0
        
        return white_bg

class PointillismProcessor(BaseImageProcessor):
    """점묘화 효과"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'point_density',
                'type': 'int',
                'default': 15,        # 50 → 15로 변경 (더 적은 점)
                'min': 5,
                'max': 50,
                'step': 5,
                'description': '점 밀집도 (작을수록 점이 큼)'
            },
            {
                'name': 'point_size',
                'type': 'int',
                'default': 8,         # 2 → 8로 변경 (더 큰 점)
                'min': 3,
                'max': 20,
                'step': 1,
                'description': '점 크기'
            }
        ]
    
    def process(self, image: np.ndarray, point_density=15, point_size=8) -> np.ndarray:
        h, w = image.shape[:2]
        
        # 흰 캔버스
        canvas = np.ones((h, w, 3), dtype=np.uint8) * 255
        
        # 점의 개수 계산 (더 적게)
        num_points = (h * w) // point_density
        
        for _ in range(num_points):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            
            # 해당 위치의 색상 가져오기
            color = tuple(map(int, image[y, x]))
            
            # 점 그리기 (더 크게)
            cv2.circle(canvas, (x, y), point_size, color, -1)
        
        return canvas
class VintageProcessor(BaseImageProcessor):
    """빈티지/세피아 효과"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'intensity',
                'type': 'float',
                'default': 1.0,
                'min': 0.5,
                'max': 1.5,
                'step': 0.1,
                'description': '세피아 강도'
            }
        ]
    
    def process(self, image: np.ndarray, intensity=1.0) -> np.ndarray:
        # 세피아 변환 매트릭스
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]]) * intensity
        
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        
        return sepia
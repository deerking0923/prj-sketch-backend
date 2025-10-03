# converter/processors/sketch.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class PencilSketchProcessor(BaseImageProcessor):
    """연필 스케치 변환"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'blur_size',
                'type': 'int',
                'default': 21,
                'min': 5,
                'max': 51,
                'step': 2,
                'description': '블러 크기 (홀수만 가능, 클수록 부드러움)'
            },
            {
                'name': 'scale',
                'type': 'float',
                'default': 256.0,
                'min': 100.0,
                'max': 400.0,
                'step': 10.0,
                'description': '스케치 강도'
            }
        ]
    
    def process(self, image: np.ndarray, blur_size=21, scale=256.0) -> np.ndarray:
        # blur_size는 홀수여야 함
        if blur_size % 2 == 0:
            blur_size += 1
        
        gray = self.to_gray(image)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (blur_size, blur_size), 0)
        inverted_blurred = cv2.bitwise_not(blurred)
        sketch = cv2.divide(gray, inverted_blurred, scale=scale)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


class ColorPencilSketchProcessor(BaseImageProcessor):
    """컬러 연필 스케치"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'sigma_s',
                'type': 'int',
                'default': 60,
                'min': 20,
                'max': 200,
                'step': 10,
                'description': '공간 범위 (클수록 색상 영역이 넓어짐)'
            },
            {
                'name': 'sigma_r',
                'type': 'float',
                'default': 0.07,
                'min': 0.01,
                'max': 0.2,
                'step': 0.01,
                'description': '색상 범위 (클수록 더 강한 효과)'
            }
        ]
    
    def process(self, image: np.ndarray, sigma_s=60, sigma_r=0.07) -> np.ndarray:
        _, color_sketch = cv2.pencilSketch(
            image, 
            sigma_s=sigma_s, 
            sigma_r=sigma_r, 
            shade_factor=0.05
        )
        return color_sketch


class InkDrawingProcessor(BaseImageProcessor):
    """잉크 드로잉 / 펜화"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'threshold1',
                'type': 'int',
                'default': 50,
                'min': 10,
                'max': 200,
                'step': 10,
                'description': '낮은 임계값 (작을수록 더 많은 선)'
            },
            {
                'name': 'threshold2',
                'type': 'int',
                'default': 150,
                'min': 50,
                'max': 300,
                'step': 10,
                'description': '높은 임계값 (클수록 주요 선만)'
            },
            {
                'name': 'line_thickness',
                'type': 'int',
                'default': 1,
                'min': 0,
                'max': 5,
                'step': 1,
                'description': '선 굵기 (0=얇음, 5=두꺼움)'
            }
        ]
    
    def process(self, image: np.ndarray, threshold1=50, threshold2=150, line_thickness=1) -> np.ndarray:
        gray = self.to_gray(image)
        edges = cv2.Canny(gray, threshold1, threshold2)
        
        # 선 굵기 조절
        if line_thickness > 0:
            kernel = np.ones((line_thickness, line_thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
        
        # 흰 배경에 검은 선
        inverted = cv2.bitwise_not(edges)
        return cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)


class DetailedSketchProcessor(BaseImageProcessor):
    """디테일한 스케치 (Sobel 엣지 사용)"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'ksize',
                'type': 'int',
                'default': 3,
                'min': 1,
                'max': 7,
                'step': 2,
                'description': 'Sobel 커널 크기 (클수록 굵은 선)'
            }
        ]
    
    def process(self, image: np.ndarray, ksize=3) -> np.ndarray:
        gray = self.to_gray(image)
        
        # Sobel 엣지 검출
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        
        # 결합
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = np.uint8(edges / edges.max() * 255)
        
        # 반전 (흰 배경)
        inverted = cv2.bitwise_not(edges)
        return cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)
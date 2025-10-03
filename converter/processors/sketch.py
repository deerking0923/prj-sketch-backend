# converter/processors/sketch.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class PencilSketchProcessor(BaseImageProcessor):
    """연필 스케치 변환"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        gray = self.to_gray(image)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        inverted_blurred = cv2.bitwise_not(blurred)
        sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


class ColorPencilSketchProcessor(BaseImageProcessor):
    """컬러 연필 스케치"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # OpenCV의 내장 함수 사용
        _, color_sketch = cv2.pencilSketch(
            image, 
            sigma_s=60, 
            sigma_r=0.07, 
            shade_factor=0.05
        )
        return color_sketch


class InkDrawingProcessor(BaseImageProcessor):
    """잉크 드로잉 / 펜화"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        gray = self.to_gray(image)
        edges = cv2.Canny(gray, 100, 200)
        # 선을 더 굵게 만들기
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        # 흰 배경에 검은 선
        inverted = cv2.bitwise_not(edges)
        return cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)


class DetailedSketchProcessor(BaseImageProcessor):
    """디테일한 스케치 (Sobel 엣지 사용)"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        gray = self.to_gray(image)
        
        # Sobel 엣지 검출
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # 결합
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = np.uint8(edges / edges.max() * 255)
        
        # 반전 (흰 배경)
        inverted = cv2.bitwise_not(edges)
        return cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)
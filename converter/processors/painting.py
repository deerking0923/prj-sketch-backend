# converter/processors/painting.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class CartoonProcessor(BaseImageProcessor):
    """카툰화 효과"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # 색상 단순화
        color = cv2.bilateralFilter(image, 9, 250, 250)
        
        # 엣지 검출
        gray = self.to_gray(image)
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9, 2
        )
        
        # 엣지를 컬러 이미지와 합성
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges_colored)
        
        return cartoon


class OilPaintingProcessor(BaseImageProcessor):
    """유화 효과"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # 여러 번 median blur 적용
        result = image.copy()
        for _ in range(2):
            result = cv2.medianBlur(result, 7)
        
        # 디테일 강화
        result = cv2.bilateralFilter(result, 9, 75, 75)
        return result


class WatercolorProcessor(BaseImageProcessor):
    """수채화 효과"""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # stylization 함수 사용
        result = cv2.stylization(image, sigma_s=60, sigma_r=0.6)
        return result


class MosaicProcessor(BaseImageProcessor):
    """모자이크/타일 아트"""
    
    def __init__(self, tile_size: int = 10):
        self.tile_size = tile_size
    
    def process(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        
        # 작은 크기로 축소 후 다시 확대
        small = cv2.resize(
            image,
            (w // self.tile_size, h // self.tile_size),
            interpolation=cv2.INTER_LINEAR
        )
        
        mosaic = cv2.resize(
            small,
            (w, h),
            interpolation=cv2.INTER_NEAREST
        )
        
        return mosaic
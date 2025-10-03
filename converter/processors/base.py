# converter/processors/base.py
import cv2
import numpy as np
from abc import ABC, abstractmethod

class BaseImageProcessor(ABC):
    """모든 이미지 프로세서의 기본 클래스"""
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        이미지를 처리하는 메인 메서드
        Args:
            image: OpenCV 형식의 이미지 (BGR)
        Returns:
            처리된 이미지 (BGR)
        """
        pass
    
    @staticmethod
    def to_gray(image: np.ndarray) -> np.ndarray:
        """이미지를 그레이스케일로 변환"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
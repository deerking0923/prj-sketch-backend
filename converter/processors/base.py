# converter/processors/base.py
import cv2
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseImageProcessor(ABC):
    """모든 이미지 프로세서의 기본 클래스"""
    
    # 각 프로세서가 지원하는 파라미터 정의
    @classmethod
    def get_parameters(cls) -> List[Dict[str, Any]]:
        """
        프로세서가 지원하는 파라미터 정보 반환
        Returns:
            List[Dict]: 파라미터 정보 리스트
            예: [
                {
                    'name': 'intensity',
                    'type': 'int',
                    'default': 5,
                    'min': 1,
                    'max': 10,
                    'description': '효과 강도'
                }
            ]
        """
        return []
    
    @abstractmethod
    def process(self, image: np.ndarray, **params) -> np.ndarray:
        """
        이미지를 처리하는 메인 메서드
        Args:
            image: OpenCV 형식의 이미지 (BGR)
            **params: 파라미터들
        Returns:
            처리된 이미지 (BGR)
        """
        pass
    
    @staticmethod
    def to_gray(image: np.ndarray) -> np.ndarray:
        """이미지를 그레이스케일로 변환"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
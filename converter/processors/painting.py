# converter/processors/painting.py
import cv2
import numpy as np
from .base import BaseImageProcessor

class CartoonProcessor(BaseImageProcessor):
    """카툰화 효과"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'color_levels',
                'type': 'int',
                'default': 9,
                'min': 3,
                'max': 20,
                'step': 1,
                'description': '색상 단순화 레벨'
            },
            {
                'name': 'edge_thickness',
                'type': 'int',
                'default': 9,
                'min': 3,
                'max': 15,
                'step': 2,
                'description': '윤곽선 감지 범위'
            },
            {
                'name': 'line_thickness',
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 5,
                'step': 1,
                'description': '선 굵기'
            }
        ]
    
    def process(self, image: np.ndarray, color_levels=9, edge_thickness=9, line_thickness=1) -> np.ndarray:
        # 색상 단순화
        color = cv2.bilateralFilter(image, color_levels, 250, 250)
        
        # 엣지 검출
        gray = self.to_gray(image)
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            edge_thickness, 2
        )
        
        # 선 굵기 조정
        if line_thickness > 1:
            kernel = np.ones((line_thickness, line_thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
        
        # 엣지를 컬러 이미지와 합성
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(color, edges_colored)
        
        return cartoon

# converter/processors/painting.py (OilPaintingProcessor만 수정)
import cv2
import numpy as np
from .base import BaseImageProcessor

class OilPaintingProcessor(BaseImageProcessor):
    """유화 효과 - 명암에 따른 붓터치"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'brush_size',
                'type': 'int',
                'default': 7,
                'min': 3,
                'max': 15,
                'step': 2,
                'description': '붓 크기'
            },
            {
                'name': 'brush_intensity',
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 10,
                'step': 1,
                'description': '붓터치 강도'
            }
        ]
    
    def process(self, image: np.ndarray, brush_size=7, brush_intensity=5) -> np.ndarray:
        """
        명암 그라디언트에 따라 붓터치 방향을 결정하는 유화 효과
        """
        # 1. 색상 단순화 (유화 느낌)
        result = image.copy()
        for _ in range(2):
            result = cv2.bilateralFilter(result, 9, 75, 75)
        
        # 2. 그레이스케일로 변환하여 명암 분석
        gray = self.to_gray(image)
        
        # 3. Sobel로 그라디언트 방향 계산
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # 그라디언트 크기와 방향
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        angle = np.arctan2(sobely, sobelx)
        
        # 4. 붓터치 효과 적용
        h, w = image.shape[:2]
        canvas = result.copy()
        
        # 일정 간격으로 붓터치 샘플링
        step = brush_size
        for y in range(0, h, step):
            for x in range(0, w, step):
                if magnitude[y, x] > 10:  # 엣지가 있는 부분만
                    # 그라디언트 방향에 수직으로 붓터치
                    direction = angle[y, x] + np.pi/2
                    
                    # 붓터치 길이
                    length = int(brush_size * 1.5)
                    
                    # 시작점과 끝점 계산
                    x1 = int(x - length/2 * np.cos(direction))
                    y1 = int(y - length/2 * np.sin(direction))
                    x2 = int(x + length/2 * np.cos(direction))
                    y2 = int(y + length/2 * np.sin(direction))
                    
                    # 범위 체크
                    if 0 <= x < w and 0 <= y < h:
                        color = tuple(map(int, result[y, x]))
                        
                        # 붓터치 그리기 (선 굵기는 brush_intensity로 조절)
                        cv2.line(canvas, (x1, y1), (x2, y2), color, 
                                max(1, brush_intensity // 2), cv2.LINE_AA)
        
        # 5. 원본과 블렌딩하여 자연스럽게
        alpha = 0.7
        result = cv2.addWeighted(result, alpha, canvas, 1-alpha, 0)
        
        # 6. 약간의 질감 추가
        result = cv2.medianBlur(result, 3)
        
        return result


class WatercolorProcessor(BaseImageProcessor):
    """수채화 효과"""
    
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
                'description': '공간 범위'
            },
            {
                'name': 'sigma_r',
                'type': 'float',
                'default': 0.6,
                'min': 0.1,
                'max': 1.0,
                'step': 0.1,
                'description': '색상 범위'
            }
        ]
    
    def process(self, image: np.ndarray, sigma_s=60, sigma_r=0.6) -> np.ndarray:
        result = cv2.stylization(image, sigma_s=sigma_s, sigma_r=sigma_r)
        return result


class MosaicProcessor(BaseImageProcessor):
    """모자이크/타일 아트"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'tile_size',
                'type': 'int',
                'default': 10,
                'min': 5,
                'max': 50,
                'step': 5,
                'description': '타일 크기'
            }
        ]
    
    def process(self, image: np.ndarray, tile_size=10) -> np.ndarray:
        h, w = image.shape[:2]
        
        small = cv2.resize(
            image,
            (w // tile_size, h // tile_size),
            interpolation=cv2.INTER_LINEAR
        )
        
        mosaic = cv2.resize(
            small,
            (w, h),
            interpolation=cv2.INTER_NEAREST
        )
        
        return mosaic


class CelShadingProcessor(BaseImageProcessor):
    """셀 쉐이딩 (애니메이션 스타일)"""
    
    @classmethod
    def get_parameters(cls):
        return [
            {
                'name': 'levels',
                'type': 'int',
                'default': 8,
                'min': 3,
                'max': 20,
                'step': 1,
                'description': '색상 레벨'
            },
            {
                'name': 'with_edges',
                'type': 'bool',
                'default': True,
                'description': '윤곽선 추가'
            },
            {
                'name': 'line_thickness',
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 5,
                'step': 1,
                'description': '선 굵기'
            }
        ]
    
    def process(self, image: np.ndarray, levels=8, with_edges=True, line_thickness=1) -> np.ndarray:
        # HSV로 변환
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        h_div = 180 // levels
        s_div = 256 // levels
        v_div = 256 // levels
        
        # 색상 양자화
        hsv[:, :, 0] = (hsv[:, :, 0] // h_div) * h_div + h_div // 2
        hsv[:, :, 1] = (hsv[:, :, 1] // s_div) * s_div + s_div // 2
        
        v = hsv[:, :, 2]
        v = (v // v_div) * v_div + v_div // 2
        
        # 최소 밝기 보정
        min_brightness = 30
        mask = v < min_brightness
        v[mask] = min_brightness + (v[mask] * 50 // min_brightness)
        
        hsv[:, :, 2] = np.clip(v, 0, 255)
        
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # 윤곽선 추가
        if with_edges:
            gray = self.to_gray(image)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9, 5
            )
            
            # 선 굵기 조정
            if line_thickness > 1:
                kernel = np.ones((line_thickness, line_thickness), np.uint8)
                edges = cv2.dilate(edges, kernel, iterations=1)
            
            # 검은 윤곽선 적용
            result[edges < 128] = [0, 0, 0]
        
        return result
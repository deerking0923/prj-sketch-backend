# converter/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from PIL import Image
import numpy as np
import io
import cv2
import base64

from .processors import ProcessorFactory

class ImageViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def convert_image(self, request):
        if 'image' not in request.data:
            return Response({'error': '이미지 파일이 누락되었습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 변환 스타일 선택 (기본값: pencil_sketch)
        style = request.data.get('style', 'pencil_sketch')
        
        uploaded_file = request.data['image']

        try:
            # 1. 파일 로드 및 OpenCV 포맷으로 변환
            image_data = uploaded_file.read()
            image = Image.open(io.BytesIO(image_data))
            numpy_image = np.array(image.convert('RGB')) 
            cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            
            # 2. 선택된 스타일로 변환
            processor = ProcessorFactory.get_processor(style)
            converted_image = processor.process(cv_image)
            
            # 3. 변환된 이미지를 Base64 문자열로 인코딩
            _, buffer = cv2.imencode('.png', converted_image) 
            base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            # 4. 최종 응답
            return Response({
                'message': '이미지 변환 성공',
                'file_name': uploaded_file.name,
                'style': style,
                'sketch_image_base64': base64_encoded_image
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'이미지 처리 중 오류 발생: {str(e)}'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def styles(self, request):
        """사용 가능한 변환 스타일 목록 반환"""
        return Response({
            'styles': ProcessorFactory.available_styles()
        })
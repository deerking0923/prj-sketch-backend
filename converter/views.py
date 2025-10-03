from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
import numpy as np
import io
import cv2
import base64

class ImageViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def convert_image(self, request):
        if 'image' not in request.data:
            return Response({'error': '이미지 파일이 누락되었습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.data['image']

        try:
            # 1. 파일 로드 및 OpenCV 포맷으로 변환
            image_data = uploaded_file.read()
            image = Image.open(io.BytesIO(image_data))
            numpy_image = np.array(image.convert('RGB')) 
            cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            
            # 2. OpenCV 연필 스케치 변환 로직
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            inverted_gray_image = cv2.bitwise_not(gray_image)
            blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
            inverted_blurred_image = cv2.bitwise_not(blurred_image)
            sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
            
            # 3. 변환된 이미지를 Base64 문자열로 인코딩
            _, buffer = cv2.imencode('.png', sketch_image) 
            base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            # 4. 최종 응답: Base64 문자열을 JSON 형태로 반환
            return Response({
                'message': '이미지 변환 성공',
                'file_name': uploaded_file.name,
                'sketch_image_base64': base64_encoded_image
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # 예외 발생 시 상세 오류 메시지 반환
            return Response({'error': f'이미지 처리 중 오류 발생: {str(e)}'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

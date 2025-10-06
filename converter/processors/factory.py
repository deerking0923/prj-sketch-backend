# converter/processors/factory.py
from .sketch import (
    InkDrawingProcessor,
    DetailedSketchProcessor
)
from .painting import (
    CartoonProcessor,
    OilPaintingProcessor,
    WatercolorProcessor,
    MosaicProcessor,
    CelShadingProcessor
)
from .artistic import (
    PointillismProcessor
)

class ProcessorFactory:
    """변환 타입에 따라 적절한 프로세서를 반환"""
    
    PROCESSORS = {
        'ink_drawing': InkDrawingProcessor,
        'detailed_sketch': DetailedSketchProcessor,
        'oil_painting': OilPaintingProcessor,
        'cartoon': CartoonProcessor,
        'watercolor': WatercolorProcessor,
        'mosaic': MosaicProcessor,
        'cel_shading': CelShadingProcessor,
        'pointillism': PointillismProcessor,
    }
    
    @classmethod
    def get_processor(cls, style: str):
        """스타일 이름으로 프로세서 인스턴스 반환"""
        processor_class = cls.PROCESSORS.get(style)
        if processor_class is None:
            raise ValueError(f"Unknown style: {style}. Available: {list(cls.PROCESSORS.keys())}")
        return processor_class()
    
    @classmethod
    def available_styles(cls):
        """사용 가능한 모든 스타일 목록과 파라미터 정보 반환"""
        styles = {}
        for style_name, processor_class in cls.PROCESSORS.items():
            styles[style_name] = {
                'name': style_name,
                'parameters': processor_class.get_parameters()
            }
        return styles
    
    @classmethod
    def get_style_info(cls, style: str):
        """특정 스타일의 파라미터 정보 반환"""
        processor_class = cls.PROCESSORS.get(style)
        if processor_class is None:
            raise ValueError(f"Unknown style: {style}")
        return {
            'name': style,
            'parameters': processor_class.get_parameters()
        }
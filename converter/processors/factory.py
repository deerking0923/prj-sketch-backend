# converter/processors/factory.py
from .sketch import (
    PencilSketchProcessor,
    ColorPencilSketchProcessor,
    InkDrawingProcessor,
    DetailedSketchProcessor
)
from .painting import (
    CartoonProcessor,
    OilPaintingProcessor,
    WatercolorProcessor,
    MosaicProcessor
)
from .artistic import (
    OutlineProcessor,
    PointillismProcessor,
    VintageProcessor
)

class ProcessorFactory:
    """변환 타입에 따라 적절한 프로세서를 반환"""
    
    PROCESSORS = {
        'pencil_sketch': PencilSketchProcessor,
        'color_pencil': ColorPencilSketchProcessor,
        'ink_drawing': InkDrawingProcessor,
        'detailed_sketch': DetailedSketchProcessor,
        'cartoon': CartoonProcessor,
        'oil_painting': OilPaintingProcessor,
        'watercolor': WatercolorProcessor,
        'mosaic': MosaicProcessor,
        'outline': OutlineProcessor,
        'pointillism': PointillismProcessor,
        'vintage': VintageProcessor,
    }
    
    @classmethod
    def get_processor(cls, style: str):
        """
        스타일 이름으로 프로세서 인스턴스 반환
        Args:
            style: 변환 스타일 이름
        Returns:
            BaseImageProcessor 인스턴스
        """
        processor_class = cls.PROCESSORS.get(style)
        if processor_class is None:
            raise ValueError(f"Unknown style: {style}. Available: {list(cls.PROCESSORS.keys())}")
        return processor_class()
    
    @classmethod
    def available_styles(cls):
        """사용 가능한 모든 스타일 목록 반환"""
        return list(cls.PROCESSORS.keys())
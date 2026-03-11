from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

class GripperCmd(BaseModel):
    gripper: int = Field(..., ge=10, le=170, description="그리퍼의 개폐 각도", examples=[40])



class PosCmd(BaseModel):
    pos:list[float] = Field(..., description="목표 XYZ 좌표", examples=[[0.2, 0.0, 0.15]])   



class TorqueCmd(BaseModel):
    torque:int = Field(..., ge=0, le=1, description="서보의 토크 ON (1) / OFF (0)", examples=[0])



class EEPosition(BaseModel):
    x:float = Field(..., description="엔드이펙터 X 좌표", examples=[0.21])
    y:float = Field(..., description="엔드이펙터 Y 좌표", examples=[-0.03])
    z:float = Field(..., description="엔드이펙터 Z 좌표", examples=[0.18])

class StatusResponse(BaseModel):
    ee:EEPosition = Field(..., description="현재 엔드이펙터 좌표")
    joints:list[int] = Field(
        ...,
        description="""
        현재 로봇 관절 각도 (deg)
        joints[0] : J1 베이스 회전
        joints[1] : J2 어깨
        joints[2] : J3 팔꿈치
        joints[3] : J4 손목 Pitch
        joints[4] : J5 손목 회전
        joints[5] : J6 그리퍼
        """)



T = TypeVar("T")
class CommonResponse(BaseModel, Generic[T]):
    success:bool
    data:Optional[T] = None
from fastapi import APIRouter, status
from .schema import GripperCmd, PosCmd, TorqueCmd, StatusResponse, CommonResponse
from ..robot import shared

router = APIRouter(tags=["Robot"], prefix="/robot")


@router.get("/state",
             summary="로봇 상태",
             description="로봇의 현재 상태를 반환한다.",
             response_model=CommonResponse[StatusResponse])
def get_status():
    with shared.state_lock:
        robot_packet = {
            'ee': shared.robot_state.copy(),
            'joints': shared.joints_degrees[:]
        }
    
    return CommonResponse(
        success=True,
        data=StatusResponse(**robot_packet)
    )



@router.post("/set_pos",
             summary="엔드이펙터 좌표 이동",
             description="엔드이펙터를 목표 XYZ 좌표로 이동시킨다.",
             response_model=CommonResponse,
             status_code=status.HTTP_201_CREATED)
def set_pos(pos:PosCmd):
    with shared.cmd_lock:
        shared.command["target_pos"] = pos.pos
    
    return CommonResponse(
        success=True,
        data=pos
        )



@router.post("/set_gripper",
             summary="그리퍼 개폐 각도 설정",
             description="그리퍼의 개폐 각도를 설정한다.",
             response_model=CommonResponse,
             status_code=status.HTTP_201_CREATED)
def set_gripper(gripper:GripperCmd):
    with shared.cmd_lock:
        shared.command["gripper_cmd"] = gripper.gripper
    return CommonResponse(
        success=True,
        data=gripper
        )



@router.post("/set_torque",
             summary="서보 토크 설정",
             description="모든 서보의 토크 ON / OFF 를 설정한다.",
             response_model=CommonResponse,
             status_code=status.HTTP_201_CREATED)
def set_torque(torque:TorqueCmd):
    with shared.cmd_lock:
        shared.command["torque_cmd"] = torque.torque
    
    return CommonResponse(
        success=True,
        data=torque
        )
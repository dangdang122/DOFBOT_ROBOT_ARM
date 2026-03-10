# DOFBOT Robot Server API Guide

## 1. 개요

본 서버는 **DOFBOT 로봇팔을 원격으로 제어하기 위한 Socket.IO 기반 API**를 제공한다.

클라이언트는 서버에 연결하여 다음 기능을 사용할 수 있다.

- 로봇 엔드이펙터 XYZ 좌표 이동
- 그리퍼 열기 / 닫기 제어
- 서보 토크 ON / OFF
- 로봇 상태 실시간 수신

서버는 약 **20Hz (0.05초 주기)** 로 로봇 상태를 클라이언트에게 자동으로 전송한다.

---

# 2. 서버 연결

## 프로토콜

Socket.IO

## 서버 주소 예시

```
http://<ROBOT_SERVER_IP>:5000
```

클라이언트가 서버에 연결하면 별도의 요청 없이 다음 이벤트를 지속적으로 수신한다.

```
robot_state
```

---

# 3. 로봇 상태 (Server → Client)

## robot_state

서버는 로봇의 현재 상태를 지속적으로 전송한다.

### 이벤트 이름

```
robot_state
```

### 데이터 구조

```json
{
  "ee": {
    "x": float,
    "y": float,
    "z": float
  },
  "joints": [j1, j2, j3, j4, j5, j6]
}
```

### 필드 설명

| 필드 | 설명 |
|-----|-----|
| ee.x | 엔드이펙터 X 좌표 |
| ee.y | 엔드이펙터 Y 좌표 |
| ee.z | 엔드이펙터 Z 좌표 |
| joints[0] | J1 베이스 회전 |
| joints[1] | J2 어깨 |
| joints[2] | J3 팔꿈치 |
| joints[3] | J4 손목 Pitch |
| joints[4] | J5 손목 회전 |
| joints[5] | J6 그리퍼 |

### 데이터 예시

```json
{
  "ee": {
    "x": 0.21,
    "y": -0.03,
    "z": 0.18
  },
  "joints": [90, 45, 30, 60, 120, 80]
}
```

### 해석 예시

```
J5 = 120도
J6 = 80도
```

의미

- 손목 회전 (J5) = 120°
- 그리퍼 개방 정도 (J6) = 80°

---

# 4. 클라이언트 제어 명령 (Client → Server)

클라이언트는 다음 명령을 서버로 보낼 수 있다.

| 명령 | 설명 |
|-----|-----|
| set_pos | 엔드이펙터 좌표 이동 |
| set_gripper | 그리퍼 개폐 |
| set_torque | 서보 토크 ON / OFF |

---

# 4.1 엔드이펙터 좌표 이동

### 이벤트 이름

```
set_pos
```

### 설명

엔드이펙터를 목표 XYZ 좌표로 이동시킨다.

서버는 내부적으로 **Inverse Kinematics (IK)** 를 계산하여 각 관절 각도를 구한 후 로봇을 이동시킨다.

### 데이터 형식

```json
{
  "pos": [x, y, z]
}
```

### 예시

```javascript
socket.emit("set_pos", {
  pos: [0.2, 0.0, 0.15]
});
```

### 의미

```
X = 0.2
Y = 0.0
Z = 0.15
```

로봇이 해당 좌표로 이동한다.

---

# 4.2 그리퍼 제어

### 이벤트 이름

```
set_gripper
```

### 설명

그리퍼의 개폐 각도를 설정한다.

### 데이터 형식

```json
{
  "gripper": angle
}
```

### 각도 범위

```
10 ~ 170
```

### 예시

```javascript
socket.emit("set_gripper", {
  gripper: 40
});
```

### 의미

| 값 | 상태 |
|---|---|
| 170 | 완전히 열림 |
| 90 | 중간 |
| 30 | 거의 닫힘 |

---

# 4.3 서보 토크 제어

### 이벤트 이름

```
set_torque
```

### 설명

모든 서보의 토크 ON / OFF 를 설정한다.

### 데이터 형식

```json
{
  "torque": value
}
```

### 값

| 값 | 의미 |
|---|---|
| 1 | 토크 ON |
| 0 | 토크 OFF |

### 예시

```javascript
socket.emit("set_torque", {
  torque: 0
});
```

### 동작 설명

토크가 OFF 상태이면 로봇팔을 **손으로 직접 움직일 수 있다.**

이때 서버는 서보 각도를 읽어서 FK 계산을 수행하므로  
**엔드이펙터 좌표도 실시간으로 업데이트된다.**

즉 **Teach Mode (수동 조작 기록)** 기능이 가능하다.

---

# 5. State 와 Command 차이

이 API는 **State / Command 구조**로 동작한다.

## State (서버 → 클라이언트)

```
robot_state
```

현재 로봇 상태를 알려주는 데이터이다.

포함 정보

- 엔드이펙터 좌표
- J1 ~ J6 관절 각도
- 그리퍼 개방 상태

예시

```
joints[5] = J6
```

이 값은 **현재 그리퍼가 얼마나 열려있는지** 나타낸다.

---

## Command (클라이언트 → 서버)

클라이언트가 로봇에게 동작을 지시하는 명령이다.

```
set_pos
set_gripper
set_torque
```

예시

```
set_gripper
```

그리퍼를 움직이라는 **명령**이다.

---

## 중요한 차이

```
robot_state.joints[5]
```

현재 그리퍼 상태 (State)

```
set_gripper
```

그리퍼를 움직이라는 명령 (Command)

따라서 J6 값이 `robot_state`에 포함되어 있더라도  
**그리퍼를 제어하려면 반드시 `set_gripper` 명령을 사용해야 한다.**

---

# 6. 사용 예시

## 로봇 이동

```javascript
socket.emit("set_pos", {
  pos: [0.18, 0.05, 0.12]
});
```

---

## 그리퍼 닫기

```javascript
socket.emit("set_gripper", {
  gripper: 30
});
```

---

## 토크 해제

```javascript
socket.emit("set_torque", {
  torque: 0
});
```

---

# 🦅 독수리 오형제 프로젝트

불법 주정차 문제 해결을 위한 **자율비행 드론 기반 차량 단속 시스템**

---

## 📅 프로젝트 기간
2024.03.04 ~ 2024.12.09 (약 9개월)

---
## 📌 프로젝트 소개

**독수리 오형제**는 자율비행 드론을 통해 불법주정차 차량을 감지하고,  
촬영 및 식별된 차량 정보를 데이터베이스와 클라우드에 자동 저장하여  
**웹과 앱을 통해 실시간으로 확인 가능한 서비스**입니다.

- 🚗 **불법주차 단속 자동화**: 자율 비행 중 불법주정차 차량을 탐지 및 촬영  
- 🧠 **YOLO를 이용한 객체 탐지**: 차량과 번호판을 AI 모델로 인식  
- 🔍 **번호판 확대 및 텍스트화**: 탐지된 번호판을 확대하고 OCR로 번호 인식  
- ☁️ **AWS 클라우드 저장소**: 차량 이미지는 클라우드에, 텍스트 정보는 DB에 저장  
- 🌐 **웹/앱에서 정보 확인**: 저장된 정보는 관리자 화면을 통해 즉시 확인 가능  
- 🛰 **픽스호크 + QGroundControl**: 센서 기반 자율비행 및 통합 제어 환경 구축  

---

## 🛠 기술 스택

| 분류 | 사용 기술 |
|------|-----------|
| 언어 | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) |
| 웹 | ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white) |
| 운영체제 | ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) |
| 모바일 | ![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white) |
| 데이터베이스 | ![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white) |
| 클라우드 | ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white) ![S3](https://img.shields.io/badge/S3-BD0C00?style=for-the-badge&logo=amazons3&logoColor=white) |
| 딥러닝 / AI | ![YOLOv8](https://img.shields.io/badge/YOLOv8-FF1493?style=for-the-badge&logo=opencv&logoColor=white) ![TorchVision](https://img.shields.io/badge/TorchVision-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white) ![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) ![Label Studio](https://img.shields.io/badge/Label%20Studio-FF6D00?style=for-the-badge&logo=data&logoColor=white) |
| 기타 | ![SSH Tunneling](https://img.shields.io/badge/SSH%20Tunneling-000000?style=for-the-badge&logo=gnu-bash&logoColor=white) |

---

## 👨‍💻 담당 역할

- 🛠 **Jetson (Ubuntu) 환경에서 YOLO 기반 객체 탐지 및 식별 수행**  
- 🔍 차량 번호판 탐지 → 확대 → 텍스트 인식 → 이미지/텍스트 저장 처리 구현  
- 🧪 YOLO 모델 학습 및 검증, 객체 인식 정확도 향상  
- ☁️ 인식된 정보를 MariaDB와 AWS에 연동하여 실시간 저장 구조 설계  

---
## 🖥 화면 구성

프로젝트의 주요 기능을 시각적으로 확인할 수 있는 화면입니다.  
클릭하면 원본 크기로 볼 수 있습니다.

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/5b3e1476-e28d-4d61-8227-885596153aa9" width="300px" alt="화면1"/><br/>
      <sub>Jetson nano 환경 설정</sub>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/6b5ba17d-cc95-40b4-9f4f-716a11841425" width="300px" alt="화면2"/><br/>
      <sub>🔍 번호판 확대 및 탐지</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/504180c1-25b0-4881-aefc-c57e2496c67a" width="300px" alt="화면3"/><br/>
      <sub>학습 모델 평가 지표</sub>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/13c982db-56c3-4309-a96c-711def833e26" width="300px" alt="화면4"/><br/>
      <sub>☁️ AWS S3 업로드 과정</sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <img src="https://github.com/user-attachments/assets/36328d23-6f45-41d2-b1c5-9e2ef6700a0b" width="600px" alt="화면5"/><br/>
      <sub>🌐 웹 대시보드에서 확인 과정 및 확인</sub>
    </td>
  </tr>
</table>

---
> 📁 프로젝트 전체는 `불법주차 단속 자동화`라는 실질적인 사회 문제 해결을 목표로,  
> 임베디드 시스템과 AI 모델, 클라우드 인프라를 유기적으로 연결한 **엔드 투 엔드 통합 시스템**입니다.

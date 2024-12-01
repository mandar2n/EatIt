# EatIt - 바쁜 삶 속에서 건강한 한 끼 챙기기
![image](https://github.com/user-attachments/assets/4d5a17a3-bec1-426e-a760-6b546ed7f533)

## 기능
1. 사용자 위치 기준 반경 1km 이내의 편의점 찾기
2. 키워드, 가격대, 편의점 종류 입력받아 AI로부터 한 끼 조합 추천받기
3. 지난 조합 조회하기
   

## 프로젝트 실행 방법

1. **Conda 환경 생성 및 의존성 설치**

2. **가상환경 활성화**:
   ```bash
   conda activate dbd

3. **프로젝트 실행**:
   ```bash
   uvicorn back.src.main:app --reload

4. **로컬로 접속**

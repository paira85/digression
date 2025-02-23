# 기본 이미지로 Python 3.9을 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 요구사항 파일을 컨테이너에 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install -r requirements.txt

# 애플리케이션 파일을 컨테이너에 복사
COPY . .

# 컨테이너가 시작될 때 실행할 명령어
CMD ["python", "app.py"]

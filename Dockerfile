FROM python:3.7.7-alpine3.11

# ==============================================================================
# 타임존 설정
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone

ENV PYTHONUNBUFFERED=0

# ==============================================================================
# 파일 복사
RUN mkdir -p /src/book_rental_manager
ADD book_rental_manager /src/book_rental_manager
ADD setup.py /src
WORKDIR /src

# ==============================================================================
# 설치
RUN pip install -r book_rental_manager/requirements.txt
RUN python setup.py install

# ==============================================================================
# 설치파일 정리
WORKDIR /root
RUN rm -rf /src

EXPOSE 5000
VOLUME ["/root"]
ENTRYPOINT ["python" , "-m", "book_rental_manager"]


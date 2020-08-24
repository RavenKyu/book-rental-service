# book-rental-manager-api

## 사용법
### 설치

### 실행
```bash

```
```bash
usage: book-rental-manager-api [-h] {init,server} ...

positional arguments:
  {init,server}
    init         Initialize database
    server       Run api server

optional arguments:
  -h, --help     show this help message and exit
```
### initialize db
```bash
# 초기화 명령 도움말 보기
python -m book_rental_manager init -h

# 디비 내용 초기화, Customer, Book, Rental 더미 데이터 삽입
python -m book_rental_manager init -dmbr
```

### server start
Execute it as a api server. 
```bash
python -m book_rental_manager server 
```

## API
### Customer
#### 전체 회원 정보 가져오기
```bash
curl --request GET 'http://localhost:5000/customers' 

[{"id": 2, "name": "\uc784\ub355\uaddc", "phone": "010-9508-0875"}, {"id": 3, "name": "\uae40\ub355\uaddc", "phone": "010-8857-5121"}]
```
#### 회원 정보 검색하여 가져오기
```bash
curl --request GET 'http://localhost:5000/customers?customer_id=1' 

```

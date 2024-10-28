# FastAPI

> Learn FastAPI
> 처음 시작하는 FastAPI(O'REILLY) - <https://www.hanbit.co.kr/store/books/look.php?p_code=B4964299316>

port: 8000


## 동시성

> 서비스가 성장하고 연결량이 빠르게 증가할 때는 효율성과 확장성이 중요하다.
> 이를 위해 다음 두 가지 항목이 줄어야 한다.

1. 지연시간(latency) - 사전 대기 시간
2. 처리량(throughput) - 서비스와 호출자 간의 초당 바이트 수

일반적으로 파이선에서의 실행 방식은 코드에 지정된 순서에 따라 한 번에 한 가지씩 실행하는 '동기식(synchronous)'임
비동기 처리는 만능이 아니다. 이벤트 루프에서 CPU 집약적인 작업을 너무 많이 수행하지 않도록 주의해야 함. (모든 작업의 속도가 저하될 수 있음)

## Starlette(ASGI)

> Starlette은 경량 ASGI 프레임워크/툴킷으로, 파이썬 비동기 웹 서비스를 구축하는 데 이상적임
> Django와 Flask는 전통적인 동기식 WSGI 표준을 기반으로 동작함



# rdt protocol 기능 구현 및 성능평가

## 구현 대상
- rdt 3.0(stop-and-wait)
- go-back-N
- selective repeat

## 기능 점검 방법
- UDP socket을 이용하여 sender와 receiver side rdt 구현
  - 목적지 호스트의 IP 주소로 loopback 주소인 127.0.0.1 사용
- 가정
  - 하나의 sender와 하나의 receiver
  - sender는 항상 전송할 데이터가 있음
  - sequence number는 0부터 1씩 순차적으로 증가
  - segment size와 transmission rate은 고려하지 않음
- 프로토콜 설정
  - Go-back-N sending window size = 50
  - Selective Repeat sending window size = 50, receiving window size = 50
  - 전송 오류(pe) = 1/1000
  - transmission delay와 propagation delay를 포함한 RTT (r) = 10ms

## 실행 방법
각 파일 안에는 sender와 receiver 코드가 따로 구분되어 있는데, python console에서 receiver 코드를 실행해주어 socket을 열어준 후 sender 코드를 실행해준다. 

아래는 python console에서 각 파일을 실행했을 때 sender 사이드에서 출력되는 화면이다.

### rdt 3.0
![rdtsender](https://user-images.githubusercontent.com/49015100/101871562-229a4b80-3bc7-11eb-908f-f033a86ba982.png)


### go-back-N
![gbnsender](https://user-images.githubusercontent.com/49015100/101871577-2a59f000-3bc7-11eb-904c-390731ab8974.png)
![gbnsender2](https://user-images.githubusercontent.com/49015100/101871584-2ded7700-3bc7-11eb-8b63-ddd3f07ae7fc.png)


### selective repeat
![SRsender](https://user-images.githubusercontent.com/49015100/101871596-33e35800-3bc7-11eb-8224-f1a21154b55e.png)
![SRsender2](https://user-images.githubusercontent.com/49015100/101871607-39d93900-3bc7-11eb-862f-3f0e2b2e8142.png)

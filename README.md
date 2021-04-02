### MASK-RCNN 을 통한 고막 검출 그리고 병증 진단 프로그램 웹서비스
### 작성자 : 신지환(순천향대학교 컴퓨터공학과 유비쿼터스 연구실 &  ICT 융합재활공학연구센터)
### 수정날 : 21.01.25.
### jihwan9675@gmail.com
 - 환경 : Tensorflow 2.3.1
 - server.py로 웹서버를 구동시킵니다.
 - 로컬에서 사용시 AWS DynamoDB 환경변수 설정
  - aws_access_key_id : your aws id key
  - aws_secret_access_key : your secret key
 - Dockerfile에도 AWS(DynamoDB)환경변수 추가 해야합니다.
 - Weight 파일은 의료데이터로 문제발생요지가 있어 공유하지 못합니다.

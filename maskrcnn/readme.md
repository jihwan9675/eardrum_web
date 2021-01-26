### MASK-RCNN 을 통한 고막 검출 그리고 병증 진단 프로그램 웹서비스
### 작성자 : 신지환(순천향대학교 컴퓨터공학과 유비쿼터스 연구실)
### 수정날 : 21.01.25.

현 디렉토리는 Socket 프로그램이다. Web Server(Flask)에서 요청이 오면 MaskRCNN 과 분류 코드를 실행시켜 패킷화하여 정보를 전달시켜준다.
현 디렉토리에 /Weights/efficientNetB0.h5, mask_rcnn_eardrum_0043.h5 두가지를 넣어줘야한다. 법적문제가 발생할 수 있어서 ignore 시켜놨다.
자세한건 deeplearningServer.py 주석으로 설명하였다.

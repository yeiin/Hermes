# Hermes

<div align = center>
    <img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=Hermes&fontSize=90" />
</div>

## About The Project
> Parenting Multitask Helper with Open CV

> 디렉토리 구조 --  내가 할 거임.

<img src="https://img.shields.io/badge/Android%20Studio-3DDC84?style=flat&logo=Android%20Studio&logoColor=white"/>
<img src="https://img.shields.io/badge/Java-007396?style=flat&logo=Java&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=OpenCV&logoColor=white"/>
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=TensorFlow&logoColor=white"/>
<img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=Raspberry%20Pi&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white"/>


## Environment
 각자 환경 넣기.
 os compiler cpu ram
</br> Choi yunseo </br>
os : Mac os</br>
code editor : VScode with ssh connection to pi</br>
cpu : Apple M1</br>
ram : 8GB</br></br>

## Prerequisite
필요한 package 적기
</br></br> Choi Yunseo : camera detecting, realtime status judgement, 3D print </br>
camera detecting : OpenCV, MediaPipe etc.
</br>

## Files
각 파일들이 어떻게 돌아가는 지 간단 정리
간단한 사용 방법 및 예제
프로젝트 경과
</br>Camera & Baby</br>![image](https://user-images.githubusercontent.com/52804557/200515596-727b8822-577f-4133-bbe7-aca37f5627e2.png)
![image](https://user-images.githubusercontent.com/52804557/200515629-8352455f-b82d-4c53-a246-2417f44739b3.png)
![image](https://user-images.githubusercontent.com/52804557/200515672-f97536ac-747a-4947-abb8-25a3fdef4868.png)
![image](https://user-images.githubusercontent.com/52804557/200515693-9d824205-b5d9-4606-8e16-16cbb2709ac3.png)
</br></br>

전체 플로우는 내가 할게 + diagram

## Contribute
각자 자신 연결
</br>Choi Yunseo : camera detecting, realtime status judgement, 3D print </br>
</br>

## Usage
각 코드 들을 어떻게 실행해야하는지
</br> raspi/camera.py : facial detecting with picamera</br>'python3 camera.py'
</br> raspi/baby.py : realtime baby's status judgement linked with camera.py</br>'python3 main.py'

## Reference
참고 내용

1. Camera detecting (camera.py)</br>
(1) MediaPipe facemesh</br> https://google.github.io/mediapipe/solutions/face_mesh.html</br>
(2) openCV with haarcascade ( less accurate than (1) )</br>
2. 3D model printing</br>
 [ Cubicon style-plus / Suwon Makerspace ]</br>
(1) Raspberry Pi 4B TURBO case With Integrated Camera Module</br>
https://www.youtube.com/watch?v=kXgKs1Zv43U</br>
https://www.thingiverse.com/thing:4912025</br>
(2) LED lamp</br>
https://www.thingiverse.com/thing:1531729

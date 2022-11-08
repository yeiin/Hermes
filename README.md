<div align = center>
    <img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=Hermes&fontSize=90" />
</div>

# About The Project
> Parenting Multitask Helper with Open CV

<div>
    <img src="https://img.shields.io/badge/Android%20Studio-3DDC84?style=flat&logo=Android%20Studio&logoColor=white"/>
    <img src="https://img.shields.io/badge/Java-007396?style=flat&logo=Java&logoColor=white" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>
    <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=OpenCV&logoColor=white"/>
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=TensorFlow&logoColor=white"/>
    <img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=Raspberry%20Pi&logoColor=white"/>
    <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white"/>
    <img src="![readme_app_1](https://user-images.githubusercontent.com/100847440/200597432-03ac2e1d-6ccd-47c4-9786-a2e4edf24b2b.jpeg)"/>
<img src="![readme_app_2](https://user-images.githubusercontent.com/100847440/200597460-9160d898-30cd-42e7-93db-ceedfff15560.jpeg)"/>
</div>

# Directory
```
.
├── HERMES_APPLICATION
│   ├── app
│   │   ├── build.gradle
│   │   ├── libs
│   │   ├── proguard-rules.pro
│   │   └── src
│   │       ├── androidTest
│   │       │   └── java
│   │       │       └── com
│   │       │           └── example
│   │       │               └── hermes_application
│   │       │                   └── ExampleInstrumentedTest.java
│   │       ├── main
│   │       │   ├── AndroidManifest.xml
│   │       │   ├── java
│   │       │   │   └── com
│   │       │   │       └── example
│   │       │   │           └── hermes_application
│   │       │   │               ├── BabyVideoActivity.java
│   │       │   │               ├── IntroActivity.java
│   │       │   │               ├── MainActivity.java
│   │       │   │               └── MusicActivity.java
│   │       │   └── res
│   │       │       ├── drawable
│   │       │       │   ├── ex1.png
│   │       │       │   └── ic_launcher_background.xml
│   │       │       ├── drawable-v24
│   │       │       │   └── ic_launcher_foreground.xml
│   │       │       ├── layout
│   │       │       │   ├── activity_baby_video.xml
│   │       │       │   ├── activity_intro.xml
│   │       │       │   ├── activity_main.xml
│   │       │       │   └── activity_music.xml
│   │       │       ├── mipmap-anydpi-v26
│   │       │       │   ├── ic_launcher_round.xml
│   │       │       │   └── ic_launcher.xml
│   │       │       ├── mipmap-hdpi
│   │       │       │   ├── ic_launcher_round.webp
│   │       │       │   └── ic_launcher.webp
│   │       │       ├── mipmap-mdpi
│   │       │       │   ├── ic_launcher_round.webp
│   │       │       │   └── ic_launcher.webp
│   │       │       ├── mipmap-xhdpi
│   │       │       │   ├── ic_launcher_round.webp
│   │       │       │   └── ic_launcher.webp
│   │       │       ├── mipmap-xxhdpi
│   │       │       │   ├── ic_launcher_round.webp
│   │       │       │   └── ic_launcher.webp
│   │       │       ├── mipmap-xxxhdpi
│   │       │       │   ├── ic_launcher_round.webp
│   │       │       │   └── ic_launcher.webp
│   │       │       ├── values
│   │       │       │   ├── colors.xml
│   │       │       │   ├── strings.xml
│   │       │       │   └── themes.xml
│   │       │       ├── values-night
│   │       │       │   └── themes.xml
│   │       │       └── xml
│   │       │           ├── backup_rules.xml
│   │       │           └── data_extraction_rules.xml
│   │       └── test
│   │           └── java
│   │               └── com
│   │                   └── example
│   │                       └── hermes_application
│   │                           └── ExampleUnitTest.java
│   ├── build.gradle
│   ├── gradle
│   │   └── wrapper
│   │       ├── gradle-wrapper.jar
│   │       └── gradle-wrapper.properties
│   ├── gradle.properties
│   ├── gradlew
│   ├── gradlew.bat
│   └── settings.gradle
├── raspi
│   ├── asset
│   │   ├── music_a.mp3
│   │   └── music_b.mp3
│   ├── baby.py
│   ├── camera.py
│   ├── constant.py
│   ├── led.py
│   ├── main.py
│   ├── mobile.py
│   ├── music.py
│   ├── network.py
│   ├── processor
│   │   ├── face_detector.py
│   │   ├── __init__.py
│   │   ├── model
│   │   │   └── haarcascades
│   │   │       ├── haarcascade_eye.xml
│   │   │       └── haarcascade_frontalface_default.xml
│   │   ├── __pycache__
│   │   │   ├── face_detector.cpython-37.pyc
│   │   │   ├── __init__.cpython-37.pyc
│   │   │   └── simple_streamer.cpython-37.pyc
│   │   └── simple_streamer.py
│   ├── __pycache__
│   │   ├── audio.cpython-37.pyc
│   │   ├── baby.cpython-37.pyc
│   │   ├── camera.cpython-37.pyc
│   │   ├── constant.cpython-37.pyc
│   │   ├── led.cpython-37.pyc
│   │   ├── led.cpython-39.pyc
│   │   ├── mobile.cpython-37.pyc
│   │   ├── motor.cpython-37.pyc
│   │   ├── music.cpython-37.pyc
│   │   ├── network.cpython-37.pyc
│   │   ├── socket.cpython-37.pyc
│   │   └── utils.cpython-37.pyc
│   ├── templates
│   │   └── index.html
│   ├── utils.py
│   └── videostream.py
├── README.md
└── tree.txt

42 directories, 76 files

```


# Environment

## Raspberry pi 4
code editor : VScode with ssh connection to pi</br>
model name : Raspberry Pi 4 Model B Rev 1.5 </br>
CPU: ARM Cortex-A72 1.5GHz</br>
RAM: 2GB </br>
Linux version 5.15.76-v7l+ (dom@buildbot) (arm-linux-gnueabihf-gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu1) 8.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #1597 SMP Fri Nov 4 12:14:58 GMT 2022 </br>


## Android
#### build.gradle
'com.android.application': version '7.3.0' </br>
'com.android.library' : version '7.3.0' </br>
</br>
Compile SDK : 32</br>
min SDK : 21</br>
target SDK : 32</br>
Java Version : VERSION_1_8 </br>
</br>
xml version : 1.0 </br>
encoding : utf-8 </br>

 
 
# Dependency
### Raspberry Pi
> Open CV
>> OpenCV :  
>> MediaPipe 
>> etc.

### Android
> Manifest
>>INTERNET Permission
>>ACCESS_NETWORK_STATE Permission

### Demo
> 3D pring

# Project

### Facial detection
#### camera.py & baby.py
Calculate the eye ratio with eye's width and height.</br>
|eye ratio||
|-----|-----|
|Close|>=4.5|
|Open|else|

### Baby Status Judgement
#### baby.py
camera.py put baby's state in queue.</br>
|Open|0|
|----|----|
|Close|1|

</br> count rate = Open/Queue's size</br>

|count rate|----|
|----------|----|
|Wake|>=0.8|
|ASLEEP|>=0.4 and Init stat = Wake|
|AWAKE| >=0.4 and Init stat = Sleep|
|Sleep|else|
|None|No detect above threshold|

</br>

> Init stat only can be Wake/Sleep
>> If baby is wake, blink count decreasing, it goes Asleep.</br>
>> If baby is sleep, blink ocunt increasing, it goes Awake.</br>
</br>

#### Final result using for GPIO
> STATS
>> Wake, Awake, Asleep, Sleep

### Andriod App
|State Notification and Control|----------------------|
|------------------------------|----------------------|
|:State of Baby|:Asleep or Awake or Sleep or Wake or Detect X|
|:Mobile|:ON or OFF|
|:LED|:ON or OFF|
|:Music|:Play or Stop and choose music|
|:Illuminance|:Level 0 - 10|
|:Mode|:Auto or User|

</br>

> If click State of baby, you can watch real-time video

</br>


### Diagram
<!-- 전체 플로우는 내가 할게 + diagram -->

# Contribute
</br>Choi Yunseo : camera detecting, realtime status judgement, 3D print </br>
</br>

# Usage

</br> raspi/camera.py : facial detecting with picamera using Mediapipe 
``` python3 camera.py``` </br>
</br> raspi/baby.py : realtime baby's status judgement linked with camera.py and Gpio operation </br>
``` python3 main.py ``` </br>

# Reference
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


#application 전제내용 ///참고 후 이 문장 삭제 부탁드려용
![readme_app_1](https://user-images.githubusercontent.com/100847440/200597432-03ac2e1d-6ccd-47c4-9786-a2e4edf24b2b.jpeg)
![readme_app_2](https://user-images.githubusercontent.com/100847440/200597460-9160d898-30cd-42e7-93db-ceedfff15560.jpeg)"

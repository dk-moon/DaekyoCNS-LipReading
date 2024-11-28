# Lip Reading using AUTO-AVSR

## Requirment

- 환경구성

    ```bash
    conda create -y -n {env_nm} python=3.9
    conda activate {env_nm}
    ```

- Python 패키지 설치

    ```bash
    pip install ffmpeg-python pydub
    ```

- FFMPEG 설치

    - macOS

        ```bash
        brew install ffmpeg
        ```

    - Ubuntu/Linux

        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```

    - Windows

        - https://ffmpeg.org/download.html 에서 설치

## Data

- AI Hub : 립리딩(입모양) 음성인식 데이터

## Preprocessing

1. Load raw data

2. Extract video section that matches the sentence information of the label
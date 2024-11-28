import os  # 파일 및 디렉토리 경로 작업을 위한 모듈
import hydra  # Hydra를 사용하여 구성 파일을 관리
import logging  # 로깅을 설정하고 작업 진행 상황 기록
from preprocessing.raw_data_preprocess import run_preprocess  # 전처리 실행 함수 가져오기

def raw_data_preprocessing(cfg):
    '''
    Step 1. Raw Data Preprocessing
    - Extract video section that matches the sentence information of the label
    '''
    logging.info("Step 1: Starting raw data preprocessing...")

    # 필요한 출력 디렉토리가 없으면 생성
    ensure_directories_exist([
        cfg.preprocess.label_folder,  # 라벨 파일 저장 디렉토리
        cfg.preprocess.audio_folder,  # 오디오 파일 저장 디렉토리
        cfg.preprocess.audiovisual_folder,  # 비디오 파일 저장 디렉토리
    ])

    # 전처리 실행
    run_preprocess(
        json_folder=cfg.preprocess.json_folder,
        wav_folder=cfg.preprocess.wav_folder,
        mp4_folder=cfg.preprocess.mp4_folder,
        label_folder=cfg.preprocess.label_folder,
        audio_folder=cfg.preprocess.audio_folder,
        audiovisual_folder=cfg.preprocess.audiovisual_folder,
    )
    logging.info("Step 1: Raw data preprocessing completed.")

def data_preprocessing(cfg):
    '''
    Step 2. Data Preprocessing
    - Audio-Visual : 
    - Audio : 
    - Label : 
    '''
    logging.info("Step 2: Starting data preprocessing...")
    # 추가 데이터 전처리 로직 구현 필요
    # 예: preprocess_data(cfg)
    logging.info("Step 2: Data preprocessing completed.")


# Hydra 초기화 및 구성 파일 로드
@hydra.main(version_base="0.1", config_path="config", config_name="preprocess_config")
def main(cfg):
    # 로그 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("log/main.log"),  # 로그를 파일에 저장
            logging.StreamHandler(),  # 콘솔에 로그 출력
        ],
    )

    # Step 1: Raw Data Preprocessing
    raw_data_preprocessing(cfg)
    
    # Step 2: Data Preprocessing
    data_preprocessing(cfg)

'''
utilities
'''
def ensure_directories_exist(directories):
    """
    주어진 디렉토리 리스트의 경로가 없으면 생성.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)  # 디렉토리가 없으면 생성, 이미 있으면 무시


if __name__ == "__main__":
    main()
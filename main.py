import os  # 파일 및 디렉토리 경로 작업을 위한 모듈
from hydra import initialize, compose  # Hydra를 사용하여 구성 파일을 초기화하고 로드
from preprocessing.raw_data_preprocess import run_preprocess  # 전처리 실행 함수 가져오기

def ensure_directories_exist(directories):
    """
    주어진 디렉토리 리스트의 경로가 없으면 생성.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)  # 디렉토리가 없으면 생성, 이미 있으면 무시

if __name__ == "__main__":
    # Hydra 초기화 및 구성 파일 로드
    # config 폴더를 기준으로 구성 파일 초기화
    with initialize(config_path="config", version_base=None):  # config 경로 설정 및 Hydra 초기화
        config = compose(config_name="preprocess_config")  # preprocess_config.yaml 파일 로드
    
    '''
    Raw Data Preprocessing
    Extract video section that matches the sentence information of the label
    '''
    
    # 필요한 출력 디렉토리가 없으면 생성
    ensure_directories_exist([
        config.preprocess.label_folder,  # 라벨 파일 저장 디렉토리
        config.preprocess.audio_folder,  # 오디오 파일 저장 디렉토리
        config.preprocess.audiovisual_folder  # 비디오 파일 저장 디렉토리
    ])
    
    # 전처리 실행
    run_preprocess(
        json_folder=config.preprocess.json_folder,  # JSON 파일 경로
        wav_folder=config.preprocess.wav_folder,  # WAV 파일 경로
        mp4_folder=config.preprocess.mp4_folder,  # MP4 파일 경로
        label_folder=config.preprocess.label_folder,  # 라벨 파일 저장 경로
        audio_folder=config.preprocess.audio_folder,  # 오디오 파일 저장 경로
        audiovisual_folder=config.preprocess.audiovisual_folder  # 비디오 파일 저장 경로
    )
    
    '''
    Data Preprocessing
    
    '''
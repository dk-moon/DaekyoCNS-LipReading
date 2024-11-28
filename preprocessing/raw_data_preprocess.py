import os
import json
import asyncio
import argparse
import ffmpeg
import logging
from pydub import AudioSegment

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log/preprocess.log"),  # 로그를 파일에 저장
        logging.StreamHandler()  # 콘솔에 로그 출력
    ]
)

async def process_json(json_file, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder):
    """
    JSON 파일을 처리하여 텍스트 파일 생성, 오디오 및 비디오 파일 추출.
    """
    try:
        logging.info(f"Processing JSON file: {json_file}")
        with open(json_file, "r") as f:
            data = json.load(f)
        
        # JSON 구조 확인 및 처리
        if isinstance(data, list):
            for item in data:
                await process_item(item, json_file, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder)
        elif isinstance(data, dict):
            await process_item(data, json_file, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder)
        else:
            logging.error(f"Unsupported JSON structure in file: {json_file}")
    except Exception as e:
        logging.error(f"Error processing JSON file {json_file}: {e}")


async def process_item(data, json_file, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder):
    """
    JSON의 개별 데이터를 처리.
    """
    try:
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        for sentence in data.get("Sentence_info", []):
            sentence_id = sentence.get("ID")
            sentence_text = sentence.get("sentence_text")
            start_time = float(sentence.get("start_time", 0))
            end_time = float(sentence.get("end_time", 0))

            if not sentence_id or not sentence_text:
                logging.warning(f"Invalid sentence data in file {json_file}: {sentence}")
                continue

            # 1. 텍스트 파일 생성
            label_filename = os.path.join(label_folder, f"{base_name}_{sentence_id}.label")
            with open(label_filename, "w") as label_file:
                label_file.write(sentence_text)
            logging.info(f"Saved label file: {label_filename}")

            # 2. 오디오 파일 처리
            wav_file_path = os.path.join(wav_folder, f"{base_name}.wav")
            if os.path.exists(wav_file_path):
                audio = AudioSegment.from_wav(wav_file_path)
                segment = audio[start_time * 1000:end_time * 1000]
                audio_output_path = os.path.join(audio_folder, f"{base_name}_{sentence_id}.wav")
                segment.export(audio_output_path, format="wav")
                logging.info(f"Saved audio file: {audio_output_path}")
            else:
                logging.warning(f"WAV file not found: {wav_file_path}")

            # 3. 비디오 파일 처리
            mp4_file_path = os.path.join(mp4_folder, f"{base_name}.mp4")
            if os.path.exists(mp4_file_path):
                video_output_path = os.path.join(audiovisual_folder, f"{base_name}_{sentence_id}.mp4")
                await extract_video_segment(mp4_file_path, start_time, end_time, video_output_path)
                logging.info(f"Saved video file: {video_output_path}")
            else:
                logging.warning(f"MP4 file not found: {mp4_file_path}")
    except KeyError as e:
        logging.error(f"Missing key in sentence data: {e}")
    except Exception as e:
        logging.error(f"Error processing sentence in file {json_file}: {e}")


async def extract_video_segment(input_file, start_time, end_time, output_file):
    """
    FFmpeg를 사용하여 비디오의 특정 구간을 추출.
    """
    try:
        (
            ffmpeg
            .input(input_file, ss=start_time, to=end_time)
            .output(output_file, vcodec="libx264", acodec="aac", strict="experimental")
            .run(quiet=True, overwrite_output=True)
        )
        logging.info(f"Extracted video segment: {output_file}")
    except ffmpeg.Error as e:
        logging.error(f"FFmpeg error while processing {input_file}: {e}")


async def main(json_folder, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder):
    """
    JSON 파일을 비동기로 처리.
    """
    tasks = []
    for json_file in os.listdir(json_folder):
        if json_file.endswith(".json"):
            json_file_path = os.path.join(json_folder, json_file)
            tasks.append(process_json(json_file_path, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder))
    
    await asyncio.gather(*tasks)


def run_preprocess(json_folder, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder):
    """
    외부 호출을 위한 진입점 함수.
    """
    asyncio.run(main(json_folder, wav_folder, mp4_folder, label_folder, audio_folder, audiovisual_folder))
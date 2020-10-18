"""Record audio and get text from AWS transcribe"""
import os
import csv
import pandas as pd
import argparse
import glob
from tqdm import tqdm
import time
import json
import urllib.request
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "audios-bbva"

def check_bucket(BUCKET_NAME):
    """Check bucket exist, if not it's created"""
    print("* Checking S3 bucket")
    s3 = boto3.resource("s3")
    bucket_names = [bucket.name for bucket in s3.buckets.all()]
    if BUCKET_NAME not in bucket_names:
        s3.create_bucket(Bucket=BUCKET_NAME)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""

    # If S3 object_name was not specified, use file_name
    print("* Uploading audio to S3")
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True


def transcribe(job_name, job_uri, languaje="es-ES"):
    """Create transcribe job using audio from S3"""
    print("* Creating transcribe job")
    transcribe = boto3.client("transcribe")
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": job_uri},
        MediaFormat="wav",
        LanguageCode=languaje,
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
            "COMPLETED",
            "FAILED",
        ]:
            break
        print("Not ready yet...")
        time.sleep(5)
    return status


def get_text_from_json(json_url, wav_file, folder_path):
    """Read json from URL containing the transcribed text"""
    file_name = os.path.join(folder_path, os.path.basename(wav_file))
    file_name = file_name.replace("wav", "json")
    print("* Getting final text\n")
    with urllib.request.urlopen(json_url) as url:
        data = json.loads(url.read().decode(), encoding='utf-8')
        text = data["results"]["transcripts"][0]["transcript"]
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
    return text

def get_audios_list(folder_path):
    list_audios = [x for x in glob.glob(f"{folder_path}/*.wav")]
    list_jsons = [x for x in glob.glob(f"{folder_path}/*.json")]
    list_audios = [x for x in list_audios if x+".json" not in list_jsons]
    #print(list_audios)
    return list_audios

def get_text_from_files(list_audios, folder_path):
    cvs_file = f'{folder_path}/output.csv'
    df = []
    if os.path.isfile(cvs_file):
        try:
            df = pd.read_csv(cvs_file)
        except:
            print("EMPTY CSV")
    list_text = []
    with open(cvs_file, mode='a') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for audio in tqdm(list_audios, total=len(list_audios)):
            current_text = process_audio(audio, folder_path)
            list_text.append(current_text)
            csv_writer.writerow([audio, current_text])
    return list_text

def process_audio(wav_file, folder_path):
    check_bucket(BUCKET_NAME)
    upload_file(wav_file, BUCKET_NAME)
    wav_name = os.path.basename(wav_file)
    audio_url = f"s3://{BUCKET_NAME}/{wav_name}"
    wav_name = wav_name.replace(" ", "_")
    response = transcribe(wav_name, audio_url)
    json_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    text = get_text_from_json(json_url, wav_file, folder_path)
    return text

def main():
    parser = argparse.ArgumentParser(
        description="Convierte todos los audios de una carpeta a texto"
    )
    parser.add_argument(
        "--folder", help="Carpeta con los audios", required=True,
    )
    
    args = parser.parse_args()
    folder_path = args.folder
    list_audios = get_audios_list(folder_path)
    list_text = get_text_from_files(list_audios, folder_path)
    print("DONE")


if __name__ == "__main__":
    main()

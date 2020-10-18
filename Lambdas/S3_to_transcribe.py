import os
import json
import boto3
import time
import os
from urllib.request import urlopen

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        s3_uri = create_uri(bucket_name, file_name)
        job_name = os.path.basename(file_name).replace(" ", "_")

        print(os.path.splitext(file_name)[0])

        transcribe.start_transcription_job(TranscriptionJobName = job_name,
                                           Media = {'MediaFileUri': s3_uri},
                                           MediaFormat =  'wav',
                                           LanguageCode = "es-ES",
                                           OutputBucketName = "transcribe-json"
                                           )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
                break
            print("Transcription in progress")
            time.sleep(5)

        s3.put_object(Bucket = bucket_name, Key="output/{}.json".format(job_name), Body=load_)
    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job created!')
    }

def create_uri(bucket_name, file_name):
    return "s3://"+bucket_name+"/"+file_name

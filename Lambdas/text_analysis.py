import os
from botocore.vendored import requests
import json
import boto3
from urllib.request import urlopen

s3 = boto3.resource("s3")
#URL = "http://3.80.26.102/predict" old
URL = "http://54.172.146.52/predict"

def lambda_handler(event, context):
    if event:
        file_obj = event["Records"][0]
        bucket_name = file_obj['s3']['bucket']['name']
        file_name = file_obj['s3']['object']['key']
        print(bucket_name)
        print(file_name)
        
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        texto = json_content["results"]["transcripts"][0]["transcript"]
        
        values = {"text": texto}
        response = requests.post(URL, json=values)
        data = response.json()
        #print(data)
        data["Nombre Archivo"] = file_name.split(".")[0]
    
        file_name = "data2.js"
        lambda_path = "/tmp/" + file_name
        #s3_path = "jarvis.com/" + file_name
        
        content_object_js = s3.Object("jarvis.com", file_name)
        file_content = content_object_js.get()['Body'].read().decode('utf-8')
        temp_line = file_content.split("[")[1]
        
        with open(lambda_path, 'w+') as file:
            file.write("var myData = [\n")
            file.write(json.dumps(data)+",\n")
            file.write(temp_line)
            file.close()
        
        s3_client = boto3.client("s3")
        s3_client.upload_file(lambda_path, "jarvis.com", file_name)
    return {
        'statusCode': 200,
        'body': json.dumps('Text')
    }

def create_uri(bucket_name, file_name):
    return "s3://"+bucket_name+"/"+file_name
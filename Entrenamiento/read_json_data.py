import json
import glob

folder_path = "audios"
list_jsons = [x for x in glob.glob(f"{folder_path}/*.json")]
list_audios = [x for x in glob.glob(f"{folder_path}/*.wav")]

list_jsons = sorted(list_jsons, key=lambda x: int(x.split(".")[0].split(" ")[1]))
list_audios = sorted(list_audios, key=lambda x: int(x.split(".")[0].split(" ")[1]))

error = False
if len(list_jsons) != len(list_audios):
    print("ERROR")

text_file = f'{folder_path}/output_text.txt'

print(len(list_jsons))

with open(text_file, mode='w', encoding='utf-8') as output_file:
    for audio_file, json_file in zip(list_audios, list_jsons):
        with open(json_file, encoding='utf-8') as json_data:
            print(audio_file, json_file)
            data = json.load(json_data)
            text = data['results']['transcripts'][0]['transcript']
            output_file.write(f"{audio_file} : {text}\n")
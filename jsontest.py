import json   

with open(r"C:\Users\binho\Downloads\Chihlee Rober\CertAnser\campaign-manager-certification-answers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    for i in data:
        print(i[0])
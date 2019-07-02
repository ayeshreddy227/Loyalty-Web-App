import base64
import os
from random import randint
BASE_PATH = "/"

def uploadfiletos3(data,filename):
    decoded = base64.b64decode(data)
    tempfilename, file_extension = os.path.splitext(filename)
    tempfilename = tempfilename + str(randint(0, 100000)) + str(file_extension)
    tempfilename = BASE_PATH + os.path.sep + tempfilename
    with open(tempfilename, 'wb') as f:
        f.write(decoded)
    system_output = os.popen(
        "echo a | sudo -S s3cmd put --acl-public " + tempfilename + " s3://botmantexttospeech/" + filename).readlines()
    if os.path.exists(tempfilename):
        os.remove(tempfilename)
    if len(system_output) == 5 and "Public URL of the object is: " in system_output[4]:
        url = system_output[4].replace("Public URL of the object is: ", "")
        return {"url": url.strip()}
    else:
        return {"error": True, "message": "error uploading file to s3"}


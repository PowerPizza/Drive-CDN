from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials

gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("test/drive_cradentials.json", "https://www.googleapis.com/auth/drive")

gdrive = GoogleDrive(gauth)
print("drive connected")

# file1 = gdrive.CreateFile({"title": "file1.txt", "mimeType": "text/javascript"})
# file1.SetContentString("console.log('Hello World')")
# file1.Upload()
# file1.InsertPermission({
#     "type": "anyone",
#     "value": "anyone",
#     "role": "reader"
# })

files = gdrive.ListFile({"q": "'root' in parents and trashed=false"}).GetList()
# for itm in files:
#     file_ = gdrive.CreateFile({"id": itm["id"]})
#     file_.Delete()
for itm in files:
    if itm["title"] == "file1.txt":
        for itm2 in itm:
            print(itm2, ":", files[0][itm2])

# for itm in files[0]:
#     if itm["title"] == "file1.txt":
#         print(itm, ":", files[0][itm])
print(files[0])
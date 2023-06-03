import uuid, os

class GdriveHelper:
    drive_obj = None
    def __init__(self, gdrive_obj):
        self.drive_obj = gdrive_obj

    def list_files_id_title(self, parent_id="root"):
        to_ret = {}  # format = FILE_ID : FILE_NAME
        for itm in self.drive_obj.ListFile({"q": f"'{parent_id}' in parents and trashed=false"}).GetList():
            to_ret[itm["id"]] = itm["title"]
        return to_ret

    def find_id_by_name(self, media_name, parent_id="root"):
        lst = self.list_files_id_title(parent_id)
        return list(lst.keys())[list(lst.values()).index(media_name)]

    def create_file_give_id(self, file_name, content_data, parent_id="root", mimetype="text/plain"):
        file_to_upload = self.drive_obj.CreateFile({"title": file_name, "mimeType": mimetype})
        if parent_id != "root":
            file_to_upload = self.drive_obj.CreateFile({"title": file_name, "parents": [{"id": parent_id}]})
        temp_file_name = f"{str(uuid.uuid4())[0:15]}.temp".replace("-", "")
        with open(temp_file_name, "wb") as fp:
            fp.write(content_data)
        file_to_upload.SetContentFile(temp_file_name)
        file_to_upload.Upload()
        os.system(f"del /f {temp_file_name}")
        return self.find_id_by_name(file_name)


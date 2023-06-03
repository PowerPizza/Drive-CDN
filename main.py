"""
developer : scihack/powerpizza
development start date : 1-6-2023
development end date : 3-6-2023
purpose : CDN [Content delivery network] for put my files online and access js files from cloud for free.
"""

import os, sys, mimetypes
import tkinter, threading, json, webbrowser
from tkinter import *
from tkinter import messagebox, filedialog
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials
from drive_adv_functions import GdriveHelper
from messages_about import *

root = tkinter.Tk()
root.geometry("500x500")
root.title("Drive CDN")
root.state("zoomed")
image_icon = PhotoImage(file="assets/app_icon.png")
root.iconphoto(False, image_icon)

# variables and constants --------
current_file = None
loaded_file_dict = {}
file_id_var = StringVar(value="None")
copy_to_clipboard_icon = PhotoImage(file="assets/copy_to_clipboard.png")
about_icon = PhotoImage(file="assets/about_icon.png")
# ---------- END --------------


# DRY functions -------------
def create_heading(master_, text_):
    lbl = Label(master_, text=text_, font=("helvetica", 24, "bold", "underline"), bg="#FFFFFF", fg="#6603fc", height=0)
    lbl.pack()


def create_paragraph(master_, text_):
    lbl = Label(master_, text=text_, font=("helvetica", 18, "bold"), bg="#FFFFFF", wraplength=root.winfo_width(),
                justify=LEFT, height=0)
    lbl.pack(side=LEFT)
    return lbl


def create_hyperlink(master_, link_):
    lnk = create_paragraph(master_, link_)
    lnk.config(font=("Helvetica", 18, "underline", "italic"), fg="blue")

    def on_click_link():
        webbrowser.open(link_)

    lnk.bind("<Button-1>", lambda *eve: threading.Thread(target=on_click_link).start())
    return lnk
# END ----------


# drive setup -------------------
gauth = GoogleAuth()
with open("credentials_file_path.json", "a") as fp:
    pass
gauth_loaded = False

try:
    cred_file_json = json.load(open("credentials_file_path.json", "r"))
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file_json["path"], "https://www.googleapis.com/auth/drive")
    gauth_loaded = True
except BaseException as e:
    print(f"Unable to set drive credentials.\nError : {e}")
    base_setup_canva = Canvas(root, bg="#FFFFFF")
    Label(base_setup_canva, text="Base Setup", font=("helvetica", 18, "underline"), bg="#FFFFFF", fg="#0000FF").pack(pady=2)

    def on_choose_cred_file():
        default_json_ = {"path": "drive_credentials.json"}
        file_ = filedialog.askopenfile(filetypes=(("json files", "*.json"),)).name
        if file_:
            try:
                default_json_["path"] = file_
                json.dump(default_json_, open("credentials_file_path.json", "w"))
                gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(default_json_["path"], "https://www.googleapis.com/auth/drive")
                base_setup_canva.destroy()
                main_canva.pack(side=LEFT, anchor="nw", fill=BOTH, expand=True)
                threading.Thread(target=list_files).start()
            except BaseException as e:
                messagebox.showerror("Invalid Credentials", f"Please provide valid credentials.\nerror : {e}")

    choose_a_cred_file = Button(base_setup_canva, text="Attach credentials file", font=("Helvetica", 14), relief="ridge", command=on_choose_cred_file)
    choose_a_cred_file.pack()

    about_btn = Button(base_setup_canva, image=about_icon, relief="ridge", command=lambda : on_click_about_software())
    about_btn.pack(pady=2)
    base_setup_canva.pack(fill=BOTH, expand=True)

gdrive = GoogleDrive(gauth)
drive_helper = GdriveHelper(gdrive)
print("drive connected")
# end --------------------


# MAIN SOFTWARE GUI
main_canva = Canvas(root, bg="#e8e8e8")

# left panel work --------------/
left_panel = Frame(main_canva, bg="#FFFFFF", highlightthickness=1, highlightbackground="#000000")

# ---------- File listing work ---------------
label_file_list = Label(left_panel, text="Files In Drive", font=("Helvetica", 12), bg="#4a4a4a", fg="#FFFFFF")
label_file_list.pack(fill=X)

fr_LSF_main = Frame(left_panel, bg="#FFFFFF")
fr_LSF = Frame(fr_LSF_main, bg="#FFFFFF")
loading_status_file = Label(fr_LSF, text="Loading Files...", font=("Helvetica", 12), bg="#FFFFFF", fg="#000000")
loading_status_file.pack(fill=X)
fr_LSF_main.pack(fill=X)

frame_file_list = Frame(left_panel, bg="#edfcf0")
file_list = Listbox(frame_file_list, bg="#fcfaed", font=("Helvetica", 12))
fr_LSF.pack_forget()
fr_LSF.pack(fill=X)

def list_files():
    global loaded_file_dict
    loaded_file_dict = drive_helper.list_files_id_title()
    file_list.delete(0, END)
    if not len(loaded_file_dict.values()):
        loading_status_file.config(text="No Files Found.")
        fr_LSF.pack_forget()
        fr_LSF.pack(fill=X)
        return 0
    fr_LSF.pack_forget()
    for itm in loaded_file_dict.values():
        file_list.insert(END, itm)
    return 1

def first_listing():
    try:
        list_files()
    except BaseException as e:
        print("Unable to load file :", e)
        if "No such file or directory" not in str(e):
            threading.Thread(target=first_listing).start()

threading.Thread(target=first_listing).start()

file_list.pack(fill=Y, expand=True)
def on_select_file(*args):
    global current_file
    if len(file_list.get(ANCHOR)):
        current_file = file_list.get(ANCHOR)
        label_current_selected.config(text=f"Selected : {current_file}")
        file_id_var.set(list(loaded_file_dict.keys())[list(loaded_file_dict.values()).index(current_file)])
file_list.bind("<<ListboxSelect>>", on_select_file)

frame_file_list.pack(fill=BOTH, expand=True)
# ------------------ file listing end -------------------


# ------------------ file options work -----------------
label_options = Label(left_panel, text="File Options", font=("Helvetica", 12), bg="#4a4a4a", fg="#FFFFFF")
label_options.pack(fill=X, side=TOP)
frame_options = Frame(left_panel, bg="#edf0fc")

def on_create_new():
    btn_create_new.config(state="disabled")
    root.update()
    data_file = ""

    dialog_window = tkinter.Tk()
    dialog_window.geometry("240x200")
    dialog_window.title("Create File")
    dialog_window.attributes("-topmost", True)
    dialog_window.resizable(False, False)
    def on_close_dialog_win():
        btn_create_new.config(state="normal")
        dialog_window.destroy()
    dialog_window.protocol("WM_DELETE_WINDOW", on_close_dialog_win)

    # vars --------
    file_name_var = StringVar(master=dialog_window)
    mimeType_var = StringVar(master=dialog_window, value="text/plain")
    # end -------

    content_canva = Canvas(dialog_window, bg="#FFFFFF")
    content_canva.pack(fill=BOTH, expand=True)

    frame_entry_1 = Frame(content_canva, bg="#FFFFFF", highlightthickness=1, highlightbackground="#000000", bd=0)
    Label(frame_entry_1, text="File Name : ", bg="#FFFFFF").pack(side=LEFT)
    entry_file_name = Entry(frame_entry_1, textvariable=file_name_var, highlightthickness=1, highlightbackground="#000000", bd=0)
    entry_file_name.pack(padx=2, pady=2, side=LEFT)
    frame_entry_1.pack(padx=2, pady=2)

    frame_entry_2 = Frame(content_canva, bg="#FFFFFF", highlightthickness=1, highlightbackground="#000000", bd=0)
    Label(frame_entry_2, text="mimeType : ", bg="#FFFFFF").pack(side=LEFT)
    manual_mimetype_input = Entry(frame_entry_2, textvariable=mimeType_var, highlightthickness=1, highlightbackground="#000000", bd=0)
    manual_mimetype_input.pack()
    select_mimetype = OptionMenu(frame_entry_2, mimeType_var, *list(mimetypes.types_map.values()))
    select_mimetype.config(highlightthickness=1, highlightbackground="#000000", bd=0)
    select_mimetype.pack()
    frame_entry_2.pack(padx=2, pady=2)

    frame_entry_3 = Frame(content_canva, bg="#FFFFFF")
    def on_click_IFE():
        nonlocal data_file
        file_choose = filedialog.askopenfile()
        if file_choose:
            data_file = file_choose.name
            file_name_var.set(data_file.split("/")[-1])
    btn_IFE = Button(frame_entry_3, text="Import From Explorer", bg="#ccc9ff", relief="ridge", command=on_click_IFE)
    btn_IFE.pack(side=LEFT)
    frame_entry_3.pack(padx=2, pady=2)

    def on_create_file():
        btn_create_file.config(state="disabled", text="Creating...")
        if file_name_var.get() in loaded_file_dict.values():
            messagebox.showerror("Already exists", f"File {file_name_var.get()} is already exists.")
            btn_create_file.config(state="normal", text="Create")
            return
        if "." not in file_name_var.get():
            if not messagebox.askokcancel("No Extension", f"No extension is given to file {file_name_var.get()}.\nDo you want to create file without any extension"):
                btn_create_file.config(state="normal", text="Create")
                return

        if len(data_file):
            file_to_upload = gdrive.CreateFile({"title": file_name_var.get(), "mimeType": mimeType_var.get()})
            file_to_upload.SetContentFile(data_file)
            file_to_upload.Upload()
            file_to_upload.InsertPermission({
                "type": "anyone",
                "value": "anyone",
                "role": "reader"
            })
        else:
            empty_file = gdrive.CreateFile({"title": file_name_var.get(), "mimeType": mimeType_var.get()})
            empty_file.Upload()
            empty_file.InsertPermission({
                "type": "anyone",
                "value": "anyone",
                "role": "reader"
            })
        list_files()
        btn_create_file.config(state="normal", text="Create")
        on_close_dialog_win()
        messagebox.showinfo("Done", "File Created Successful.")

    btn_create_file = Button(content_canva, text="Create", font=("Helvetica", 12), relief="ridge", bg="#d9ffe9", command=lambda :threading.Thread(target=on_create_file).start())
    btn_create_file.pack(side=BOTTOM, padx=2, pady=2, fill=X)

    dialog_window.mainloop()

btn_create_new = Button(frame_options, text="Create New", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=on_create_new)
btn_create_new.pack(fill=X, anchor="nw", pady=1)

def on_edit_file():
    text_box.config(state="normal")
    btn_edit_file.config(state="disabled", text="Opening...")
    if current_file:
        try:
            file_ = gdrive.CreateFile({"id": drive_helper.find_id_by_name(current_file)})
            text_box.delete("1.0", "end")
            text_box.insert(END, file_.GetContentString())
            label_current_open.config(text=f"Opened : {current_file}")
            label_status_changes.pack(side=LEFT, padx=2)
        except BaseException as e:
            print(e)
            if "'utf-8' codec can't decode byte" in str(e):
                messagebox.showerror("Unable to open", "Can't open file in text editor, file contains bytes.")
    btn_edit_file.config(state="normal", text="Edit")

btn_edit_file = Button(frame_options, text="Edit", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=lambda : threading.Thread(target=on_edit_file).start())
btn_edit_file.pack(fill=X, anchor="nw", pady=1)

def on_delete():
    global current_file
    if current_file:
        if messagebox.askyesno("Verify", f"Do you want to delete {current_file} ?"):
            btn_delete.config(state="disabled", text="Deleting...")
            file_to_delete = gdrive.CreateFile({"id": drive_helper.find_id_by_name(current_file)})
            file_to_delete.Delete()
            list_files()
            current_file = None

            label_current_selected.config(text=f"Selected : {current_file}")
            label_current_open.config(text=f"Opened : {current_file}")
            text_box.delete("1.0", END)
            text_box.config(state="disabled")
            file_id_var.set(value="None")
            label_status_changes.pack_forget()

            messagebox.showinfo("Successful", "File Deleted successful.")
    btn_delete.config(state="normal", text="Delete")

btn_delete = Button(frame_options, text="Delete", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=lambda : threading.Thread(target=on_delete).start())
btn_delete.pack(fill=X, anchor="nw", pady=1)

def on_save_file():
    btn_save.config(state="disabled", text="Saving...")
    if current_file:
        file_ = gdrive.CreateFile({"id": drive_helper.find_id_by_name(current_file)})
        file_.SetContentString(text_box.get("1.0", END))
        file_.Upload()
        label_status_changes.config(text="Changes : Saved")
    btn_save.config(state="normal", text="Save")

btn_save = Button(frame_options, text="Save", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=lambda : threading.Thread(target=on_save_file).start())
btn_save.pack(fill=X, pady=1)

def on_click_properties():
    if not current_file:
        return
    btn_properties.config(state="disabled")

    file_metadata = None
    for files_ in gdrive.ListFile({"q": f"'root' in parents and trashed=false"}).GetList():
        if files_["title"] == current_file:
            file_metadata = files_
            break

    properties_win = tkinter.Tk()
    properties_win.geometry("350x400")
    properties_win.title(f"Properties [{current_file}]")
    properties_win.resizable(0, 0)

    copy_to_clipboard_icon2 = PhotoImage(master=properties_win, file="assets/copy_to_clipboard.png")

    def on_close_prop_win():
        btn_properties.config(state="normal")
        properties_win.destroy()
    properties_win.protocol("WM_DELETE_WINDOW", on_close_prop_win)

    prop_canvas = Canvas(properties_win, bg="#fdffba")

    prop_canvas.pack(fill=BOTH, expand=True)
    label_head = Label(prop_canvas, text=f"Properties of {current_file}", bg="#e3ffba", font=("Helvetica", 14))
    label_head.pack(fill=X)

    frame_info_viewer = Frame(prop_canvas, bg="#fdffba")

    info_fr_1 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_1, f"File Name - {file_metadata['originalFilename']}").config(font=("Helvetica", 12), bg="#fdffba")
    info_fr_1.pack(fill=X, padx=2, pady=1)

    info_fr_2 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_2, f"Mime Type - {file_metadata['mimeType']}").config(font=("Helvetica", 12), bg="#fdffba")
    info_fr_2.pack(fill=X, padx=2, pady=1)

    info_fr_3 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_3, f"File Size - {format(int(file_metadata['fileSize'])/1000, 'f')} KB").config(font=("Helvetica", 12), bg="#fdffba")
    info_fr_3.pack(fill=X, padx=2, pady=1)

    info_fr_4 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_4, f"View Link - ").config(font=("Helvetica", 12), bg="#fdffba")
    Button(info_fr_4, text="Web View", bg="#d8baff", relief="ridge", command=lambda : webbrowser.open(file_metadata['alternateLink'])).pack(side=LEFT)
    info_fr_4.pack(fill=X, padx=2, pady=1)

    info_fr_5 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_5, f"Download Link - ").config(font=("Helvetica", 12), bg="#fdffba")
    Button(info_fr_5, text="Download", bg="#d8baff", relief="ridge", command=lambda : webbrowser.open(file_metadata['webContentLink'])).pack(side=LEFT)
    info_fr_5.pack(fill=X, padx=2, pady=1)

    info_fr_6 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_6, f"Creation Date - {file_metadata['createdDate'].replace('T', ' ; ').replace('Z', '')}").config(font=("Helvetica", 12), bg="#fdffba")
    info_fr_6.pack(fill=X, padx=2, pady=1)

    info_fr_7 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_7, f"Modified Like - {file_metadata['modifiedDate'].replace('T', ' ; ').replace('Z', '')}").config(font=("Helvetica", 12), bg="#fdffba")
    info_fr_7.pack(fill=X, padx=2, pady=1)

    info_fr_8 = Frame(frame_info_viewer, bg="#fdffba")
    create_paragraph(info_fr_8, f"Src Link - ").config(font=("Helvetica", 12), bg="#fdffba")
    Entry(info_fr_8, textvariable=StringVar(master=properties_win, value=f"https://drive.google.com/uc?id={file_metadata['id']}"), state="disabled", relief="ridge").pack(side=LEFT)
    def copy_link():
        root.clipboard_clear()
        root.clipboard_append(f"https://drive.google.com/uc?id={file_metadata['id']}")
    Button(info_fr_8, image=copy_to_clipboard_icon2, relief="ridge", command=copy_link).pack(side=LEFT, padx=2)
    info_fr_8.pack(fill=X, padx=2, pady=1)

    frame_info_viewer.pack(fill=BOTH, expand=True)

    properties_win.mainloop()

btn_properties = Button(frame_options, text="Properties", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=lambda : threading.Thread(target=on_click_properties).start())
btn_properties.pack(fill=X, pady=1)

frame_options.pack(fill=BOTH, expand=True)
# ----------------- file option end -------------------


# -------------- advance options work ------------------
label_options = Label(left_panel, text="Advance Options", font=("Helvetica", 12), bg="#4a4a4a", fg="#FFFFFF")
label_options.pack(fill=X, side=TOP)

frame_adv_options = Frame(left_panel, bg="#edf0fc")

def on_change_cred_file():
    if messagebox.askyesno("Verify", "Do you really want to change credentials file by deleting old one ?"):
        os.remove("credentials_file_path.json")
        messagebox.showinfo("Restart", "Please restart the software to load new credentials.")
        sys.exit(400)

btn_change_cred_file = Button(frame_adv_options, text="Change Credentials", font=("Helvetica", 12), relief="ridge", bg="#8f95f7", command=on_change_cred_file)
btn_change_cred_file.pack(fill=X, pady=1)

def on_clear_CDN():
    global current_file
    if messagebox.askyesno("Verify", "This operation will delete all the files present on this CDN do you want to continue ?"):
        btn_clear_CDN.config(state="disabled", text="Clearing...")
        for i in range(len(loaded_file_dict.keys())):
            btn_clear_CDN.config(text=f"Cleared : {i+1}/{len(loaded_file_dict.keys())}")
            file_ = gdrive.CreateFile({"id": list(loaded_file_dict.keys())[i]})
            file_.Delete()
        list_files()

        current_file = None
        label_current_selected.config(text=f"Selected : {current_file}")
        label_current_open.config(text=f"Opened : {current_file}")
        text_box.delete("1.0", END)
        text_box.config(state="disabled")
        file_id_var.set(value="None")
        label_status_changes.pack_forget()

        messagebox.showinfo("Done", "CDN has been empty now.")
        btn_clear_CDN.config(state="normal", text="Clear CDN")

btn_clear_CDN = Button(frame_adv_options, text="Clear CDN", font=("Helvetica", 12), relief="ridge", bg="#ffcdc9", command=lambda : threading.Thread(target=on_clear_CDN).start())
btn_clear_CDN.pack(fill=X, pady=1)
frame_adv_options.pack(fill=BOTH, expand=True)
# -------------- advance options end ------------------

left_panel.pack(side=LEFT, fill=Y)
# END ------------------/


editor_panel = Frame(main_canva, bg="#FFFFFF", highlightthickness=1, highlightbackground="#000000")

frame_status_bar = Frame(editor_panel, bg="#FFFFFF")

label_current_selected = Label(frame_status_bar, text=f"Selected : None", bg="#4a4a4a", fg="#FFFFFF", font=("Helvetica", 12))
label_current_selected.pack(side=LEFT, padx=2)

fr_opened_file_id = Frame(frame_status_bar)
lbl_opened_file_id = Label(fr_opened_file_id, text=f"File ID : ", bg="#4a4a4a", fg="#FFFFFF", font=("Helvetica", 12))
lbl_opened_file_id.pack(side=LEFT, padx=2)
entry_copyable_id = Entry(fr_opened_file_id, font=("Helvetica", 12), bd=0, state="disabled", highlightthickness=1, highlightbackground="#4a4a4a", textvariable=file_id_var)
entry_copyable_id.pack(side=LEFT)
def on_copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(file_id_var.get())
btn_copy_id = Button(fr_opened_file_id, image=copy_to_clipboard_icon, bg="#d0ffcc", relief="ridge", command=on_copy_to_clipboard)
btn_copy_id.pack(side=LEFT)
fr_opened_file_id.pack(side=LEFT)

label_current_open = Label(frame_status_bar, text=f"Opened : {current_file}", bg="#4a4a4a", fg="#FFFFFF", font=("Helvetica", 12))
label_current_open.pack(side=LEFT, padx=2)

label_status_changes = Label(frame_status_bar, text=f"Changes : Saved", bg="#4a4a4a", fg="#FFFFFF", font=("Helvetica", 12))

def on_click_about_software():
    root.state("zoomed")
    about_canva = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="#FFFFFF")

    fr_top_bar = Frame(about_canva, bg="#FFFFFF", highlightbackground="#000000", highlightthickness=1)
    def onclick_close_about():
        about_canva.destroy()
        root.unbind("<MouseWheel>", binder_id)

    btn_close_about = Button(fr_top_bar, text="⬅ Back", font=("Helvetica", 12), relief="ridge", bg="#96ffce", fg="#0000FF", command=onclick_close_about)
    btn_close_about.pack(side=LEFT, anchor="nw")

    fr_top_bar.pack(fill=X)

    frame_container_text = Frame(about_canva, bg="#FFFFFF")

    frame_text = Frame(frame_container_text, bg="#FFFFFF")  # scrollable

    fr_segment_1 = Frame(frame_text, bg="#FFFFFF")
    create_heading(fr_segment_1, "Introduction of Software")
    create_paragraph(fr_segment_1, introduction_software)
    fr_segment_1.pack(fill=X)


    fr_segment_2 = Frame(frame_text, bg="#FFFFFF")
    create_heading(fr_segment_2, "How to use ?")

    fr_link_1 = Frame(fr_segment_2, bg="#FFFFFF")
    create_paragraph(fr_link_1, "NOTE : Video tutorial may be more helpful ")
    create_hyperlink(fr_link_1, "https://youtu.be/Gfur2E4TKzQ")
    fr_link_1.pack(fill=X)

    fr_link_2 = Frame(fr_segment_2, bg="#FFFFFF")
    create_paragraph(fr_link_2, how_to_use_s1)
    create_hyperlink(fr_link_2, "https://console.cloud.google.com/")
    fr_link_2.pack(fill=X)

    fr_para1 = Frame(fr_segment_2, bg="#FFFFFF")
    create_paragraph(fr_para1, how_to_use_s2)
    fr_para1.pack(fill=X)

    fr_segment_2.pack(fill=X)


    fr_segment_3 = Frame(frame_text, bg="#FFFFFF")
    create_heading(fr_segment_3, "Developer Details")

    fr_s3_p1 = Frame(fr_segment_3, bg="#FFFFFF")
    create_paragraph(fr_s3_p1, "Name : Scihack/powerpizza")
    fr_s3_p1.pack(fill=X)

    fr_s3_p3 = Frame(fr_segment_3, bg="#FFFFFF")
    create_paragraph(fr_s3_p3, "Gmail : scihack.official@gmail.com")
    fr_s3_p3.pack(fill=X)

    fr_s3_l1 = Frame(fr_segment_3, bg="#FFFFFF")
    create_paragraph(fr_s3_l1, "Github : ")
    create_hyperlink(fr_s3_l1, "https://github.com/powerpizza")
    fr_s3_l1.pack(fill=X)

    fr_s3_l2 = Frame(fr_segment_3, bg="#FFFFFF")
    create_paragraph(fr_s3_l2, "Youtube : ")
    create_hyperlink(fr_s3_l2, "https://www.youtube.com/channel/UCFHxcui4fu2Sxf3RFj03h_Q")
    fr_s3_l2.pack(fill=X)

    fr_s3_p2 = Frame(fr_segment_3, bg="#FFFFFF")
    create_paragraph(fr_s3_p2, "Discord : scihack223#4934")
    fr_s3_p2.pack(fill=X)

    fr_segment_3.pack(fill=X)

    frame_text.pack()
    frame_container_text.pack()
    frame_text.update()
    frame_text.pack_forget()
    frame_text.place(x=0, y=0)

    about_canva.place(x=0, y=0)

    scrolled = 0
    def on_scroll_about_canva(eve):
        nonlocal scrolled
        frame_text.update()
        if eve.delta < 0 and frame_text.winfo_screenheight() - frame_text.winfo_height() <= frame_text.winfo_y()+120:
            scrolled -= 10
            frame_text.place(x=0, y=scrolled)
        elif eve.delta > 0 and frame_text.winfo_y()+10 <= 0:
            scrolled += 10
            frame_text.place(x=0, y=scrolled)

    binder_id = root.bind("<MouseWheel>", on_scroll_about_canva)

btn_about_software = Button(frame_status_bar, image=about_icon, relief="ridge", bg="#8a90ff", command=on_click_about_software)
btn_about_software.pack(side=RIGHT, padx=2)

frame_status_bar.pack(fill=X, pady=1)

text_box = Text(editor_panel, bg="#fffcf2", font=("Helvetica", 12), state="disabled")
text_box.pack(fill=BOTH, expand=True)
text_box.bind("<KeyPress>", lambda *eve: label_status_changes.config(text="Changes : Unsaved"))
editor_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=1)

if gauth_loaded:
    main_canva.pack(side=LEFT, anchor="nw", fill=BOTH, expand=True)

root.mainloop()
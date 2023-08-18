import expiry_changer

username = ""
password = ""

urls = [
    ("http://localhost:8069","DatabaseName"),
    ("http://localhost:8070","DatabaseName2"),
]    


for url,db in urls:
    try:
        expiry_changer.DataBaseTools(url,db,username,password)
    except Exception as e:
        print(e)
        continue

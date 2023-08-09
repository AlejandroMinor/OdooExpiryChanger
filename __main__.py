import expiry_changer

username = ""
password = ""

urls = [
    ("http://localhost:8069","DatabaseName"),
    ("http://localhost:8070","DatabaseName2"),
]    


for url,db in urls:
    expiry_changer.DataBaseTools(url,db,username,password)

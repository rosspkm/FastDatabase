import fdb

struc = fdb.Structure()
struc.Create("temp")
struc.AddTable("temp", "test")
struc.AddField("temp", "test", "chloe")



db = fdb.database()
db.SelectDB('temp')
db.SelectTable('test')
db.Insert("haha lol123")
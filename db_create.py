from models import BlogPost, BlogUser, db

# Create the database and the tables
print("Create Database & Tables : ", flush=True, end="")
db.create_all()
print("Ok")

# insert records
print("Insert records in Tables : ", flush=True, end="")
db.session.add(BlogUser("admin", "cle", "password"))

db.session.add(BlogPost("Bon", "je suis bon !"))
db.session.add(BlogPost("Bien", "je vais bien !"))
print("Ok")

# commit
print("Commit : ", flush=True, end="")
db.session.commit()
print("Ok")
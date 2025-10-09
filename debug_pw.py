from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

plain_pw = "ramesh"
hashed_pw = "$2b$12$dzP.nh514gnBuFjZ7FmCIes.c0n5GCaVz6rB/XeLDOoRE7GnMBtmy"

print("plain repr:", repr(plain_pw))
print("plain len chars:", len(plain_pw))
print("plain len bytes:", len(plain_pw.encode('utf-8')))
print("hash repr:", repr(hashed_pw))
print("hash len:", len(hashed_pw))

# passlib verify
try:
    print("passlib verify ->", pwd_context.verify(plain_pw, hashed_pw))
except Exception as e:
    print("passlib verify raised:", repr(e))

# bcrypt library verify
try:
    print("bcrypt checkpw ->", bcrypt.checkpw(plain_pw.encode('utf-8'), hashed_pw.encode('utf-8')))
except Exception as e:
    print("bcrypt.checkpw raised:", repr(e))

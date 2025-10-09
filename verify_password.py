from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_pw = "$2b$12$dzP.nh514gnBuFjZ7FmCIes.c0n5GCaVz6rB/XeLDOoRE7GnMBtmy"
plain_pw = "ramesh"

print(pwd_context.verify(plain_pw, hashed_pw))

##用來生成雜湊後的登入帳密表

import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Mr.admin","Mr.test"]
usernames = ["admin","test"]
passwords = ["XXX","XXX"]

hashed_passwords = stauth.utilities.hasher.Hasher(passwords).generate()
print(hashed_passwords)


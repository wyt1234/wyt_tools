import re

zh_pattern = re.compile(r'[\u4e00-\u9fa5]+')
email_pattern = re.compile(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$")
phone_pattern = re.compile(r'^1([3-9])[0-9]{9}$')
pwd_pattern = re.compile(r'^[0-9a-zA-Z]{6,24}$')


def is_valid_email(email: str):
    return email_pattern.match(email)


def is_valid_phone(phone: str):
    return phone_pattern.match(phone)


def is_valid_pwd(pwd: str):
    return pwd_pattern.match(pwd)


def contain_zh(text):
    match = re.search(zh_pattern, text)
    return True if match else False

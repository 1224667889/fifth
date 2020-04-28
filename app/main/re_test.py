"""mirrorlied begin at 2020/4/18"""
import re

#usn = /^\w{4,18}$/;
#psw = /(?!^\d+$)^.{6,18}$/;

def re_username(test_str):
    ret = re.match(r"^\w{4,18}$", test_str)
    if ret:
        return True
    else:
        return False

def re_password(test_str):
    ret = re.match(r"(?!^\d+$)^.{6,18}$", test_str)
    if ret:
        return True
    else:
        return False
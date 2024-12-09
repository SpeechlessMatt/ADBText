import os
from loguru import logger
import base64


class AdbInstallErr(Exception):
    def __init__(self, e):
        print(e)

# 一定要加r
ADB_EXE = r'"platform-tools/adb.exe"'

def check_device() -> bool:
    process = os.popen(f"{ADB_EXE} devices")
    ret = process.readlines()
    logger.trace("check devices..")
    logger.info(f"check devices\n{ret}")
    if len(ret) == 2:
        return False
    return True


def get_devices() -> list:
    process = os.popen(f"{ADB_EXE} devices")
    ret = process.readlines()
    logger.trace("get devices")
    device_list = []
    for i in range(1, len(ret) - 1):
        device_list.append(ret[i])
    return device_list


def adb_install(apk):
    process = os.popen(f"{ADB_EXE} install {apk}")
    ret = process.readlines()
    logger.trace("adb install finished")
    if ret[1].rstrip() == "Success":
        logger.info("install success")
        return True
    logger.warning(f"ADB error:\n{ret}")
    raise AdbInstallErr(ret)


def check_using_ime():
    process = os.popen(f"{ADB_EXE} shell settings get secure default_input_method")
    ret = process.readlines()[0].rstrip()
    logger.info(f"正在使用的输入法:{ret}")
    return ret


# 勾选输入法
def enable_ime(ime):
    process = os.popen(f"{ADB_EXE} shell ime enable {ime}")
    ret = process.readlines()[0].rstrip()
    logger.info(f"{ret}")
    return ret


# 启用输入法
def set_ime(ime):
    process = os.popen(f"{ADB_EXE} shell ime set {ime}")
    ret = process.readlines()[0].rstrip()
    logger.info(f"{ret}")
    return ret


def send_text(text):
    encode_str = str(base64.b64encode(text.encode('utf-8')), "utf-8")
    logger.debug(f"base64编码：f{encode_str}")
    logger.trace("发送命令:adb shell am broadcast -a ADB_INPUT_B64 --es msg '{encode_str}'")
    process = os.popen(f"{ADB_EXE} shell am broadcast -a ADB_INPUT_B64 --es msg '{encode_str}'")
    ret = process.readlines()
    logger.debug(f"发送文字：adb返回状态:\n{ret}")

def active():
    pass

def check_installed(bundle_name: str) -> bool:
    process = os.popen(f"{ADB_EXE} shell pm list packages -3")
    ret = process.readlines()
    logger.trace(ret)
    for i in ret:
        bundle = i.replace("package:", "").rstrip()
        logger.trace(bundle)
        if bundle == bundle_name:
            logger.info(f"找到:{bundle_name}")
            return True
    logger.debug("没有发现该包名")
    return False


def uninstall(bundle_name) -> bool:
    if not check_installed(bundle_name):
        return False
    process = os.popen(f"{ADB_EXE} uninstall {bundle_name}")
    ret = process.readlines()
    logger.debug(f"(adb)uninstall:{ret}")
    if ret[0].rstrip() == "Success":
        logger.info("delete success")
        return True

# enable_ime("com.android.adbkeyboard/.AdbIME")
# set_ime("com.android.adbkeyboard/.AdbIME")
# send_text("你好你是sdifoasdjf';'';")

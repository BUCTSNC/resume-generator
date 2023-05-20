import requests
import os

font_hash_checklist = {"SourceHanSansSC-Bold.otf":"914f583e687036332cd072dc61600c7b",
"SourceHanSansSC-ExtraLight.otf":"e545887a389fb4005a017b12f77c1457",
"SourceHanSansSC-Heavy.otf":"c469026e73e004f3bace31bebad459eb",
"SourceHanSansSC-Light.otf":"2f276822468c742bc6e2484814e4f624",
"SourceHanSansSC-Medium.otf":"78c934173750e6cf0612fa2c8c391a5c",
"SourceHanSansSC-Normal.otf":"f5c7050344d0bcb0d6e87250fe99c70f",
"SourceHanSansSC-Regular.otf":"32c532646132e7e6755b81fef52e8b13",
"SourceHanSerifSC-Bold.otf":"1b9afd8c5105c77381a6e64f8122e894",
"SourceHanSerifSC-ExtraLight.otf":"921372e09a2b5bfded6fce448ea2b51f",
"SourceHanSerifSC-Heavy.otf":"e1f7b4210a108ff33bbe8722522825c6",
"SourceHanSerifSC-Light.otf":"2e5b44cbac602e1ec362a521c80fa675",
"SourceHanSerifSC-Medium.otf":"1f5f4d4793a1914231cc1340aa9dc6b4",
"SourceHanSerifSC-Regular.otf":"d140b6b3ad0e2f4961467a90446d2fd0",
"SourceHanSerifSC-SemiBold.otf":"464ea322f8c47267896bcdaf198d4c98"}


def get_fonts(font_weighted_name: str):
    # https://mirrors.tuna.tsinghua.edu.cn/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/
    # https://mirrors.tuna.tsinghua.edu.cn/adobe-fonts/source-han-sans/OTF/SimplifiedChinese/
    pass


def check_crc32(file_path: str, font_weighted_name: str):
    import hashlib

    flag_ensure_font_original = True
    flag_build_dict=False
    try:
        # print(file_path)
        file_raw = open(file_path, "rb")
    except:
        print("[ERROR]Failed to open font file.")
        return -1
    temp_hash = hashlib.md5()
    temp_hash.update(b"HelloWorld")
    temp_hash.update(file_raw.read())
    hash_result = str(temp_hash.hexdigest())
    if flag_build_dict==True:
        print("\""+font_weighted_name+"\":\""+hash_result+"\",") 
        return 1
    if hash_result == "68e109f0f40ca72a15e05cc22786f8e6":
        print("[ERROR]Failed to calc MD5")  # "HelloWorld"'s MD5 is above
    else:
        if font_hash_checklist.get(font_weighted_name) != hash_result:
            print("[WARN]Font file was not original")
            if flag_ensure_font_original == True:
                get_fonts(font_weighted_name=font_weighted_name)
        else:
            print("[INFO]" + font_weighted_name + " passed check.")
    return 0


def pre_check_fonts():
    if os.getcwd() != __file__.replace("build.py", ""):
        print("[WARN]Not running in root working dictionary.")
    font_family = ["source-han-sans", "source-han-serif"]
    for name in font_family:
        if os.path.exists(
            os.path.join(__file__.replace("build.py", ""), "fonts", name)
        ):
            font_list = os.listdir(
                os.path.join(__file__.replace("build.py", ""), "fonts", name)
            )
            for weight in font_list:
                check_crc32(
                    os.path.join(
                        __file__.replace("build.py", ""), "fonts", name, weight
                    ),
                    weight,
                )


def pre_check():
    pre_check_fonts()


def complie():
    pass


def clean_up():
    pass


def main():
    flag_clean_up = False
    pre_check()
    complie()
    if flag_clean_up == True:
        clean_up()


if __name__ == "__main__":
    main()

import requests
import os

font_hash_checklist = {"afaffdfaf": "68e109f0f40ca72a15e05cc22786f8e6"}


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

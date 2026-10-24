from encodings import utf_8
from pathlib import Path

def read_file():
    #获取文件的根目录
    project_root = Path(__file__).resolve().parent
    #构建文件路径
    project_path = project_root.joinpath("data").joinpath("samples.txt")
    #读取文件的内容
    content = project_path.read_text(encoding="utf-8")
    #输出结果
    print("文件读取开始！")
    print("content:", content)
    print("文件读取结束!")
if __name__ == "__main__":
   read_file()



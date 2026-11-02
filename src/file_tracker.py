import json
from pathlib import Path
from src.fingerprint import fingerprint_file
from src.logger_handler import get_logger

logger = get_logger("file_tracker")

def load_index(index_path:str)->dict:
    #1.判断路径是否合法
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(index_path).resolve()
    if not  file_path.exists():
        logger.info(f"索引文件不存在,创建空索引:{file_path}")
        return {"files":[]}
    if not file_path.is_file():
        logger.error(f"索引路径不是普通文件:{file_path}")
        raise ValueError(f"不是普通文件:{file_path}")
    if  file_path.suffix !=".json":
        logger.error(f"不支持索引类型:{file_path.suffix}")
        raise TypeError("该类型文件不支持处理！")
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"索引文件解析失败: {file_path}")
        raise ValueError(f"索引文件已损坏，无法解析: {file_path}") from e
    return data


def save_index(index_path:str,data:dict)->None:
    #1.判断路径是否合法
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(index_path).resolve()
    #检查后缀
    if file_path.suffix.lower() !=".json":
        logger.error("该类型文件不支持处理")
        raise TypeError("该类型文件不支持处理!")
    #确保父目录存在
    file_path.parent.mkdir(parents=True,exist_ok=True)
    #写入JSON
    with open(file_path,'w',encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    logger.info(f"文件索引保存成功:{file_path}")


def is_processed(data:dict,file_hash:str)->bool:
    #1.传入file_hash
    #2.取出data["files"]
    #3.逐条遍历record
    for  record in data["files"]:
        # 4.对比record和file_hash
        if record["hash"] == file_hash:
            return True
    return False


def add_file(data:dict,path:str,file_hash:str)->None:
    #将path转化成Path对象
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    #获取文件字节大小
    file_size = file_path.stat().st_size
    #获取文件修改时间
    file_time = file_path.stat().st_mtime
    record = {"hash": file_hash, "path": path, "size": file_size, "mtime": file_time}
    data["files"].append(record)
    logger.info(f"文件记录添加成功: {path}")

def update_file(data:dict,path:str,file_hash:str)->bool:
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    file_size = file_path.stat().st_size
    file_time = file_path.stat().st_mtime
    for record in data["files"]:
        if record["path"] == path:
            record["hash"] = file_hash
            record["size"] = file_size
            record["mtime"] = file_time
            return True
    logger.warning(f"没有找到需要更新的文件记录: {path}")
    return False



if __name__ == '__main__':
    data = load_index(index_path="data/index.json")
    file_hash = fingerprint_file("data/example.json")
    if not is_processed(data,file_hash):
        add_file(data,path="data/example.json",file_hash=file_hash)
    else:
       logger.info("该文件已经被处理过")
    save_index("data/index.json",data)


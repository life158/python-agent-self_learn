import logging
import sys
from pathlib import Path
def get_logger(name: str)->logging.Logger:
    # 获取 Logger
    logger = logging.getLogger(name)

    # 设置 Logger 日志等级
    logger.setLevel(logging.DEBUG)

    # 只有没有 Handler 时，才进行配置
    if not logger.handlers:

        # 创建 Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 创建控制台 Handler
        control_handler = logging.StreamHandler(stream=sys.stdout)
        control_handler.setFormatter(formatter)

        # 创建日志文件路径
        log_path = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            .joinpath(f"logs/{name}.log")
        )

        # 创建 logs 目录
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 创建文件 Handler
        file_handler = logging.FileHandler(
            log_path,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # 添加 Handler
        logger.addHandler(control_handler)
        logger.addHandler(file_handler)
    return logger
if __name__ == "__main__":
    logger1 = get_logger("test")
    logger2 = get_logger("test")
    logger3 = get_logger("test")

    print(logger1 is logger2)
    print(logger2 is logger3)
    print(len(logger1.handlers))

    logger1.info("Hello Agent")

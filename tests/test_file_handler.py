from src.file_handler import load_file


def test_txt():
    result = load_file("data/samples.txt")

    assert isinstance(result, dict)
    assert isinstance(result["content"], str)
    assert result["type"] == ".txt"


def test_md():
    result = load_file("data/example.md")

    assert isinstance(result["content"], str)
    assert result["type"] == ".md"


def test_json():
    result = load_file("data/example.json")

    assert isinstance(result["content"], str)
    assert result["type"] == ".json"



import pytest

def test_unsupported_file(tmp_path):
    # 1. 创建一个临时 PDF 文件
    pdf_file = tmp_path / "example.pdf"

    # 2. 写入测试内容，确保文件真实存在
    pdf_file.write_text("test content", encoding="utf-8")

    # 3. 验证不支持的文件类型是否抛出 TypeError
    with pytest.raises(TypeError):
        load_file(str(pdf_file))



if __name__ == "__main__":
    test_txt()
    test_md()
    test_json()
    print("TXT、MD、JSON 测试通过！")
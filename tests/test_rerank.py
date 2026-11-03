import subprocess
import sys


def test_rerank_lazy_import():

    code = """
import sys
import src.rerank

assert "sentence_transformers" not in sys.modules
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
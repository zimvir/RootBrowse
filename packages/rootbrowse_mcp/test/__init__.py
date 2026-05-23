"""pytest 配置"""

import sys
from pathlib import Path

# 将 src 目录加入 Python 路径
rootbrowse_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(rootbrowse_src))
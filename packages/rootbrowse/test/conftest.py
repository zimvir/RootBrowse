"""pytest 配置"""

import sys
from pathlib import Path

# 将根目录加入 Python 路径
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

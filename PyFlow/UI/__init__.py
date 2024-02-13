import sys
import os
from .EditorHistory import EditorHistory

fileDir = os.path.dirname(__file__)
fileDir = fileDir.replace("\\", "/")
sys.path.append(fileDir)
RESOURCES_DIR = fileDir + "/resources"

editor_history = EditorHistory()
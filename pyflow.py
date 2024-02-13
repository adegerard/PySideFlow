import signal
import sys
from PyFlow.App import PyFlow
from PySide6.QtWidgets import QApplication
import argparse
import os
import json


def main():
    app = QApplication(sys.argv)

    instance = PyFlow.instance(software="standalone")
    if instance is not None:
        instance.activateWindow()
        instance.show()

        parser = argparse.ArgumentParser(description="PyFlow CLI")
        parser.add_argument("-f", "--filePath", type=str, default="Untitled.pygraph")
        parsedArguments, unknown = parser.parse_known_args(sys.argv[1:])
        filePath = parsedArguments.filePath
        if not filePath.endswith(".pygraph"):
            filePath += ".pygraph"
        if os.path.exists(filePath):
                with open(filePath, 'r') as f:
                    data = json.load(f)
                    instance.loadFromData(data)
                    instance.currentFileName = filePath

        try:
            sys.exit(app.exec())
        except Exception as e:
            print(e)


        try:
            sys.exit(app.exec())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

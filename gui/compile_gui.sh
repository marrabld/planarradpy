#!/bin/bash

pyrcc4 resources.qrc -o resources_rc.py
pyuic4 gui_Layout.ui -o gui_Layout.py
pyuic4 aboutGui.ui -o gui_About.py
pyuic4 logReader.ui -o gui_log.py

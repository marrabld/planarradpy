#!/bin/bash

pyrcc4 resources.qrc -o resources_rc.py
pyuic4 gui_Layout.ui -o gui_Layout.py

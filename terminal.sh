#!/bin/bash

if [[ $(pgrep -x konsole) ]]; then     xdotool windowactivate `xdotool search --pid $(pgrep -x konsole ) | tail -1`; else     konsole; fi

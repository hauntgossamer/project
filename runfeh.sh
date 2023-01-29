#!/bin/bash
cd /tmp/imgs > /dev/null 2>1&
feh /tmp/imgs/*.png -g $1x$2 --slideshow-delay $3 --reload 60 --scale-down --auto-zoom -y --no-jump-on-resort -p -R 60 --quiet --title Scraypuh  2>/dev/null
#!/bin/bash
cd /tmp/imgs > /dev/null 2> /dev/null
feh /tmp/imgs/*.png -g $1x$2 --slideshow-delay $3 --reload 60 --scale-down --auto-zoom -y --no-jump-on-resort -p -R 60 --quiet --title Scraypuh --randomize 2>/dev/null

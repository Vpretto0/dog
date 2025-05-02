<!--
Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.

Downloading, reproducing, distributing or otherwise using the SDK Software
is subject to the terms and conditions of the Boston Dynamics Software
Development Kit License (20191101-BDSDK-SL).
-->

# Live-Color Camera

TODO

## Known Issues

This example will fail on Mac due to a problem opening the window related to an opengl shader compile version issue.

TODO get issues from both base examples.

## Required Items

- none

## Installation Steps

### Install Packages on PC

Navigate via the CLI on your PC to the stitch_front_images directory and review the requirements.txt file. Several python packages are described and can be installed using the following command line:

```
python3 -m pip install -r requirements.txt
```

## To execute

live_feed.py

```
python live_feed.py 192.168.80.3 --image-source frontright_fisheye_image --image-source frontleft_fisheye_image --pixel-format PIXEL_FORMAT_RGB_U8 -j 50 --auto-rotate
```

live_feed_stiched.py

```
x
```
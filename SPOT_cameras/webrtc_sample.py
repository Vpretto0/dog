# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

import asyncio
import logging
import sys
import threading

from aiortc import RTCConfiguration
from aiortc.contrib.media import MediaRecorder
from SPOT_cameras.webrtc_client_sample import WebRTCClient

from bosdyn.client.command_line import Command, Subcommands

logging.basicConfig(level=logging.DEBUG, filename='webrtc.log', filemode='a+')
STDERR = logging.getLogger('stderr')


class InterceptStdErr:#?
    """Intercept all exceptions and print them to StdErr without interrupting."""
    _stderr = sys.stderr

    def __init__(self):
        pass

    def write(self, data):
        STDERR.error(data)


class WebRTCCommands(Subcommands):
    """Commands related to the Spot CAM's WebRTC service"""

    NAME = 'webrtc'

    def __init__(self, subparsers, command_dict):
        super(WebRTCCommands, self).__init__(subparsers, command_dict,
                                             [WebRTCSaveCommand, WebRTCRecordCommand]) #no vamos a grabar


class WebRTCSaveCommand(Command): #tampoco
    """Save webrtc stream as a sequence of images"""

    NAME = 'save'

    def __init__(self, subparsers, command_dict):
        super(WebRTCSaveCommand, self).__init__(subparsers, command_dict)
        self._parser.add_argument('track', default='video', const='video', nargs='?',
                                  choices=['video'])
        self._parser.add_argument('--sdp-filename', default='h264.sdp',
                                  help='File being streamed from WebRTC server')
        self._parser.add_argument('--sdp-port', default=31102, help='SDP port of WebRTC server')
        self._parser.add_argument('--cam-ssl-cert', default=None,
                                  help='Spot CAM\'s client cert path to check with Spot CAM server')
        self._parser.add_argument('--dst-prefix', default='h264.sdp',
                                  help='Filename prefix to prepend to all output data')
        self._parser.add_argument('--count', type=int, default=1,
                                  help='Number of images to save. 0 to stream without saving.')

    def _run(self, robot, options):
        # Suppress all exceptions and log them instead.
        sys.stderr = InterceptStdErr()

        if not options.cam_ssl_cert:
            options.cam_ssl_cert = False

        shutdown_flag = threading.Event()
        webrtc_thread = threading.Thread(
            target=start_webrtc, args=[shutdown_flag, options, robot.user_token, process_frame],
            daemon=True)
        webrtc_thread.start()

        try:
            webrtc_thread.join()
            print('Successfully saved webrtc images to local directory.') #no vamos a guardar imagenes
        except KeyboardInterrupt:
            shutdown_flag.set()
            webrtc_thread.join(timeout=3.0)


class WebRTCRecordCommand(Command): #no vamos a grabar nada
    """Save webrtc stream as video or audio"""

    NAME = 'record'

    def __init__(self, subparsers, command_dict):
        super(WebRTCRecordCommand, self).__init__(subparsers, command_dict)
        self._parser.add_argument('track', default='video', const='video', nargs='?',
                                  choices=['video', 'audio'])
        self._parser.add_argument('--sdp-filename', default='h264.sdp',
                                  help='File being streamed from WebRTC server')
        self._parser.add_argument('--sdp-port', default=31102, help='SDP port of WebRTC server')
        self._parser.add_argument('--cam-ssl-cert', default=None,
                                  help='Spot CAM\'s client cert path to check with Spot CAM server')
        self._parser.add_argument('--dst-prefix', default='h264.sdp',
                                  help='Filename prefix to prepend to all output data')
        self._parser.add_argument('--time', type=int, default=10,
                                  help='Number of seconds to record.')

    def _run(self, robot, options):
        # Suppress all exceptions and log them instead.
        sys.stderr = InterceptStdErr()

        if not options.cam_ssl_cert:
            options.cam_ssl_cert = False

        if options.track == 'video':
            recorder = MediaRecorder(f'{options.dst_prefix}.mp4')
        else:
            recorder = MediaRecorder(f'{options.dst_prefix}.wav')

        # run event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(record_webrtc(options, robot.user_token, recorder))




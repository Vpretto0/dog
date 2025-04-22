import asyncio
import base64
import requests
import threading
import cv2
import sys
import logging
import numpy as np
import argparse
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCConfiguration
from aiortc.contrib.media import MediaRecorder
from bosdyn.client.command_line import Command, Subcommands
from bosdyn.api import image_pb2
from bosdyn.api.spot_cam import camera_pb2, logging_pb2
from bosdyn.client.spot_cam.media_log import MediaLogClient
import bosdyn.client.util
from bosdyn.client.directory_registration import DirectoryRegistrationClient, DirectoryRegistrationKeepAlive
from bosdyn.client.data_acquisition_plugin_service import DataAcquisitionPluginService
from bosdyn.client.auth import AuthClient


DEFAULT_WEB_REQUEST_TIMEOUT = 10.0
    
logging.basicConfig(level=logging.DEBUG, filename='webrtc.log', filemode='a+')
STDERR = logging.getLogger('stderr')


class InterceptStdErr:#?
    """Intercept all exceptions and print them to StdErr without interrupting."""
    _stderr = sys.stderr

    def __init__(self):
        pass

    def write(self, data):
        STDERR.error(data)
class SpotCAMMediaStreamTrack(MediaStreamTrack):
    def __init__(self, track, queue):
        super().__init__()
        
        self.track = track
        self.queue = queue

    async def recv(self):
        frame = await self.track.recv()
        await self.queue.put(frame)
        
        return frame

class WebRTCClient:
    def __init__(self, hostname, sdp_port, sdp_filename, cam_ssl_cert, token, rtc_config):
        self.pc = RTCPeerConnection(configuration=rtc_config)
        
        self.video_frame_queue = asyncio.Queue()
        self.hostname = hostname
        self.token = token
        self.sdp_port = sdp_port
        self.sdp_filename = sdp_filename
        self.cam_ssl_cert = cam_ssl_cert
        self.sink_task = None

    def get_bearer_token(self, mock=False):
        if mock:
            return 'token'
        return self.token

    def get_sdp_offer_from_spot_cam(self, token):
        # then made the sdp request with the token
        headers = {'Authorization': f'Bearer {token}'}
        server_url = f'https://{self.hostname}:{self.sdp_port}/{self.sdp_filename}'
        response = requests.get(server_url, verify=self.cam_ssl_cert, headers=headers, 
                                timeout=DEFAULT_WEB_REQUEST_TIMEOUT)
        result = response.json()
        return result['id'], base64.b64decode(result['sdp']).decode()

    def send_sdp_answer_to_spot_cam(self, token, offer_id, sdp_answer):
        headers = {'Authorization': f'Bearer {token}'}
        server_url = f'https://{self.hostname}:{self.sdp_port}/{self.sdp_filename}'
        payload = {'id': offer_id, 'sdp': base64.b64encode(sdp_answer).decode('utf8')}
        r = requests.post(server_url, verify=self.cam_ssl_cert, json=payload, headers=headers, 
                        timeout=DEFAULT_WEB_REQUEST_TIMEOUT)
        if r.status_code != 200:
            raise ValueError(r)

    async def start(self):
        # first get a token
        try:
            token = self.get_bearer_token()
        except:
            token = self.get_bearer_token(mock=True)
            
        offer_id, sdp_offer = self.get_sdp_offer_from_spot_cam(token)
            
        @self.pc.on('icegatheringstatechange')
        def _on_ice_gathering_state_change():
            print(f'ICE gathering state changed to {self.pc.iceGatheringState}')

        @self.pc.on('signalingstatechange')
        def _on_signaling_state_change():
            print(f'Signaling state changed to: {self.pc.signalingState}')

        @self.pc.on('icecandidate')
        def _on_ice_candidate(event):
            print(f'Received candidate: {event.candidate}')

        @self.pc.on('iceconnectionstatechange')
        async def _on_ice_connection_state_change():
            print(f'ICE connection state changed to: {self.pc.iceConnectionState}')

            if self.pc.iceConnectionState == 'checking':
                self.send_sdp_answer_to_spot_cam(token, offer_id,
                                                self.pc.localDescription.sdp.encode())
                
        # @self.pc.on('track')
        # def on_track(track):
        #     print(f'Received track: {track.kind}')
        #     #elimine medio parrafo aqui, si hay error verificar aqui
        #     if track.kind == 'video':
        #         video_track = SpotCAMMediaStreamTrack(track, self.video_frame_queue)   
        #         # video_track.kind = 'video'
        #         # self.pc.addTrack(video_track)     ????????????????????????????????????????????????? #revisar

        desc = RTCSessionDescription(sdp_offer, 'offer')
        await self.pc.setRemoteDescription(desc)
        
        sdp_answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(sdp_answer)
        
# # WebRTC must be in its own thread with its own event loop.
# async def record_webrtc(options, token, recorder):
#     config = RTCConfiguration(iceServers=[])
#     client = Camera_1_1.WebRTCClient(options.hostname, options.sdp_port, options.sdp_filename,
#                         options.cam_ssl_cert, token, config)
#     await client.start()

#     # wait for connection to be established before recording
#     while client.pc.iceConnectionState != 'completed':
#         await asyncio.sleep(0.1)

#     # start recording
#     await recorder.start()
#     try:
#         await asyncio.sleep(options.time)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         # close everything
#         await client.pc.close()
#         await recorder.stop()

# Frame processing occurs; otherwise it waits.
async def process_frame(client, options, shutdown_flag):
    count = 0
    while not shutdown_flag.is_set():
        try:
            frame = await client.video_frame_queue.get()
            frame.to_image().save(f'{options.dst_prefix}-{count}.jpg')
            count += 1
            if count >= options.count:
                break
        except Exception as e:
            print(e)

    shutdown_flag.set()
    
# processing to occur.
async def monitor_shutdown(shutdown_flag, client):
    while not shutdown_flag.is_set():
        await asyncio.sleep(1.0)

    await client.pc.close()
    asyncio.get_event_loop().stop()
    

# WebRTC must be in its own thread with its own event loop.
def start_webrtc(shutdown_flag, options, token, process_func, recorder=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = RTCConfiguration(iceServers=[])
    client = WebRTCClient(options.hostname, options.sdp_port, options.sdp_filename,
                        options.cam_ssl_cert, token, config)

    asyncio.gather(client.start(), process_func(client, options, shutdown_flag),
                monitor_shutdown(shutdown_flag, client))
    loop.run_forever()

class Options:
    def __init__ (self, hostname, sdp_port, sdp_filename, cam_ssl_cert, time, count, dst_prefix):
        self.hostname = hostname
        self.sdp_port = sdp_port
        self.sdp_filename = sdp_filename
        self.cam_ssl_cert = cam_ssl_cert
        self.time = time
        self.count = count
        self.dst_prefix = dst_prefix
        
if __name__ == "__main__":

    options = Options(
        hostname='192.168.80.3',
        sdp_port=443,
        sdp_filename='api/v1/robot/video/frontleft/webrtc', #cruzar dedos
        cam_ssl_cert='',
        time=10,
        count=50,
        dst_prefix='frame'
    )
    shutdown_flag = threading.Event()
    # sdk = bosdyn.client.create_standard_sdk('WebRTCClient')
    # robot = sdk.create_robot(options.hostname)
    
    # guid, secret = get_guid_and_secret(options)
    # robot.authenticate(guid, secret)
    
    # auth_client = robot.ensure_client(AuthClient.default_service_name)
    # token = auth_client.get_auth_token().token
    ##Descomentar como intento de hacer que funcione (por problemas con el token)
    
    start_webrtc(shutdown_flag, options)    #Token

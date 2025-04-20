import asyncio
import base64
import requests
import threading
import cv2
import numpy as np
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCConfiguration
from aiortc.contrib.media import MediaBlackhole


DEFAULT_WEB_REQUEST_TIMEOUT = 10.0

class Camera_1_1:
    
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
                    
            @self.pc.on('track')
            def on_track(track):
                print(f'Received track: {track.kind}')
                #elimine medio parrafo aqui, si hay error verificar aqui
                if track.kind == 'video':
                    video_track = Camera_1_1.SpotCAMMediaStreamTrack(track, self.video_frame_queue)     #hay que ser inteligentes
                    # video_track.kind = 'video'
                    # self.pc.addTrack(video_track)     ????????????????????????????????????????????????? #revisar

            desc = RTCSessionDescription(sdp_offer, 'offer')
            await self.pc.setRemoteDescription(desc)
            
            sdp_answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(sdp_answer)
            
    # WebRTC must be in its own thread with its own event loop.
    async def record_webrtc(options, token, recorder):
        config = RTCConfiguration(iceServers=[])
        client = Camera_1_1.WebRTCClient(options.hostname, options.sdp_port, options.sdp_filename,
                            options.cam_ssl_cert, token, config)
        await client.start()

        # wait for connection to be established before recording
        while client.pc.iceConnectionState != 'completed':
            await asyncio.sleep(0.1)

        # start recording
        await recorder.start()
        try:
            await asyncio.sleep(options.time)
        except KeyboardInterrupt:
            pass
        finally:
            # close everything
            await client.pc.close()
            await recorder.stop()


    # WebRTC must be in its own thread with its own event loop.
    def start_webrtc(shutdown_flag, options, token, process_func, recorder=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        config = RTCConfiguration(iceServers=[])
        client = Camera_1_1.WebRTCClient(options.hostname, options.sdp_port, options.sdp_filename,
                            options.cam_ssl_cert, token, config)

        asyncio.gather(client.start(), process_func(client, options, shutdown_flag),
                    Camera_1_1.monitor_shutdown(shutdown_flag, client))
        loop.run_forever()


    # Frame processing occurs; otherwise it waits.
    async def process_frame(client, options, shutdown_flag):
        count = 0
        while asyncio.get_event_loop().is_running():
            try:
                frame = await client.video_frame_queue.get()
                frame.to_image().save(f'{options.dst_prefix}-{count}.jpg')
                count += 1
                if count >= options.count:
                    break
            except Exception as e:
                print(e)
            
        shutdown_flag.set()


    # Flag must be monitored in a different coroutine and sleep to allow frame
    # processing to occur.
    async def monitor_shutdown(shutdown_flag, client):
        while not shutdown_flag.is_set():
            await asyncio.sleep(1.0)

        await client.pc.close()
        asyncio.get_event_loop().stop()
        
        
if __name__ == "__main__":
    application = Camera_1_1()
    
    options = Camera_1_1.Options(
        hostname='192.168.80.3',
        sdp_port=443,
        sdp_filename='api/v1/robot/video/frontleft/webrtc', #cruzar dedos
        cam_ssl_cert='/path/to/cert.pem',
        time=10,
        count=50,
        dst_prefix='frame'
    )



import asyncio                                                                       # puede ejecutar varias tareas al mismo tiempo
import base64                                                                        # convierte datos en un formato seguro y entendible para los sistemas
import requests                                                                      # permite hacer peticiones HTTP                                       
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription        # una biblioteca para la comunicación web en tiempo real (WebRTC) y la comunicación de objetos en tiempo real (ORTC)
from aiortc.contrib.media import MediaBlackhole                                      # proporciona clases para manipular flujos de medios, como leer y grabar audio y video

DEFAULT_WEB_REQUEST_TIMEOUT = 10.0                                                  


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

    def __init__(self, hostname, sdp_port, sdp_filename, cam_ssl_cert, token, rtc_config,
                 media_recorder=None, recorder_type=None): #no se va a grabar nada
        self.pc = RTCPeerConnection(configuration=rtc_config)

        self.video_frame_queue = asyncio.Queue()
        self.audio_frame_queue = asyncio.Queue() #audio es muy complicado

        self.hostname = hostname
        self.token = token
        self.sdp_port = sdp_port
        self.media_recorder = media_recorder    #no vamos a grabar
        self.media_black_hole = None #deprecado (para mi)
        self.recorder_type = recorder_type #tampoco
        self.sdp_filename = sdp_filename #no vamos a guardar nada
        self.cam_ssl_cert = cam_ssl_cert    #se ve importante
        self.sink_task = None   #si

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
        def _on_track(track):
            print(f'Received track: {track.kind}')

            if self.media_recorder: #no vamos a grabar
                if track.kind == self.recorder_type:
                    self.media_recorder.addTrack(track)
                else:
                    # We only care about the track we are recording.
                    self.media_black_hole = MediaBlackhole()    #ya elimiamos esto, asi que no se si es necesario
                    self.media_black_hole.addTrack(track)
                    loop = asyncio.get_event_loop()
                    self.sink_task = loop.create_task(self.media_black_hole.start())
            else:
                if track.kind == 'video':
                    video_track = SpotCAMMediaStreamTrack(track, self.video_frame_queue)
                    video_track.kind = 'video'
                    self.pc.addTrack(video_track)

                if track.kind == 'audio':   #no audio
                    self.media_recorder = MediaBlackhole()
                    self.media_recorder.addTrack(track)
                    loop = asyncio.get_event_loop()
                    self.sink_task = loop.create_task(self.media_recorder.start())

        desc = RTCSessionDescription(sdp_offer, 'offer')
        await self.pc.setRemoteDescription(desc)

        sdp_answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(sdp_answer)
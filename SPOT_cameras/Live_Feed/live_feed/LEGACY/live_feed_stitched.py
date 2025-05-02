# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""Simple image display example."""

import argparse
import logging
import sys
import time

import cv2
import numpy as np
from scipy import ndimage

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request
from bosdyn.client.time_sync import TimedOutError

# SDL: From stich together
import io
import os
from PIL import Image
from contextlib import contextmanager
from ctypes import *
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, get_a_tform_b, get_vision_tform_body
import OpenGL
from OpenGL.GL import *
from OpenGL.GL import GL_VERTEX_SHADER, shaders
from OpenGL.GLU import *

_LOGGER = logging.getLogger(__name__)

VALUE_FOR_Q_KEYSTROKE = 113
VALUE_FOR_ESC_KEYSTROKE = 27

ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -78,
    'frontright_fisheye_image': -102,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180
}

### SDL
COMBINED_WINDOW_NAME = "Front"

### SDL: Incorporated from get_image.py example
def pixel_format_type_strings():
    names = image_pb2.Image.PixelFormat.keys()
    return names[1:]

### SDL: Incorporated from get_image.py example
def pixel_format_string_to_enum(enum_string):
    return dict(image_pb2.Image.PixelFormat.items()).get(enum_string)

### SDL: Incorporated from stitch_front_images.py example
class StitchingCamera(object):
    """Camera to render from in OpenGL."""

    def __init__(self, image_1, image_2):
        """We assume the two images passed in are Front Right and Front Left,
        we put our fake OpenGl rendering camera smack dab in the middle of the
        two"""
        super(StitchingCamera, self).__init__()

        rect_stitching_distance_meters = 2.0

        vo_T_body = image_1.vision_T_body.to_matrix()

        eye_wrt_body = proto_vec_T_numpy(image_1.body_T_image_sensor.position) \
                     + proto_vec_T_numpy(image_2.body_T_image_sensor.position)

        # Add the two real camera norms together to get the fake camera norm.
        eye_norm_wrt_body = numpy.array(image_1.body_T_image_sensor.rot.transform_point(0, 0, 1)) \
                          + numpy.array(image_2.body_T_image_sensor.rot.transform_point(0, 0, 1))

        # Make the virtual camera centered.
        eye_wrt_body[1] = 0
        eye_norm_wrt_body[1] = 0

        # Make sure our normal has length 1
        eye_norm_wrt_body = normalize(eye_norm_wrt_body)

        plane_wrt_body = eye_wrt_body + eye_norm_wrt_body * rect_stitching_distance_meters

        self.plane_wrt_vo = mat4mul3(vo_T_body, plane_wrt_body)
        self.plane_norm_wrt_vo = mat4mul3(vo_T_body, eye_norm_wrt_body, 0)

        self.eye_wrt_vo = mat4mul3(vo_T_body, eye_wrt_body)
        self.up_wrt_vo = mat4mul3(vo_T_body, numpy.array([0, 0, 1]), 0)

### SDL: Incorporated from stitch_front_images.py
class CompiledShader():
    """OpenGL shader compile"""

    def __init__(self, vert_shader, frag_shader):
        self.program = shaders.compileProgram( \
            shaders.compileShader(vert_shader, GL_VERTEX_SHADER), \
            shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER) \
        )
        self.camera1_MVP = glGetUniformLocation(self.program, 'camera1_MVP')
        self.camera2_MVP = glGetUniformLocation(self.program, 'camera2_MVP')

        self.image1_texture = glGetUniformLocation(self.program, 'image1')
        self.image2_texture = glGetUniformLocation(self.program, 'image2')

        self.initialized = False
        self.image1 = None
        self.image2 = None
        self.matrix1 = None
        self.matrix2 = None

    def update_images(self, image_1, image_2):
        self.initialized = True
        self.matrix1 = image_1.MVP
        self.matrix2 = image_2.MVP
        if self.image1 is None:
            self.image1 = ImageInsideOpenGL(image_1.image)
        else:
            self.image1.update(image_1.image)
        if self.image2 is None:
            self.image2 = ImageInsideOpenGL(image_2.image)
        else:
            self.image2.update(image_2.image)


def load_get_image_response_from_binary_file(file_path):
    """Read in image from image response"""
    if not os.path.exists(file_path):
        raise IOError(f'File not found at: {file_path}')

    _images = image_pb2.GetImageResponse()
    with open(file_path, 'rb') as f:
        data = f.read()
        _images.ParseFromString(data)

    return _images


def proto_vec_T_numpy(vec):
    return numpy.array([vec.x, vec.y, vec.z])


def mat4mul3(mat, vec, vec4=1):
    ret = numpy.matmul(mat, numpy.append(vec, vec4))
    return ret[:-1]


def normalize(vec):
    norm = numpy.linalg.norm(vec)
    if norm == 0:
        raise ValueError('norm function returned 0.')
    return vec / norm


def draw_geometry(plane_wrt_vo, plane_norm_wrt_vo, sz_meters):
    """Draw as GL_TRIANGLES."""
    plane_left_wrt_vo = normalize(numpy.cross(numpy.array([0, 0, 1]), plane_norm_wrt_vo))
    if plane_left_wrt_vo is None:
        return
    plane_up_wrt_vo = normalize(numpy.cross(plane_norm_wrt_vo, plane_left_wrt_vo))
    if plane_up_wrt_vo is None:
        return

    plane_up_wrt_vo = plane_up_wrt_vo * sz_meters
    plane_left_wrt_vo = plane_left_wrt_vo * sz_meters

    vertices = (
        plane_wrt_vo + plane_left_wrt_vo - plane_up_wrt_vo,
        plane_wrt_vo + plane_left_wrt_vo + plane_up_wrt_vo,
        plane_wrt_vo - plane_left_wrt_vo + plane_up_wrt_vo,
        plane_wrt_vo - plane_left_wrt_vo - plane_up_wrt_vo,
    )

    indices = (0, 1, 2, 0, 2, 3)

    glBegin(GL_TRIANGLES)
    for index in indices:
        glVertex3fv(vertices[index])
    glEnd()

### SDL: Incorporated from stitch_front_images.py
class ImagePreppedForOpenGL():
    """Prep image for OpenGL from Spot image_response."""

    def extract_image(self, image_response):
        """Return numpy_array of input image_response image."""
        image_format = image_response.shot.image.format

        if image_format == image_pb2.Image.FORMAT_RAW:
            raise Exception('Won\'t work.  Yet.')
        elif image_format == image_pb2.Image.FORMAT_JPEG:
            numpy_array = np.asarray(Image.open(io.BytesIO(image_response.shot.image.data)))
        else:
            raise Exception('Won\'t work.')

        return numpy_array

    def __init__(self, image_response):
        self.image = self.extract_image(image_response)
        self.body_T_image_sensor = get_a_tform_b(image_response.shot.transforms_snapshot, \
             BODY_FRAME_NAME, image_response.shot.frame_name_image_sensor)
        self.vision_T_body = get_vision_tform_body(image_response.shot.transforms_snapshot)
        if not self.body_T_image_sensor:
            raise Exception('Won\'t work.')

        if image_response.source.pinhole:
            resolution = np.asarray([ \
                image_response.source.cols, \
                image_response.source.rows])

            focal_length = np.asarray([ \
                image_response.source.pinhole.intrinsics.focal_length.x, \
                image_response.source.pinhole.intrinsics.focal_length.y])

            principal_point = np.asarray([ \
                image_response.source.pinhole.intrinsics.principal_point.x, \
                image_response.source.pinhole.intrinsics.principal_point.y])
        else:
            raise Exception('Won\'t work.')

        sensor_T_vo = (self.vision_T_body * self.body_T_image_sensor).inverse()

        camera_projection_mat = np.eye(4)
        camera_projection_mat[0, 0] = (focal_length[0] / resolution[0])
        camera_projection_mat[0, 2] = (principal_point[0] / resolution[0])
        camera_projection_mat[1, 1] = (focal_length[1] / resolution[1])
        camera_projection_mat[1, 2] = (principal_point[1] / resolution[1])

        self.MVP = camera_projection_mat.dot(sensor_T_vo.to_matrix())

def image_to_opencv(image, auto_rotate=True):
    """Convert an image proto message to an openCV image."""
    num_channels = 1  # Assume a default of 1 byte encodings.
    if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
        dtype = np.uint16
        extension = '.png'
    else:
        dtype = np.uint8
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
            num_channels = 3
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
            num_channels = 4
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            num_channels = 1
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16:
            num_channels = 1
            dtype = np.uint16
        extension = '.jpg'

    img = np.frombuffer(image.shot.image.data, dtype=dtype)
    if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into a RGB rows X cols shape.
            img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_channels))
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    if auto_rotate:
        img = ndimage.rotate(img, ROTATION_ANGLE[image.source.name])

    return img, extension


def reset_image_client(robot):
    """Recreate the ImageClient from the robot object."""
    del robot.service_clients_by_name['image']
    del robot.channels_by_authority['api.spot.robot']
    return robot.ensure_client('image')


def main(argv):
    # Parse args
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('--image-sources', help='Get image from source(s)', action='append')
    parser.add_argument('--image-service', help='Name of the image service to query.',
                        default=ImageClient.default_service_name)
    parser.add_argument( ### SDL: Incorporated from get_image.py example
        '--pixel-format', choices=pixel_format_type_strings(),
        help='Requested pixel format of image. If supplied, will be used for all sources.')
    parser.add_argument('-j', '--jpeg-quality-percent', help='JPEG quality percentage (0-100)',
                        type=int, default=50)
    parser.add_argument('-c', '--capture-delay', help='Time [ms] to wait before the next capture',
                        type=int, default=100)
    parser.add_argument('-r', '--resize-ratio', help='Fraction to resize the image', type=float,
                        default=1)
    parser.add_argument(
        '--disable-full-screen',
        help='A single image source gets displayed full screen by default. This flag disables that.',
        action='store_true')
    parser.add_argument('--auto-rotate', help='rotate right and front images to be upright',
                        action='store_true')
    options = parser.parse_args(argv)

    ### SDL: Added
    both_front_cameras_desired = ("frontleft_fisheye_image" in options.image_sources) and ("frontright_fisheye_image" in options.image_sources)

    # Create robot object with an image client.
    sdk = bosdyn.client.create_standard_sdk('image_capture')
    robot = sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()

    ### SDL: Load shaders. Incorporated from stitch_front_images.py
    with open('shader_vert.glsl', 'r') as file:
        vert_shader = file.read()
    with open('shader_frag.glsl', 'r') as file:
        frag_shader = file.read()
    program = CompiledShader(vert_shader, frag_shader)

    image_client = robot.ensure_client(options.image_service)
    pixel_format = pixel_format_string_to_enum(options.pixel_format)
    requests = [
        build_image_request(source, quality_percent=options.jpeg_quality_percent,
                            pixel_format=pixel_format, ### SDL: Incorporated from get_image.py example
                            resize_ratio=options.resize_ratio) for source in options.image_sources
    ]

    ### SDL: If both exist, create only one window for both of them
    if both_front_cameras_desired:
        cv2.namedWindow(COMBINED_WINDOW_NAME, cv2.WINDOW_NORMAL)
        ### SDL: Copied from below
        if len(options.image_sources) > 1 or options.disable_full_screen:
            cv2.setWindowProperty(COMBINED_WINDOW_NAME, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        else:
            cv2.setWindowProperty(COMBINED_WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    for image_source in options.image_sources:
        if both_front_cameras_desired and (image_source == "frontleft_fisheye_image" or image_source == "frontright_fisheye_image"): ### SDL: Already accounted for
            continue
        cv2.namedWindow(image_source, cv2.WINDOW_NORMAL)
        if len(options.image_sources) > 1 or options.disable_full_screen:
            cv2.setWindowProperty(image_source, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        else:
            cv2.setWindowProperty(image_source, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    keystroke = None
    timeout_count_before_reset = 0
    t1 = time.time()
    image_count = 0

    while keystroke != VALUE_FOR_Q_KEYSTROKE and keystroke != VALUE_FOR_ESC_KEYSTROKE:
        try:
            images_future = image_client.get_image_async(requests, timeout=0.5)
            while not images_future.done():
                keystroke = cv2.waitKey(25)
                print(keystroke)
                if keystroke == VALUE_FOR_ESC_KEYSTROKE or keystroke == VALUE_FOR_Q_KEYSTROKE:
                    sys.exit(1)
            images = images_future.result()
        except TimedOutError as time_err:
            if timeout_count_before_reset == 5:
                # To attempt to handle bad comms and continue the live image stream, try recreating the
                # image client after having an RPC timeout 5 times.
                _LOGGER.info('Resetting image client after 5+ timeout errors.')
                image_client = reset_image_client(robot)
                timeout_count_before_reset = 0
            else:
                timeout_count_before_reset += 1
        except Exception as err:
            _LOGGER.warning(err)
            continue
        ### SDL: If both front cameras are wanted, pull em out the list and handle seperately
        if both_front_cameras_desired:
            front_left = None
            front_right = None
            for i in range(len(images) - 1, -1, -1): # Traverse thru backwards so can easily remove elements
                if images[i].source.name == "frontleft_fisheye_image":
                    front_left = images[i]
                    images.pop(i)
                    continue
                elif images[i].source.name == "frontright_fisheye_image":
                    front_right = images[i]
                    images.pop(i)
                    continue
            ### SDL: TODO error check front images both found
            front_left_cv2, extension = image_to_opencv(front_left, options.auto_rotate) ### SDL: Before, extensions was not included.
            front_right_cv2, extension = image_to_opencv(front_right, options.auto_rotate) ### SDL: Before, extensions was not included.
            front_left_opengl = ImagePreppedForOpenGL(front_left)
            front_right_opengl = ImagePreppedForOpenGL(front_right)
            #front_left_opengl.image = front_left_cv2 # SDL: Replace original image with color one
            #front_right_opengl.image = front_right_cv2 # SDL: Replace original image with color one
            #program.update_images(front_right_opengl, front_left_opengl)
            #stitching_camera = StitchingCamera(front_right, front_left)
            ### SDL: The opengl.image is the same as cv2, just with color it appears.
            #Image.fromarray(front_left_cv2).save("cv_test1.png")
            #Image.fromarray(front_left_opengl.image).save("gl_test1.png")
            #front_left_cv2.save("cv_test1.png")
            #front_left_opengl.save("gl_test1.png")
            #cv2.imshow(COMBINED_WINDOW_NAME, front_left_image)

        print(len(images))
        for i in range(len(images)):
            #image, _ = image_to_opencv(images[i], options.auto_rotate) 
            image, extension = image_to_opencv(images[i], options.auto_rotate) ### SDL: Before, extensions was not included.
            cv2.imshow(images[i].source.name, image)

        keystroke = cv2.waitKey(options.capture_delay)
        image_count += 1
        print(f'Mean image retrieval rate: {image_count/(time.time() - t1)}Hz')


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)

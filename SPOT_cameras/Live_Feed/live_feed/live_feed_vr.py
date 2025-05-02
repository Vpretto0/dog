"""
pyopenxr example program color_cube.py
This example renders one big cube.
"""

'''
# ContextObject is a high level pythonic class meant to keep simple cases simple.
with xr.ContextObject(
    instance_create_info=xr.InstanceCreateInfo(
        enabled_extension_names=[
            # A graphics extension is mandatory (without a headless extension)
            xr.KHR_OPENGL_ENABLE_EXTENSION_NAME,
        ],
    ),
) as context:
    vertex_shader = compileShader(
        inspect.cleandoc("""
        #version 430
        
        // Adapted from @jherico's RiftDemo.py in pyovr
        
        /*  Draws a cube:
        
           2________ 3
           /|      /|
         6/_|____7/ |
          | |_____|_| 
          | /0    | /1
          |/______|/
          4       5          

         */

        layout(location = 0) uniform mat4 Projection = mat4(1);
        layout(location = 4) uniform mat4 ModelView = mat4(1);
        layout(location = 8) uniform float Size = 0.3;

        // Minimum Y value is zero, so cube sits on the floor in room scale
        const vec3 UNIT_CUBE[8] = vec3[8](
          vec3(-1.0, -0.0, -1.0), // 0: lower left rear
          vec3(+1.0, -0.0, -1.0), // 1: lower right rear
          vec3(-1.0, +2.0, -1.0), // 2: upper left rear
          vec3(+1.0, +2.0, -1.0), // 3: upper right rear
          vec3(-1.0, -0.0, +1.0), // 4: lower left front
          vec3(+1.0, -0.0, +1.0), // 5: lower right front
          vec3(-1.0, +2.0, +1.0), // 6: upper left front
          vec3(+1.0, +2.0, +1.0)  // 7: upper right front
        );

        const vec3 UNIT_CUBE_NORMALS[6] = vec3[6](
          vec3(0.0, 0.0, -1.0),
          vec3(0.0, 0.0, 1.0),
          vec3(1.0, 0.0, 0.0),
          vec3(-1.0, 0.0, 0.0),
          vec3(0.0, 1.0, 0.0),
          vec3(0.0, -1.0, 0.0)
        );

        const int CUBE_INDICES[36] = int[36](
          0, 1, 2, 2, 1, 3, // rear
          4, 6, 5, 6, 7, 5, // front
          0, 2, 4, 4, 2, 6, // left
          1, 3, 5, 5, 3, 7, // right
          2, 6, 3, 6, 3, 7, // top
          0, 1, 4, 4, 1, 5  // bottom
        );

        out vec3 _color;

        void main() {
          _color = vec3(1.0, 0.0, 0.0);
          int vertexIndex = CUBE_INDICES[gl_VertexID];
          int normalIndex = gl_VertexID / 6;

          _color = UNIT_CUBE_NORMALS[normalIndex];
          if (any(lessThan(_color, vec3(0.0)))) {
              _color = vec3(1.0) + _color;
          }

          gl_Position = Projection * ModelView * vec4(UNIT_CUBE[vertexIndex] * Size, 1.0);
        }
        """), GL.GL_VERTEX_SHADER)
    fragment_shader = compileShader(
        inspect.cleandoc("""
        #version 430
        
        in vec3 _color;
        out vec4 FragColor;

        void main() {
          FragColor = vec4(_color, 1.0);
        }
        """), GL.GL_FRAGMENT_SHADER)
    shader = compileProgram(vertex_shader, fragment_shader)
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glClearColor(0.2, 0.2, 0.2, 1)
    GL.glClearDepth(1.0)
    for frame_index, frame_state in enumerate(context.frame_loop()):
        for view_index, view in enumerate(context.view_loop(frame_state)):
            if view_index == 1:
                # continue
                pass
            # print(view_index, view.pose.position)  # Are both eyes the same?
            projection = xr.Matrix4x4f.create_projection_fov(
                graphics_api=xr.GraphicsAPI.OPENGL,
                fov=view.fov,
                near_z=0.05,
                far_z=100.0,  # tip: use negative far_z for infinity projection...
            )
            to_view = xr.Matrix4x4f.create_translation_rotation_scale(
                translation=view.pose.position,
                rotation=view.pose.orientation,
                scale=(1, 1, 1),
            )
            view = xr.Matrix4x4f.invert_rigid_body(to_view)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            GL.glUseProgram(shader)
            GL.glUniformMatrix4fv(0, 1, False, projection.as_numpy())
            GL.glUniformMatrix4fv(4, 1, False, view.as_numpy())
            GL.glBindVertexArray(vao)
            #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        # if frame_index > 3: break
'''

# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""Stitch frontleft_fisheye_image, frontright_fisheye_image from Image Service."""

import io
import os
import sys
from contextlib import contextmanager
from ctypes import *

import numpy
import OpenGL
import pygame
from OpenGL.GL import *
from OpenGL.GL import GL_VERTEX_SHADER, shaders
from OpenGL.GLU import *
from PIL import Image
from pygame.locals import *

import bosdyn.api
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.frame_helpers import BODY_FRAME_NAME, get_a_tform_b, get_vision_tform_body
from bosdyn.client.image import ImageClient, build_image_request

### SDL: Imported from image_viewer.py
import cv2
from scipy import ndimage

# Pyopenxr example
import inspect
#from OpenGL import GL
#from OpenGL.GL.shaders import compileShader, compileProgram
import xr

### SDL
color_requested = False
gl_pixel_format = GL_LUMINANCE ### SDL: GL_LUMINANCE = one byte (grayscale), GL_RGB = three byte (color)

### SDL - Constants
DISPLAY_TICK_HZ = 60 # 60 was original value


### SDL: Imported from image_viewer.py
def image_to_opencv(image, auto_rotate=True):
    """Convert an image proto message to an openCV image."""
    num_channels = 1  # Assume a default of 1 byte encodings.
    if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
        dtype = numpy.uint16
        extension = '.png'
    else:
        dtype = numpy.uint8
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
            num_channels = 3
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
            num_channels = 4
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            num_channels = 1
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16:
            num_channels = 1
            dtype = numpy.uint16
        extension = '.jpg'

    img = numpy.frombuffer(image.shot.image.data, dtype=dtype)
    if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into a RGB rows X cols shape.
            img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_channels))
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    # if auto_rotate:
    #     img = ndimage.rotate(img, ROTATION_ANGLE[image.source.name])

    #return img, extension
    return img ### SDL: Don't need extension

### SDL: Incorporated from get_image.py example
def pixel_format_type_strings():
    names = image_pb2.Image.PixelFormat.keys()
    return names[1:]

class ImagePreppedForOpenGL():
    """Prep image for OpenGL from Spot image_response."""

    def extract_image(self, image_response):
        """Return numpy_array of input image_response image."""
        image_format = image_response.shot.image.format

        if image_format == image_pb2.Image.FORMAT_RAW:
            raise Exception('Won\'t work.  Yet.')
        elif image_format == image_pb2.Image.FORMAT_JPEG:
            if color_requested:
                numpy_array = numpy.asarray(Image.open(io.BytesIO(image_response.shot.image.data)))[:, :, 0]
            else:
                numpy_array = numpy.asarray(Image.open(io.BytesIO(image_response.shot.image.data)))
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
            resolution = numpy.asarray([ \
                image_response.source.cols, \
                image_response.source.rows])

            focal_length = numpy.asarray([ \
                image_response.source.pinhole.intrinsics.focal_length.x, \
                image_response.source.pinhole.intrinsics.focal_length.y])

            principal_point = numpy.asarray([ \
                image_response.source.pinhole.intrinsics.principal_point.x, \
                image_response.source.pinhole.intrinsics.principal_point.y])
        else:
            raise Exception('Won\'t work.')

        sensor_T_vo = (self.vision_T_body * self.body_T_image_sensor).inverse()

        camera_projection_mat = numpy.eye(4)
        camera_projection_mat[0, 0] = (focal_length[0] / resolution[0])
        camera_projection_mat[0, 2] = (principal_point[0] / resolution[0])
        camera_projection_mat[1, 1] = (focal_length[1] / resolution[1])
        camera_projection_mat[1, 2] = (principal_point[1] / resolution[1])

        self.MVP = camera_projection_mat.dot(sensor_T_vo.to_matrix())

    ### SDL
    def update_image_with_color_image(self, color_image):
        self.image = color_image


class ImageInsideOpenGL():
    """Create OpenGL Texture"""

    def __init__(self, numpy_array):
        glEnable(GL_TEXTURE_2D)
        self.pointer = glGenTextures(1)
        with self.manage_bind():
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, numpy_array.shape[1], numpy_array.shape[0], 0, \
                #GL_LUMINANCE, GL_UNSIGNED_BYTE, numpy_array)
                #GL_RGB, GL_UNSIGNED_BYTE, numpy_array) ### SDL
                gl_pixel_format, GL_UNSIGNED_BYTE, numpy_array) ### SDL
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    @contextmanager
    def manage_bind(self):
        glBindTexture(GL_TEXTURE_2D, self.pointer)  # bind image
        try:
            yield
        finally:
            glBindTexture(GL_TEXTURE_2D, 0)  # unbind image

    def update(self, numpy_array):
        """Update texture"""
        with self.manage_bind():
            glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, numpy_array.shape[1], numpy_array.shape[0], \
                #GL_LUMINANCE, GL_UNSIGNED_BYTE, numpy_array)
                #GL_RGB, GL_UNSIGNED_BYTE, numpy_array) ### SDL
                gl_pixel_format, GL_UNSIGNED_BYTE, numpy_array) ### SDL


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


def get_geometry(plane_wrt_vo, plane_norm_wrt_vo, sz_meters):
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

    return vertices, indices
    '''
    glBegin(GL_TRIANGLES)
    for index in indices:
        glVertex3fv(vertices[index])
    glEnd()
    '''


def draw_routine(display, program, stitching_camera):
    """OpenGL Draw"""

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(110, (display[0] / display[1]), 0.1, 50.0)

    if not program.initialized:
        print('Gl is not ready yet.')
        return
    if stitching_camera is None:
        print('No stitching camera yet.')
        return

    glUseProgram(program.program)

    glActiveTexture(GL_TEXTURE0 + 0)
    with program.image1.manage_bind():
        glUniform1i(program.image1_texture, 0)
        glActiveTexture(GL_TEXTURE0 + 1)

        with program.image2.manage_bind():

            glUniform1i(program.image2_texture, 1)

            glUniformMatrix4fv(program.camera1_MVP, 1, GL_TRUE, program.matrix1)
            glUniformMatrix4fv(program.camera2_MVP, 1, GL_TRUE, program.matrix2)

            plane_wrt_vo = stitching_camera.plane_wrt_vo
            plane_norm_wrt_vo = stitching_camera.plane_norm_wrt_vo
            eye_wrt_vo = stitching_camera.eye_wrt_vo
            up_wrt_vo = stitching_camera.up_wrt_vo

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(eye_wrt_vo[0], eye_wrt_vo[1], eye_wrt_vo[2], \
                      plane_wrt_vo[0], plane_wrt_vo[1], plane_wrt_vo[2], \
                      up_wrt_vo[0], up_wrt_vo[1], up_wrt_vo[2])

            rect_sz_meters = 7
            return get_geometry(plane_wrt_vo, plane_norm_wrt_vo, rect_sz_meters)


def stitch(robot, options):
    #display = (1080, 720)
    #pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




def main():
    """Top-level function to stitch together two Spot front camera images."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('-j', '--jpeg-quality-percent', help='JPEG quality percentage (0-100)',
                        type=int, default=50)
    parser.add_argument( ### SDL: Incorporated from get_image.py example
        '--pixel-format', choices=pixel_format_type_strings(),
        help='Requested pixel format of image. If supplied, will be used for all sources.')
    options = parser.parse_args()

    ### SDL: Only 8 bit greyscale and RGB supported right now
    assert (options.pixel_format == "PIXEL_FORMAT_RGB_U8") or (options.pixel_format == "PIXEL_FORMAT_GREYSCALE_U8"), "Only 8 bit greyscale or rgb supported right now. Please call using one of those as --pixel-format param"

    sdk = bosdyn.client.create_standard_sdk('front_cam_stitch') ### TODO CHANGE
    robot = sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()

    global color_requested ### SDL
    global gl_pixel_format ### SDL

    """Stitch two front fisheye images together"""
    #pygame.init()

    #display = (1080, 720)
    #pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    #clock = pygame.time.Clock()

    with open('shader_vert.glsl', 'r') as file:
        vert_shader = file.read()
    with open('shader_frag.glsl', 'r') as file:
        frag_shader = file.read()

    program = CompiledShader(vert_shader, frag_shader)

    image_client = robot.ensure_client(ImageClient.default_service_name)

    image_sources = ['frontright_fisheye_image', 'frontleft_fisheye_image']

    requests = [
        build_image_request(source,
            pixel_format=options.pixel_format, ### SDL: Incorporated from get_image.py example
            quality_percent=options.jpeg_quality_percent)
        for source in image_sources
    ]
    ### SDL
    if options.pixel_format == "PIXEL_FORMAT_RGB_U8":
        color_requested = True
        #gl_pixel_format = GL_RGB
        gl_pixel_format = GL_BGR ### SDL: Must be shared across both Open GL functions
    else:
        color_requested = False
        gl_pixel_format = GL_LUMINANCE
    #color_requested = options.pixel_format == "PIXEL_FORMAT_RGB_U8"

    running = True

    images_future = None
    stitching_camera = None

    # ContextObject is a high level pythonic class meant to keep simple cases simple.
    with xr.ContextObject(
        instance_create_info=xr.InstanceCreateInfo(
            enabled_extension_names=[
                # A graphics extension is mandatory (without a headless extension)
                xr.KHR_OPENGL_ENABLE_EXTENSION_NAME,
            ],
        ),
    ) as context:
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.2, 0.2, 0.2, 1)
        GL.glClearDepth(1.0)
        for frame_index, frame_state in enumerate(context.frame_loop()):
            
            if images_future is not None and images_future.done():
                try:
                    images = images_future.result()
                except Exception as exc:
                    print('Could not get images:', exc)
                else:
                    front_right_image = None ### SDL
                    front_left_image = None ### SDL
                    for image in images:
                        #print("img:",numpy.asarray(Image.open(io.BytesIO(image.shot.image.data))))
                        #print("shape",numpy.asarray(Image.open(io.BytesIO(image.shot.image.data))).shape)
                        if image.source.name == 'frontright_fisheye_image':
                            front_right_image = image ### SDL
                            front_right = ImagePreppedForOpenGL(image)
                        elif image.source.name == 'frontleft_fisheye_image':
                            front_left_image = image ### SDL
                            front_left = ImagePreppedForOpenGL(image)

                    if front_right is not None and front_left is not None:
                        if color_requested: ### SDL: Replace image with image derived from get_image.py
                            front_right.update_image_with_color_image(image_to_opencv(front_right_image))
                            front_left.update_image_with_color_image(image_to_opencv(front_left_image))
                        program.update_images(front_right, front_left)
                        stitching_camera = StitchingCamera(front_right, front_left)
                        #input()
                    else:
                        print('Got image response, but not with both images!')

                # Reset variable so we re-send next image request
                images_future = None

            if images_future is None:
                images_future = image_client.get_image_async(requests, timeout=5.0)

            #glClearColor(0, 0, 255, 0)
            #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            vertices, indices = draw_routine(display, program, stitching_camera) # TODO draw these geoms
            #pygame.display.flip() ### SDL: Commented out to remove flickering. 
            #clock.tick(60)
            #ms = clock.tick(DISPLAY_TICK_HZ)
            #print("tick:", ms)

            #https://pythonprogramming.net/adding-ground-pyopengl-tutorial/
            ground_vertices = (
                (-10,-0.1,50),
                (10,-0.1,50),
                (-10,-0.1,-300),
                (10,-0.1,-300),

                )
            glBegin(GL_QUADS)
            x = 0
            for vertex in ground_vertices:
            	x = x + 1
            	glColor3fv((0,1,1))
            	glVertex3fv(vertex)

            glEnd()


            for view_index, view in enumerate(context.view_loop(frame_state)):
                if view_index == 1:
                    # continue
                    pass
                # print(view_index, view.pose.position)  # Are both eyes the same?
                projection = xr.Matrix4x4f.create_projection_fov(
                    graphics_api=xr.GraphicsAPI.OPENGL,
                    fov=view.fov,
                    near_z=0.05,
                    far_z=100.0,  # tip: use negative far_z for infinity projection...
                )
                to_view = xr.Matrix4x4f.create_translation_rotation_scale(
                    translation=view.pose.position,
                    rotation=view.pose.orientation,
                    scale=(1, 1, 1),
                )
                view = xr.Matrix4x4f.invert_rigid_body(to_view)
                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                GL.glUniformMatrix4fv(0, 1, False, projection.as_numpy())
                GL.glUniformMatrix4fv(4, 1, False, view.as_numpy())
                GL.glBindVertexArray(vao)
                #GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
            if frame_index > 3: break

    #stitch(robot, options)

    return True


if __name__ == '__main__':
    main()

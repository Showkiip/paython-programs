import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Load a 3D dinosaur model (make sure to provide the correct path)
scene = pywavefront.Wavefront('dinosaur.obj', collect_faces=True)


def draw_model(model):
    for name, mesh in model.meshes.items():
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex in face:
                glVertex3fv(mesh.vertices[vertex])
        glEnd()


# Set the dinosaur's initial position
dino_pos = [0, -1, -5]


def move_dinosaur(keys):
    global dino_pos
    if keys[pygame.K_LEFT]:
        dino_pos[0] -= 0.1
    if keys[pygame.K_RIGHT]:
        dino_pos[0] += 0.1
    if keys[pygame.K_UP]:
        dino_pos[2] += 0.1
    if keys[pygame.K_DOWN]:
        dino_pos[2] -= 0.1


# Main program
def dinosaur_adventure():
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.0, -10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()  # Get user inputs
        move_dinosaur(keys)  # Move dinosaur based on inputs

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(dino_pos[0], dino_pos[1], dino_pos[2])
        draw_model(scene)  # Draw the dinosaur model
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


# Call the function
dinosaur_adventure()

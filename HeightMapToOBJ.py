import sys
import numpy as np
from PIL import Image
from noise import pnoise2


def generate_noise_map(width, height):
    noise_map = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_map[y][x] = pnoise2(x / 10, y / 10)
    return noise_map


def load_noise_map_from_image(image_path):
    image = Image.open(image_path).convert('L')
    noise_map = np.array(image) / 255.0  # Normalize the pixel values to the range [0, 1]
    return noise_map


def save_as_obj(vertices, faces, output_path):
    with open(output_path, 'w') as obj_file:
        for v in vertices:
            obj_file.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for f in faces:
            # Increment vertex indices by 1
            face1 = [v + 1 for v in f]
            obj_file.write(f"f {' '.join(map(str, face1))}\n")

def convert_noise_map_to_obj(noise_map, scale=1.0, exaggeration=10):
    height, width = noise_map.shape
    vertices = []
    faces = []
    for y in range(height):
        for x in range(width):
            vertex = [x * scale, y * scale, noise_map[y][x] * scale * exaggeration]
            vertices.append(vertex)

    # Generate faces for the plane
    for y in range(height - 1):
        for x in range(width - 1):
            v1 = y * width + x + 1
            v2 = (y + 1) * width + x + 1
            v3 = (y + 1) * width + x
            v4 = y * width + x
            face1 = [v1, v2, v3]
            face2 = [v3, v4, v1]
            faces.append(face1)
            faces.append(face2)

    return vertices, faces




def main():
    if len(sys.argv) > 1:
        # Command line argument provided, load noise map from the PNG file
        noise_map = load_noise_map_from_image(sys.argv[1])
    else:
        # No command line argument provided, generate noise map on the fly
        width, height = 8192, 8192  # Specify the size of the noise map
        noise_map = generate_noise_map(width, height)

    vertices, faces = convert_noise_map_to_obj(noise_map, 64)

    output_path = "output.obj"  # Specify the output OBJ file path
    save_as_obj(vertices, faces, output_path)
    print(f"OBJ file saved: {output_path}")


if __name__ == '__main__':
    main()

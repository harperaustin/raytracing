# Ray Tracing in Python

A simple ray tracing implementation in Python that renders 3D scenes composed of spheres with support for reflections, refractions, and various lighting models.

For our final project, we followed this tutorial https://medium.com/@www.seymour/coding-a-3d-ray-tracing-graphics-engine-from-scratch-f914c12bb162. We worked through the ray tracing process incrementally, adding features in a modular fashion to understand how each component works and to note the visual effects of the components. Then with the functional ray tracer, we took to creating visually interesting scenes.

## Project Structure

### Core Modules

- **`vector.py`** - Implements 3D vector mathematics including operations like dot product, cross product, normalization, reflection, and refraction. Also includes an `Angle` class for rotation operations.

- **`ray.py`** - Contains the `Ray` class for casting rays through the scene and the `Intersection` class for tracking ray-object intersections. Handles ray-sphere intersection calculations, reflection, refraction, and recursive ray tracing with configurable bounce limits.

- **`object.py`** - Defines the `Sphere` class representing 3D spheres with properties like center position, radius, material, color, and unique ID.

- **`material.py`** - Implements the `Material` class that defines surface properties including reflectivity, transparency, emissivity, and refractive index.

- **`colour.py`** - Provides the `Colour` class for RGB color representation and operations like color addition, scaling, and illumination calculations.

- **`light.py`** - Contains lighting classes: `GlobalLight` for directional ambient lighting and `PointLight` for point light sources with distance-based attenuation.

### Notebooks

The project includes several Jupyter notebooks demonstrating different ray tracing features:

- **`basic.ipynb`** - Basic ray tracing with emitive spheres
- **`point_light.ipynb`** - Demonstrates point light sources
- **`global_light.ipynb`** - Shows global/directional lighting
- **`reflection.ipynb`** - Examples of reflective surfaces
- **`refraction.ipynb`** - Demonstrates transparent materials and refraction
- **`fun_1.ipynb` through `fun_8.ipynb`** - Various creative examples and experiments

### Output

- **`output_images/`** - Directory containing rendered output images from various notebooks

## How to Run

This project uses Jupyter notebooks for rendering scenes. To run any of the notebooks:

1. Ensure you have the required dependencies installed:

   ```bash
   pip install numpy matplotlib seaborn jupyter
   ```

2. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

3. Open any of the notebook files (e.g., `basic.ipynb`, `reflection.ipynb`, `refraction.ipynb`) and run all cells.

4. The rendered images will be saved to the `output_images/` directory or in the project root, depending on the notebook configuration.

Each notebook demonstrates different aspects of the ray tracer:

- Basic rendering with emitive spheres
- Point light sources with shadows
- Global lighting effects
- Reflective materials
- Transparent materials with refraction

## Citations

- https://medium.com/@www.seymour/coding-a-3d-ray-tracing-graphics-engine-from-scratch-f914c12bb162
- AI tools used to generate the "How to Run" section of documentation.

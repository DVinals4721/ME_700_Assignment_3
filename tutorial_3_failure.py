from finiteelementanalysis import pre_process as pre
from finiteelementanalysis import solver
import numpy as np

# Problem setup - Highly compressed block
L = 1.0
H = 1.0
material_props = np.array([10.0, 1000.0])  # Very high bulk modulus

# Create mesh
ele_type = "D2_nn4"
nx = ny = 10
coords, connect = pre.generate_rect_mesh_2d(ele_type, 0.0, 0.0, L, H, nx, ny)

# Boundary conditions
boundary_nodes, boundary_edges = pre.identify_rect_boundaries(coords, connect, ele_type, 0.0, L, 0.0, H)
fixed_nodes = pre.assign_fixed_nodes_rect(boundary_nodes, "left", 0.0, 0.0)
dload_info = pre.assign_uniform_load_rect(boundary_edges, "right", 1000.0, 0.0)  # Very large load

try:
    # Attempt to solve
    displacements, info = solver.hyperelastic_solver(material_props, ele_type, coords.T, connect.T, 
                                                   fixed_nodes, dload_info, True, 5)
except Exception as e:
    print("Solver failed with error:", str(e))

"""
This example fails because:
1. The material is nearly incompressible (high bulk modulus)
2. The applied load is very large
3. The mesh is too coarse
4. Using linear elements (D2_nn4) for large deformation problems

To improve:
- Use higher-order elements (D2_nn8_quad)
- Refine the mesh
- Use smaller load steps
- Reduce the material incompressibility
"""
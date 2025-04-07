from finiteelementanalysis import pre_process as pre
from finiteelementanalysis import solver
import numpy as np
import matplotlib.pyplot as plt

def analytical_beam_deflection(x, L, P, E, I):
    """Analytical solution for cantilever beam deflection"""
    return (P * x**2 * (3*L - x)) / (6 * E * I)

# Problem setup - Cantilever beam
L = 10.0  # Length
H = 1.0   # Height
E = 1000.0  # Young's modulus
nu = 0.3    # Poisson's ratio
P = 1.0     # End load

# Convert to Neo-Hookean parameters
mu = E / (2 * (1 + nu))
kappa = E / (3 * (1 - 2*nu))
material_props = np.array([mu, kappa])

# Create meshes with different refinements
ele_types = ["D2_nn4", "D2_nn8_quad"]
nx_values = [10, 20, 40]
errors = []

for ele_type in ele_types:
    for nx in nx_values:
        # Generate mesh
        coords, connect = pre.generate_rect_mesh_2d(ele_type, 0.0, 0.0, L, H, nx, int(nx/10))
        
        # Boundary conditions
        boundary_nodes, boundary_edges = pre.identify_rect_boundaries(coords, connect, ele_type, 0.0, L, 0.0, H)
        fixed_nodes = pre.assign_fixed_nodes_rect(boundary_nodes, "left", 0.0, 0.0)
        dload_info = pre.assign_uniform_load_rect(boundary_edges, "right", P, 0.0)

        # Solve
        displacements, _ = solver.hyperelastic_solver(material_props, ele_type, coords.T, connect.T, 
                                                    fixed_nodes, dload_info, False, 1)
        
        # Compare with analytical solution
        I = H**3 / 12
        x_coords = coords[:, 0]
        analytical_disp = analytical_beam_deflection(x_coords, L, P, E, I)
        numerical_disp = displacements[-1][:, 1]  # vertical displacement
        
        error = np.linalg.norm(analytical_disp - numerical_disp) / np.linalg.norm(analytical_disp)
        errors.append((ele_type, nx, error))

# Plot results
for ele_type in ele_types:
    ele_errors = [e[2] for e in errors if e[0] == ele_type]
    plt.loglog(nx_values, ele_errors, '-o', label=ele_type)

plt.xlabel('Number of elements')
plt.ylabel('Relative Error')
plt.legend()
plt.grid(True)
plt.show()
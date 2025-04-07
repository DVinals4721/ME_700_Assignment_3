from finiteelementanalysis import pre_process as pre
from finiteelementanalysis import solver
import numpy as np
import matplotlib.pyplot as plt

# Problem setup - Large deformation bending
L = 10.0
H = 1.0
material_props = np.array([10.0, 100.0])  # mu, kappa

# h-refinement study
nx_values = [10, 20, 40, 80]
ele_types = ["D2_nn4", "D2_nn8_quad"]  # p-refinement
results = []

for ele_type in ele_types:
    for nx in nx_values:
        # Generate mesh
        coords, connect = pre.generate_rect_mesh_2d(ele_type, 0.0, 0.0, L, H, nx, int(nx/10))
        
        # Boundary conditions
        boundary_nodes, boundary_edges = pre.identify_rect_boundaries(coords, connect, ele_type, 0.0, L, 0.0, H)
        fixed_nodes = pre.assign_fixed_nodes_rect(boundary_nodes, "left", 0.0, 0.0)
        dload_info = pre.assign_uniform_load_rect(boundary_edges, "right", 50.0, 0.0)

        # Solve with load stepping
        displacements, info = solver.hyperelastic_solver(material_props, ele_type, coords.T, connect.T, 
                                                       fixed_nodes, dload_info, False, 10)
        
        # Store maximum displacement
        max_disp = np.max(np.abs(displacements[-1]))
        results.append((ele_type, nx, max_disp))

# Plot convergence
for ele_type in ele_types:
    ele_results = [(r[1], r[2]) for r in results if r[0] == ele_type]
    nx_list, disp_list = zip(*ele_results)
    plt.semilogx(nx_list, disp_list, '-o', label=ele_type)

plt.xlabel('Number of elements')
plt.ylabel('Maximum displacement')
plt.legend()
plt.grid(True)
plt.show()
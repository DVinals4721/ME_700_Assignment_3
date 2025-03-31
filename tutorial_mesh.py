import pre_process as pre
import pre_process_demo_helper_fcns as pre_demo
import numpy as np
import matplotlib.pyplot as plt

def fcn_interp(x, y):
    return np.sin(x / 10.0) * np.cos(y / 10.0)

def fcn_interp_deriv(x, y):
    df_dx = np.cos(x / 10.0) * np.cos(y / 10.0) * 1.0 / 10.0
    df_dy = -np.sin(x / 10.0) * np.sin(y / 10.0) * 1.0 / 10.0
    return np.array([df_dx, df_dy])

# 1. Element type and number of Gauss Points
ele_type = "D2_nn3_tri"  # or "D2_nn6_tri"
num_gauss_pts = 3  # 1, 3, or 4

print(f"Element type: {ele_type}")
print(f"Number of Gauss Points: {num_gauss_pts}")

# Create mesh
mesh_name = f"bulldog_mesh_{ele_type}_gp{num_gauss_pts}"
complex_outline = pre.get_bulldog_outline()
mesh_size = 10.0
coords, connect = pre.mesh_outline(complex_outline, ele_type, mesh_name, mesh_size)
mesh_gauss_pts = pre_demo.get_all_mesh_gauss_pts(ele_type, num_gauss_pts, coords, connect)

# 2. Image of the mesh with Gauss Points shown
pre_demo.plot_mesh_2D(mesh_name, ele_type, coords, connect, mesh_gauss_pts)
plt.title("Mesh with Gauss Points")
plt.savefig(f"{mesh_name}_with_gauss_points.png")
plt.close()

# 3. Element quality histograms
aspect_ratios, skewness, min_angles, max_angles = pre_demo.compute_element_quality_metrics(ele_type, coords, connect)
cond_nums, jac_dets = pre_demo.compute_condition_and_jacobian(ele_type, coords, connect)
plot_file = mesh_name + "_histograms"
pre_demo.plot_element_quality_histograms(
    fname=str(plot_file),
    super_title=f"Mesh Quality Metrics ({ele_type})",
    ele_type=ele_type,
    cond_nums=cond_nums,
    jac_dets=jac_dets,
    aspect_ratios=aspect_ratios,
    skewness=skewness,
    min_angles=min_angles,
    max_angles=max_angles
)

# 4. Interpolation function
print("Interpolation function:")
print(fcn_interp.__code__.co_code)

# 5. Gauss point interpolation plot w/ error
ground_truth_fcn = fcn_interp(mesh_gauss_pts[..., 0], mesh_gauss_pts[..., 1])
interpolated = pre_demo.interpolate_scalar_to_gauss_pts(ele_type, num_gauss_pts, fcn_interp, coords, connect)
error_plot = mesh_name + "_fcn_errors"
pre_demo.plot_interpolation_with_error(
    str(error_plot),
    ele_type,
    coords,
    connect,
    mesh_gauss_pts,
    interpolated,
    ground_truth_fcn
)

# 6. Gauss point gradient interpolation plot w/ error
ground_truth_grad = np.zeros_like(mesh_gauss_pts)
for kk in range(mesh_gauss_pts.shape[0]):
    for jj in range(mesh_gauss_pts.shape[1]):
        x, y = mesh_gauss_pts[kk, jj, 0], mesh_gauss_pts[kk, jj, 1]
        ground_truth_grad[kk, jj] = fcn_interp_deriv(x, y)

interpolated_grad = pre_demo.interpolate_scalar_deriv_to_gauss_pts(
    ele_type,
    num_gauss_pts,
    fcn_interp,
    coords,
    connect
)

grad_error_plot = mesh_name + "_fcn_grad_errors"
pre_demo.plot_interpolation_gradient_with_error(
    str(grad_error_plot),
    ele_type,
    coords,
    connect,
    mesh_gauss_pts,
    interpolated_grad,
    ground_truth_grad
)

print("All tasks completed. Check the generated image files for visualizations.")
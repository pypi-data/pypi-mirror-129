"""
Collection of Smoothing Functions
"""

# global
import ivy as _ivy
import math as _math

# local
from ivy_vision import single_view_geometry as _ivy_svg

MIN_DENOMINATOR = 1e-12


# noinspection PyUnresolvedReferences
def weighted_image_smooth(mean, weights, kernel_dim):
    """
    Smooth an image using weight values from a weight image of the same size.

    :param mean: Image to smooth *[batch_shape,h,w,d]*
    :type mean: array
    :param weights: Variance image, with the variance values of each pixel in the image *[batch_shape,h,w,d]*
    :type weights: array
    :param kernel_dim: The dimension of the kernel
    :type kernel_dim: int
    :return: Image smoothed based on variance image and smoothing kernel.
    """

    # shapes as list
    kernel_shape = [kernel_dim, kernel_dim]
    dim = mean.shape[-1]

    # KW x KW x D
    kernel = _ivy.ones(kernel_shape + [dim])

    # D
    kernel_sum = _ivy.reduce_sum(kernel, [0, 1])[0]

    # BS x H x W x D
    mean_x_weights = mean * weights
    mean_x_weights_sum = _ivy.abs(_ivy.depthwise_conv2d(mean_x_weights, kernel, 1, "VALID"))
    sum_of_weights = _ivy.depthwise_conv2d(weights, kernel, 1, "VALID")
    new_mean = mean_x_weights_sum / (sum_of_weights + MIN_DENOMINATOR)

    new_weights = sum_of_weights / (kernel_sum + MIN_DENOMINATOR)

    # BS x H x W x D,  # BS x H x W x D
    return new_mean, new_weights


def smooth_image_fom_var_image(mean, var, kernel_dim, kernel_scale, dev_str=None):
    """
    Smooth an image using variance values from a variance image of the same size, and a spatial smoothing kernel.

    :param mean: Image to smooth *[batch_shape,h,w,d]*
    :type mean: array
    :param var: Variance image, with the variance values of each pixel in the image *[batch_shape,h,w,d]*
    :type var: array
    :param kernel_dim: The dimension of the kernel
    :type kernel_dim: int
    :param kernel_scale: The scale of the kernel along the channel dimension *[d]*
    :type kernel_scale: array
    :param dev_str: device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. Same as x if None.
    :type dev_str: str, optional
    :return: Image smoothed based on variance image and smoothing kernel.
    """

    if dev_str is None:
        dev_str = _ivy.dev_str(mean)

    # shapes as list
    kernel_shape = [kernel_dim, kernel_dim]
    kernel_size = kernel_dim ** 2
    dims = mean.shape[-1]

    # KH x KW x 2
    uniform_pixel_coords = _ivy_svg.create_uniform_pixel_coords_image(kernel_shape, dev_str=dev_str)[..., 0:2]

    # 2
    kernel_central_pixel_coord = _ivy.array([float(_math.floor(kernel_shape[0] / 2)),
                                             float(_math.floor(kernel_shape[1] / 2))], dev_str=dev_str)

    # KH x KW x 2
    kernel_xy_dists = kernel_central_pixel_coord - uniform_pixel_coords
    kernel_xy_dists_sqrd = kernel_xy_dists ** 2

    # KW x KW x D x D
    unit_kernel = _ivy.tile(_ivy.reduce_sum(kernel_xy_dists_sqrd, -1, keepdims=True) ** 0.5, (1, 1, dims))
    kernel = 1 + unit_kernel * kernel_scale
    recip_kernel = 1 / (kernel + MIN_DENOMINATOR)

    # D
    kernel_sum = _ivy.reduce_sum(kernel, [0, 1])[0]
    recip_kernel_sum = _ivy.reduce_sum(recip_kernel, [0, 1])

    # BS x H x W x D
    recip_var = 1 / (var + MIN_DENOMINATOR)
    recip_var_scaled = recip_var + 1

    recip_new_var_scaled = _ivy.depthwise_conv2d(recip_var_scaled, recip_kernel, 1, "VALID")
    # This 0.99 prevents float32 rounding errors leading to -ve variances, the true equation would use 1.0
    recip_new_var = recip_new_var_scaled - recip_kernel_sum * 0.99
    new_var = 1 / (recip_new_var + MIN_DENOMINATOR)

    mean_x_recip_var = mean * recip_var
    mean_x_recip_var_sum = _ivy.abs(_ivy.depthwise_conv2d(mean_x_recip_var, recip_kernel, 1, "VALID"))
    new_mean = new_var * mean_x_recip_var_sum

    new_var = new_var * kernel_size ** 2 / (kernel_sum + MIN_DENOMINATOR)
    # prevent overconfidence from false meas independence assumption

    # BS x H x W x D,        # BS x H x W x D
    return new_mean, new_var

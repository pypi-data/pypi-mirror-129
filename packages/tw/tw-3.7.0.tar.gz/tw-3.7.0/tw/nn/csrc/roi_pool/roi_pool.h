
#ifndef _TW_DNN_OPS_ROI_POOL_H_
#define _TW_DNN_OPS_ROI_POOL_H_

#include <torch/extension.h>

std::tuple<at::Tensor, at::Tensor> ROIPool_forward_cuda(
    const at::Tensor& input,
    const at::Tensor& rois,
    const float spatial_scale,
    const int pooled_height,
    const int pooled_width);

at::Tensor ROIPool_backward_cuda(const at::Tensor& grad,
                                 const at::Tensor& input,
                                 const at::Tensor& rois,
                                 const at::Tensor& argmax,
                                 const float spatial_scale,
                                 const int pooled_height,
                                 const int pooled_width,
                                 const int batch_size,
                                 const int channels,
                                 const int height,
                                 const int width);

at::Tensor nms_cuda(const at::Tensor boxes, float nms_overlap_thresh);

at::Tensor compute_flow_cuda(const at::Tensor& boxes,
                             const int height,
                             const int width);

std::tuple<at::Tensor, at::Tensor> ROIPool_forward(const at::Tensor& input,
                                                   const at::Tensor& rois,
                                                   const float spatial_scale,
                                                   const int pooled_height,
                                                   const int pooled_width) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ROIPool_forward_cuda(
        input, rois, spatial_scale, pooled_height, pooled_width);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

at::Tensor ROIPool_backward(const at::Tensor& grad,
                            const at::Tensor& input,
                            const at::Tensor& rois,
                            const at::Tensor& argmax,
                            const float spatial_scale,
                            const int pooled_height,
                            const int pooled_width,
                            const int batch_size,
                            const int channels,
                            const int height,
                            const int width) {
  if (grad.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ROIPool_backward_cuda(grad,
                                 input,
                                 rois,
                                 argmax,
                                 spatial_scale,
                                 pooled_height,
                                 pooled_width,
                                 batch_size,
                                 channels,
                                 height,
                                 width);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

#endif
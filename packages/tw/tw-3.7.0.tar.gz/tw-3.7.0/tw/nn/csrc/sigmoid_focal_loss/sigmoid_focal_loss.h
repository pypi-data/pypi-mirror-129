

#ifndef _TW_DNN_OPS_SIGMOID_FOCAL_LOSS_H_
#define _TW_DNN_OPS_SIGMOID_FOCAL_LOSS_H_

#include <torch/extension.h>

at::Tensor SigmoidFocalLoss_forward_cuda(const at::Tensor& logits,
                                         const at::Tensor& targets,
                                         const int num_classes,
                                         const float gamma,
                                         const float alpha);

at::Tensor SigmoidFocalLoss_backward_cuda(const at::Tensor& logits,
                                          const at::Tensor& targets,
                                          const at::Tensor& d_losses,
                                          const int num_classes,
                                          const float gamma,
                                          const float alpha);

// Interface for Python
at::Tensor SigmoidFocalLoss_forward(const at::Tensor& logits,
                                    const at::Tensor& targets,
                                    const int num_classes,
                                    const float gamma,
                                    const float alpha) {
  if (logits.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return SigmoidFocalLoss_forward_cuda(
        logits, targets, num_classes, gamma, alpha);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

at::Tensor SigmoidFocalLoss_backward(const at::Tensor& logits,
                                     const at::Tensor& targets,
                                     const at::Tensor& d_losses,
                                     const int num_classes,
                                     const float gamma,
                                     const float alpha) {
  if (logits.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return SigmoidFocalLoss_backward_cuda(
        logits, targets, d_losses, num_classes, gamma, alpha);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

#endif
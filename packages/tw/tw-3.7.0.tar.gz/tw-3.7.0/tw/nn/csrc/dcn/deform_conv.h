// Copyright 2018 The KaiJIN Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================
// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
#ifndef _TW_DNN_OPS_DEFORM_CONV_H_
#define _TW_DNN_OPS_DEFORM_CONV_H_

#include <torch/extension.h>

void modulated_deform_conv_cuda_forward(at::Tensor input,
                                        at::Tensor weight,
                                        at::Tensor bias,
                                        at::Tensor ones,
                                        at::Tensor offset,
                                        at::Tensor mask,
                                        at::Tensor output,
                                        at::Tensor columns,
                                        int kernel_h,
                                        int kernel_w,
                                        const int stride_h,
                                        const int stride_w,
                                        const int pad_h,
                                        const int pad_w,
                                        const int dilation_h,
                                        const int dilation_w,
                                        const int group,
                                        const int deformable_group,
                                        const bool with_bias);

void modulated_deform_conv_cuda_backward(at::Tensor input,
                                         at::Tensor weight,
                                         at::Tensor bias,
                                         at::Tensor ones,
                                         at::Tensor offset,
                                         at::Tensor mask,
                                         at::Tensor columns,
                                         at::Tensor grad_input,
                                         at::Tensor grad_weight,
                                         at::Tensor grad_bias,
                                         at::Tensor grad_offset,
                                         at::Tensor grad_mask,
                                         at::Tensor grad_output,
                                         int kernel_h,
                                         int kernel_w,
                                         int stride_h,
                                         int stride_w,
                                         int pad_h,
                                         int pad_w,
                                         int dilation_h,
                                         int dilation_w,
                                         int group,
                                         int deformable_group,
                                         const bool with_bias);

int deform_conv_forward_cuda(at::Tensor input,
                             at::Tensor weight,
                             at::Tensor offset,
                             at::Tensor output,
                             at::Tensor columns,
                             at::Tensor ones,
                             int kW,
                             int kH,
                             int dW,
                             int dH,
                             int padW,
                             int padH,
                             int dilationW,
                             int dilationH,
                             int group,
                             int deformable_group,
                             int im2col_step);

int deform_conv_backward_input_cuda(at::Tensor input,
                                    at::Tensor offset,
                                    at::Tensor gradOutput,
                                    at::Tensor gradInput,
                                    at::Tensor gradOffset,
                                    at::Tensor weight,
                                    at::Tensor columns,
                                    int kW,
                                    int kH,
                                    int dW,
                                    int dH,
                                    int padW,
                                    int padH,
                                    int dilationW,
                                    int dilationH,
                                    int group,
                                    int deformable_group,
                                    int im2col_step);

int deform_conv_backward_parameters_cuda(
  at::Tensor input,
  at::Tensor offset,
  at::Tensor gradOutput,
  at::Tensor gradWeight,  // at::Tensor gradBias,
  at::Tensor columns,
  at::Tensor ones,
  int kW,
  int kH,
  int dW,
  int dH,
  int padW,
  int padH,
  int dilationW,
  int dilationH,
  int group,
  int deformable_group,
  float scale,
  int im2col_step);

// Interface for Python
int deform_conv_forward(at::Tensor input,
                        at::Tensor weight,
                        at::Tensor offset,
                        at::Tensor output,
                        at::Tensor columns,
                        at::Tensor ones,
                        int kW,
                        int kH,
                        int dW,
                        int dH,
                        int padW,
                        int padH,
                        int dilationW,
                        int dilationH,
                        int group,
                        int deformable_group,
                        int im2col_step) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return deform_conv_forward_cuda(input,
                                    weight,
                                    offset,
                                    output,
                                    columns,
                                    ones,
                                    kW,
                                    kH,
                                    dW,
                                    dH,
                                    padW,
                                    padH,
                                    dilationW,
                                    dilationH,
                                    group,
                                    deformable_group,
                                    im2col_step);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

int deform_conv_backward_input(at::Tensor input,
                               at::Tensor offset,
                               at::Tensor gradOutput,
                               at::Tensor gradInput,
                               at::Tensor gradOffset,
                               at::Tensor weight,
                               at::Tensor columns,
                               int kW,
                               int kH,
                               int dW,
                               int dH,
                               int padW,
                               int padH,
                               int dilationW,
                               int dilationH,
                               int group,
                               int deformable_group,
                               int im2col_step) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return deform_conv_backward_input_cuda(input,
                                           offset,
                                           gradOutput,
                                           gradInput,
                                           gradOffset,
                                           weight,
                                           columns,
                                           kW,
                                           kH,
                                           dW,
                                           dH,
                                           padW,
                                           padH,
                                           dilationW,
                                           dilationH,
                                           group,
                                           deformable_group,
                                           im2col_step);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

int deform_conv_backward_parameters(
  at::Tensor input,
  at::Tensor offset,
  at::Tensor gradOutput,
  at::Tensor gradWeight,  // at::Tensor gradBias,
  at::Tensor columns,
  at::Tensor ones,
  int kW,
  int kH,
  int dW,
  int dH,
  int padW,
  int padH,
  int dilationW,
  int dilationH,
  int group,
  int deformable_group,
  float scale,
  int im2col_step) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return deform_conv_backward_parameters_cuda(input,
                                                offset,
                                                gradOutput,
                                                gradWeight,
                                                columns,
                                                ones,
                                                kW,
                                                kH,
                                                dW,
                                                dH,
                                                padW,
                                                padH,
                                                dilationW,
                                                dilationH,
                                                group,
                                                deformable_group,
                                                scale,
                                                im2col_step);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

void modulated_deform_conv_forward(at::Tensor input,
                                   at::Tensor weight,
                                   at::Tensor bias,
                                   at::Tensor ones,
                                   at::Tensor offset,
                                   at::Tensor mask,
                                   at::Tensor output,
                                   at::Tensor columns,
                                   int kernel_h,
                                   int kernel_w,
                                   const int stride_h,
                                   const int stride_w,
                                   const int pad_h,
                                   const int pad_w,
                                   const int dilation_h,
                                   const int dilation_w,
                                   const int group,
                                   const int deformable_group,
                                   const bool with_bias) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return modulated_deform_conv_cuda_forward(input,
                                              weight,
                                              bias,
                                              ones,
                                              offset,
                                              mask,
                                              output,
                                              columns,
                                              kernel_h,
                                              kernel_w,
                                              stride_h,
                                              stride_w,
                                              pad_h,
                                              pad_w,
                                              dilation_h,
                                              dilation_w,
                                              group,
                                              deformable_group,
                                              with_bias);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

void modulated_deform_conv_backward(at::Tensor input,
                                    at::Tensor weight,
                                    at::Tensor bias,
                                    at::Tensor ones,
                                    at::Tensor offset,
                                    at::Tensor mask,
                                    at::Tensor columns,
                                    at::Tensor grad_input,
                                    at::Tensor grad_weight,
                                    at::Tensor grad_bias,
                                    at::Tensor grad_offset,
                                    at::Tensor grad_mask,
                                    at::Tensor grad_output,
                                    int kernel_h,
                                    int kernel_w,
                                    int stride_h,
                                    int stride_w,
                                    int pad_h,
                                    int pad_w,
                                    int dilation_h,
                                    int dilation_w,
                                    int group,
                                    int deformable_group,
                                    const bool with_bias) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return modulated_deform_conv_cuda_backward(input,
                                               weight,
                                               bias,
                                               ones,
                                               offset,
                                               mask,
                                               columns,
                                               grad_input,
                                               grad_weight,
                                               grad_bias,
                                               grad_offset,
                                               grad_mask,
                                               grad_output,
                                               kernel_h,
                                               kernel_w,
                                               stride_h,
                                               stride_w,
                                               pad_h,
                                               pad_w,
                                               dilation_h,
                                               dilation_w,
                                               group,
                                               deformable_group,
                                               with_bias);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

#endif
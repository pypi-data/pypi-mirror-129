# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import numpy as np
import nearest_neighbors.lib.python.nearest_neighbors as nearest_neighbors
import time

batch_size = 16
num_points = 81920
K = 16
pc = np.random.rand(batch_size, num_points, 3).astype(np.float32)

# nearest neighbours
start = time.time()
neigh_idx = nearest_neighbors.knn_batch(pc, pc, K, omp=True)
print(time.time() - start)



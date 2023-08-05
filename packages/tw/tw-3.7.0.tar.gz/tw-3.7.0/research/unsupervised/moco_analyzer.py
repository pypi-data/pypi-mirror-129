
import numpy as np
import matplotlib.pyplot as pyplot
import argparse
import torch

# if opt.cuda:
#   print("set use cuda")


# else:
#   torch.set_default_tensor_type(torch.DoubleTensor)


def Hbeta_torch(D, beta=1.0):
  P = torch.exp(-D.clone() * beta)

  sumP = torch.sum(P)

  H = torch.log(sumP) + beta * torch.sum(D * P) / sumP
  P = P / sumP

  return H, P


def x2p_torch(X, tol=1e-5, perplexity=30.0):
  """
      Performs a binary search to get P-values in such a way that each
      conditional Gaussian has the same perplexity.
  """

  # Initialize some variables
  print("Computing pairwise distances...")
  (n, d) = X.shape

  sum_X = torch.sum(X*X, 1)
  D = torch.add(torch.add(-2 * torch.mm(X, X.t()), sum_X).t(), sum_X)

  P = torch.zeros(n, n)
  beta = torch.ones(n, 1)
  logU = torch.log(torch.tensor([perplexity]))
  n_list = [i for i in range(n)]

  # Loop over all datapoints
  for i in range(n):

    # Print progress
    if i % 500 == 0:
      print("Computing P-values for point %d of %d..." % (i, n))

    # Compute the Gaussian kernel and entropy for the current precision
    # there may be something wrong with this setting None
    betamin = None
    betamax = None
    Di = D[i, n_list[0:i]+n_list[i+1:n]]

    (H, thisP) = Hbeta_torch(Di, beta[i])

    # Evaluate whether the perplexity is within tolerance
    Hdiff = H - logU
    tries = 0
    while torch.abs(Hdiff) > tol and tries < 50:

      # If not, increase or decrease precision
      if Hdiff > 0:
        betamin = beta[i].clone()
        if betamax is None:
          beta[i] = beta[i] * 2.
        else:
          beta[i] = (beta[i] + betamax) / 2.
      else:
        betamax = beta[i].clone()
        if betamin is None:
          beta[i] = beta[i] / 2.
        else:
          beta[i] = (beta[i] + betamin) / 2.

      # Recompute the values
      (H, thisP) = Hbeta_torch(Di, beta[i])

      Hdiff = H - logU
      tries += 1

    # Set the final row of P
    P[i, n_list[0:i]+n_list[i+1:n]] = thisP

  # Return final P-matrix
  return P


def pca_torch(X, no_dims=50):
  print("Preprocessing the data using PCA...")
  (n, d) = X.shape
  X = X - torch.mean(X, 0)

  (l, M) = torch.eig(torch.mm(X.t(), X), True)
  # split M real
  for i in range(d):
    if l[i, 1] != 0:
      M[:, i+1] = M[:, i]
      i += 1

  Y = torch.mm(X, M[:, 0:no_dims])
  return Y


def tsne(X, no_dims=2, initial_dims=50, perplexity=30.0):
  """
      Runs t-SNE on the dataset in the NxD array X to reduce its
      dimensionality to no_dims dimensions. The syntaxis of the function is
      `Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array.
  """

  # Check inputs
  if isinstance(no_dims, float):
    print("Error: array X should not have type float.")
    return -1
  if round(no_dims) != no_dims:
    print("Error: number of dimensions should be an integer.")
    return -1

  # Initialize variables
  X = pca_torch(X, initial_dims)
  (n, d) = X.shape
  max_iter = 200
  initial_momentum = 0.5
  final_momentum = 0.8
  eta = 500
  min_gain = 0.01
  Y = torch.randn(n, no_dims)
  dY = torch.zeros(n, no_dims)
  iY = torch.zeros(n, no_dims)
  gains = torch.ones(n, no_dims)

  # Compute P-values
  P = x2p_torch(X, 1e-5, perplexity)
  P = P + P.t()
  P = P / torch.sum(P)
  P = P * 4.    # early exaggeration
  print("get P shape", P.shape)
  P = torch.max(P, torch.tensor([1e-21]))

  # Run iterations
  for iter in range(max_iter):

    # Compute pairwise affinities
    sum_Y = torch.sum(Y*Y, 1)
    num = -2. * torch.mm(Y, Y.t())
    num = 1. / (1. + torch.add(torch.add(num, sum_Y).t(), sum_Y))
    num[range(n), range(n)] = 0.
    Q = num / torch.sum(num)
    Q = torch.max(Q, torch.tensor([1e-12]))

    # Compute gradient
    PQ = P - Q
    for i in range(n):
      dY[i, :] = torch.sum((PQ[:, i] * num[:, i]).repeat(no_dims, 1).t() * (Y[i, :] - Y), 0)

    # Perform the update
    if iter < 20:
      momentum = initial_momentum
    else:
      momentum = final_momentum

    gains = (gains + 0.2) * ((dY > 0.) != (iY > 0.)).double() + (gains * 0.8) * ((dY > 0.) == (iY > 0.)).double()
    gains[gains < min_gain] = min_gain
    iY = momentum * iY - eta * (gains * dY)
    Y = Y + iY
    Y = Y - torch.mean(Y, 0)

    # Compute current value of cost function
    if (iter + 1) % 10 == 0:
      C = torch.sum(P * torch.log(P / Q))
      print("Iteration %d: error is %f" % (iter + 1, C))

    # Stop lying about P-values
    if iter == 100:
      P = P / 4.

  # Return solution
  return Y


if __name__ == "__main__":
  print("Run Y = tsne.tsne(X, no_dims, perplexity) to perform t-SNE on your dataset.")
  torch.set_default_tensor_type(torch.cuda.DoubleTensor)


  # {
  #     '_demo/MOCOv2-simple-LOL.CLIP2/LOL_clip2.pth': 'r',
  #     '_demo/MOCOv2-simple-SVID_20210427_105627_1/mtd_SVID_20210427_105627_1_0_640x312.mp4.fold.pth', 'b',
  #     '_demo/MOCOv2-simple-SVID_20210427_110917_1/mtd_SVID_20210427_110917_1_0_640x312.mp4.fold.pth', 'b',
  #     '_demo/MOCOv2-simple-SVID_20210506_151543_1/demo_SVID_20210506_151543_1_0__312.0x640.0.mp4.fold.pth', 'b',
  #     '_demo/MOCOv2-simple-SVID_20210506_154544_1/demo_SVID_20210506_154544_1_0__640.0x312.0.mp4.fold.pth'
  #     '_demo/MOCOv2-simple-SVID_20210506_155555_1/demo_SVID_20210506_155555_1_0__640.0x312.0.mp4.fold.pth'
  # }

  X = []
  labels = []
  for k, v in torch.load('_demo/MOCOv2-simple-LOL.CLIP2/LOL_clip2.pth', 'cpu').items():
    X.append(v)
    labels.append(0)

  for k, v in torch.load('_demo/MOCOv2-simple-SVID_20210427_105627_1/mtd_SVID_20210427_105627_1_0_640x312.mp4.fold.pth', 'cpu').items():
    X.append(v)
    labels.append(1)

  for k, v in torch.load('_demo/MOCOv2-simple-SVID_20210427_110917_1/mtd_SVID_20210427_110917_1_0_640x312.mp4.fold.pth', 'cpu').items():
    X.append(v)
    labels.append(2)

  for k, v in torch.load('_demo/MOCOv2-simple-SVID_20210506_151543_1/demo_SVID_20210506_151543_1_0__312.0x640.0.mp4.fold.pth', 'cpu').items():
    X.append(v)
    labels.append(3)

    # print(k, v.shape)
  X = torch.cat(X, dim=0).cuda()

  # X = np.loadtxt(xfile)
  # X = torch.Tensor(X)
  # labels = np.loadtxt(yfile).tolist()

  # # confirm that x file get same number point than label file
  # # otherwise may cause error in scatter
  # assert(len(X[:, 0]) == len(X[:, 1]))
  # assert(len(X) == len(labels))

  with torch.no_grad():
    Y = tsne(X, 2, 50, 20.0)

  print(Y.shape)

  # if opt.cuda:
  Y = Y.cpu().numpy()

  # # You may write result in two files
  # # print("Save Y values in file")
  # # Y1 = open("y1.txt", 'w')
  # # Y2 = open('y2.txt', 'w')
  # # for i in range(Y.shape[0]):
  # #     Y1.write(str(Y[i,0])+"\n")
  # #     Y2.write(str(Y[i,1])+"\n")

  pyplot.scatter(Y[:, 0], Y[:, 1], 20, labels)
  pyplot.savefig('123.png')

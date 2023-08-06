# GenAgg
A Learnable, Generalised Aggregation Function for GNNs

## Installation
```bash
cd GenAgg
python3 -m pip install -e .
```

## Theory
The function space of multiple different aggregators (min, max, mean, sum, etc...) can be parameterised by two variables:

![GenAgg](https://latex.codecogs.com/svg.image?{\color{Gray}\mathrm{GenAgg}_{p,\alpha}(x)=N^{\alpha}\left(\frac{1}{N}\sum_i^N{x_i^p}\right)^\frac{1}{p}})

By learning parameters p and alpha, GenAgg can select the most appropriate aggregator for a given scenario.
The following are special cases of GenAgg (note that in practice we use p'=tan(p*pi/4) so the domain [-inf,inf] is compressed to [-2,2]):

GenAgg[p=1, a=0] : mean

GenAgg[p=1, a=1] : sum

GenAgg[p=inf, a=0] : max

GenAgg[p=-inf, a=0] : min

GenAgg[p=0, a=0] : geometric mean

GenAgg[p=-1, a=0] : harmonic mean

GenAgg[p=2, a=0.5] : euclidean norm

## Example
```python
from genagg import GenAgg
import torch

agg = GenAgg(p=1, a=0, shift=True, learnable=False)

x = torch.randn(10,3)
y = agg(x)

print('x:', x)
print('y:', y)
```
```
x: tensor([[ 0.0890,  1.5933, -1.1298],
        [ 1.8399,  0.1661,  0.3371],
        [-0.8418,  0.9115,  0.8917],
        [ 0.2672, -0.3730,  1.5296],
        [-0.6422,  0.2952,  0.6574],
        [-2.3479, -1.3364, -1.0817],
        [-1.6736,  1.7427, -0.0809],
        [-0.0141, -0.7493,  0.0438],
        [ 0.4062,  0.9410,  0.1462],
        [-0.0480,  0.5727, -0.8570]])
y: tensor([-0.2965,  0.3764,  0.0456])
```

## Experiments
### Min function regression:
![min](https://github.com/Acciorocketships/GenAgg/blob/main/examples/results/min.png)
### Max function regression:
![min](https://github.com/Acciorocketships/GenAgg/blob/main/examples/results/max.png)
### Mean function regression:
![min](https://github.com/Acciorocketships/GenAgg/blob/main/examples/results/mean.png)
### Sum function regression:
![min](https://github.com/Acciorocketships/GenAgg/blob/main/examples/results/sum.png)

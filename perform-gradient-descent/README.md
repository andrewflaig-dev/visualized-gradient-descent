# Table Of Contents

# Notes
## Gradient Descent
An alogrithm that moves along "the path of steepest descent" thats why we subtract it from our current point to 'walk down' that slope bit by bit based on a learning rate.
In general, it is trying to find a basin, ie. when slope is 0. 
Gradient Descent can perform until convergence or when a threshold is met. 

In the real world, we typically perform gradient descent on a <b>loss function</b>. Loss functions model prediction error. During descent, we try to update parameters to minimize the loss, that is why we descent.

We create this parameter update rule
$$\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$$

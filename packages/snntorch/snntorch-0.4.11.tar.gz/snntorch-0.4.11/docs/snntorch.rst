snntorch
================


snnTorch Neurons
---------------------
:mod:`snntorch` is designed to be intuitively used with PyTorch, as though each spiking neuron were simply another activation in a sequence of layers. 

A variety of spiking neuron classes are available which can simply be treated as activation units with PyTorch. 
Each layer of spiking neurons are therefore agnostic to fully-connected layers, convolutional layers, residual connections, etc. 

The neuron models are represented by recursive functions which removes the need to store membrane potential traces in order to calculate the gradient. 
This eliminates the need to store traces of hidden states for all neurons to calculate the gradient. 
The lean requirements of :mod:`snntorch` enable small and large networks to be viably trained on CPU, where needed. 
Being deeply integrated with ``torch.autograd``, :mod:`snntorch` is able to take advantage of GPU acceleration in the same way as PyTorch.

By default, PyTorch's autodifferentiation tools are unable to calculate the analytical derivative of the spiking neuron graph. 
The discrete nature of spikes makes it difficult for ``torch.autograd`` to calculate a gradient that facilitates learning.
:mod:`snntorch` overrides the default gradient by using :mod:`snntorch.LIF.Heaviside`. Alternative options exist in :mod:`snntorch.surrogate`.

At present, the neurons available in :mod:`snntorch` are variants of the Leaky Integrate-and-Fire neuron model:

* **Leaky** - 1st-Order Leaky Integrate-and-Fire Neuron
* **Synaptic** - 2nd-Order Integrate-and-Fire Neuron (including synaptic conductance)
* **Lapicque** - Lapicque's RC Neuron Model
* **Alpha** - Alpha Membrane Model



How to use snnTorch's neuron models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Spiking neural networks can be constructed using a combination of the ``snntorch`` and ``torch.nn`` packages.

Example::

      import torch
      import torch.nn as nn
      import snntorch as snn

      alpha = 0.9
      beta = 0.85

      num_steps = 100


      # Define Network
      class Net(nn.Module):
         def __init__(self):
            super().__init__()

            # initialize layers
            self.fc1 = nn.Linear(num_inputs, num_hidden)
            self.lif1 = snn.Synaptic(alpha=alpha, beta=beta)
            self.fc2 = nn.Linear(num_hidden, num_outputs)
            self.lif2 = snn.Synaptic(alpha=alpha, beta=beta)

         def forward(self, x):
            spk1, syn1, mem1 = self.lif1.init_synaptic(batch_size, num_hidden)
            spk2, syn2, mem2 = self.lif2.init_synaptic(batch_size, num_outputs)

            spk2_rec = []  # Record the output trace of spikes
            mem2_rec = []  # Record the output trace of membrane potential

            for step in range(num_steps):
                  cur1 = self.fc1(x)
                  spk1, syn1, mem1 = self.lif1(cur1, syn1, mem1)
                  cur2 = self.fc2(spk1)
                  spk2, syn2, mem2 = self.lif2(cur2, syn2, mem2)

                  spk2_rec.append(spk2)
                  mem2_rec.append(mem2)

            return torch.stack(spk2_rec, dim=0), torch.stack(mem2_rec, dim=0)

      net = Net().to(device)

      output, mem_rec = net(data.view(batch_size, -1))

In the above example, all hidden states, ``spk``, ``syn``, and ``mem`` must be manually initialized for each layer.
This can be overcome by automatically instantiating neuron hidden states by invoking ``init_hidden=True``. 

In some cases (e.g., in real-time recurrent learning), it might be necessary to perform backward passes before all time steps have completed processing.
This requires moving the time step for-loop out of the network and into the training-loop. 

An example of this is shown below::

      import torch
      import torch.nn as nn
      import snntorch as snn

      num_steps = 100

      lif1 = snn.Leaky(beta=0.9, init_hidden=True) # only returns spk
      lif2 = snn.Leaky(beta=0.9, init_hidden=True, output=True) # returns mem and spk if output=True


      #  Initialize Network
      net = nn.Sequential(nn.Flatten(),
                          nn.Linear(784,1000), 
                          lif1,
                          nn.Linear(1000, 10),
                          lif2).to(device)

      for step in range(num_steps):
         spk_out, mem_out = net(data.view(batch_size, -1))


Setting the hidden states to instance variables is necessary for calling the backpropagation methods available in :mod:`snntorch.backprop`, or for calling :mod:`nn.Sequential` from PyTorch.

Whenever a neuron is instantiated, it is added as a list item to the class variable :mod:`LIF.instances`. 
This helps the functions in :mod:`snntorch.backprop` keep track of what neurons are being used in the network, and when they must be detached from the computation graph. 

In the above examples, the decay rate of membrane potential :mod:`beta` is treated as a hyperparameter. But it can also be configured as a learnable parameter, as shown below::

      import torch
      import torch.nn as nn
      import snntorch as snn

      num_steps = 100

      lif1 = snn.Leaky(beta=0.9, learn_beta=True, init_hidden=True) # only returns spk
      lif2 = snn.Leaky(beta=0.5, learn_beta=True, init_hidden=True, output=True) # returns mem and spk if output=True


      #  Initialize Network
      net = nn.Sequential(nn.Flatten(),
                          nn.Linear(784,1000), 
                          lif1,
                          nn.Linear(1000, 10),
                          lif2).to(device)

      for step in range(num_steps):
         spk_out, mem_out = net(data.view(batch_size, -1))

Here, :mod:`beta` is initialized to 0.9 for the first layer, and 0.5 for the second layer.
Each layer then treats it as a learnable parameter, just like all the other network weights.
In the event you wish to have a learnable decay rate for each neuron rather than each layer, the following example shows how::


      import torch
      import torch.nn as nn
      import snntorch as snn

      num_steps = 100
      num_hidden = 1000
      num_output = 10

      beta1 = torch.rand(num_hidden)  # randomly initialize beta as a vector
      beta2 = torch.rand(num_output)

      lif1 = snn.Leaky(beta=beta1, learn_beta=True, init_hidden=True) # only returns spk
      lif2 = snn.Leaky(beta=beta2 learn_beta=True, init_hidden=True, output=True) # returns mem and spk if output=True


      #  Initialize Network
      net = nn.Sequential(nn.Flatten(),
                          nn.Linear(784, num_hidden), 
                          lif1,
                          nn.Linear(1000, num_output),
                          lif2).to(device)

      for step in range(num_steps):
         spk_out, mem_out = net(data.view(batch_size, -1))


Each neuron has the option to inhibit other neurons within the same layer from firing. 
This can be invoked by setting ``inhibition=True`` when instantiating the neuron layer.

.. warning:: invoking ``inhibition=True`` requires ``batch_size`` to also be passed as an argument to the neuron.



.. automodule:: snntorch
   :members:
   :undoc-members:
   :show-inheritance:
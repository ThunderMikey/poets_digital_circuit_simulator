# Abstract
Large circuit simulations on modern CPUs can take a lot of time due to
their limited parallelism and overhead in communications on large data sets.
POETS (Partially Ordered Event Triggered System) is a technology under
development which has an extremely large number of processing cores
working independently of each other and fast inter-core connection infrastructure.
This project aims to realise the circuit simulation potential of this hardware,
by developing a digital circuit simulator running on it and
evaluate its performance against a well-known circuit simulator,
Simulator M, therefore, conclude the pros and cons to simulate circuits on POETS.
A toolchain was developed to convert an arbitrary combinatorial circuit to
a POETS executable that simulates the circuit.
The simulator does combinatorial gate-level simulation without timing considerations.
It is purely functional, similar to the functionality of Verilator and
it iterates all logical value combinations of input ports.
Together with implementation details,
evaluations have been made to explore architectural features which empower
simulations with better scalability in some circumstances,
although the overall observed performance is about 10 times worse than the
counterpart.

# Hands-on
You need to have git access to https://github.com/POETSII/graph_schema.git
because:
* The POETS graph generation toolchain needs Python libraries in this repo.
* The POETS simulator, `epoch_sim` is compiled from this repo.
* This repo is not open to public at the moment.

Git LFS is used to store all simulation logs of size 2GiB.
`GIT_LFS_SKIP_SMUDGE=1` env var can skip downloading LFS data.

1. `GIT_LFS_SKIP_SMUDGE=1 git clone git@github.com:ThunderMikey/poets_digital_circuit_simulator.git`
2. `git submodule init && git submodule update`
3. To generate POETS graph instances: `make graphs/2_bit_full_adder.xml`
4. Then, to get simulation results: `make sim_results/2_bit_full_adder.log`

# Remote POETS server

`ssh defoe.cl.cam.ac.uk`


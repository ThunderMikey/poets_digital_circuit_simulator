#!/bin/bash
make digital_circuit_simulator_tests

bin/epoch_sim  --log-level 2 --max-steps 10 --snapshots 1 tmp.snap  demos/digital_circuit_simulator/digital_circuit_typical.xml

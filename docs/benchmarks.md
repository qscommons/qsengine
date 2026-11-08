# Benchmarks

Every simulator ran the same circuit: five layers of a Hadamard on every qubit, an RZ rotation on every qubit and a chain of CNOTs, then 1000 measurement shots. Times are the best of at least three runs.

## Results

<!-- Copied from ../benchmarks/results.csv: simulate + 1000 shots, best of at least three runs. -->

| Qubits | Pure Python | qsengine CPU | qsengine GPU | Qiskit Aer |
| ---: | ---: | ---: | ---: | ---: |
| 6 | 2.2 ms | 0.11 ms | 1.4 ms | 3.4 ms |
| 10 | 31 ms | 0.29 ms | 1.3 ms | 6.1 ms |
| 14 | 713 ms | 2.2 ms | 1.5 ms | 11.7 ms |
| 18 | 17.7 s | 21 ms | 6.2 ms | 29 ms |
| 22 | not run | 1.17 s | 77 ms | 431 ms |

The pure Python loop was stopped after 18 qubits, when one run passed 10 seconds.

## What the numbers say

- Below 14 qubits the CPU backend is the fastest: 8 to 50 times faster than Qiskit Aer, because a call has almost no overhead. Aer’s time there is mostly its fixed per-call cost (about 2 ms to submit a job and build its result), so this measures call overhead more than simulation.
- From 14 qubits the GPU backend is the fastest: 3 to 8 times faster than Aer. The GPU backend computes in 32-bit floats and Aer ran in 64-bit; Aer’s `precision="single"` option would be the like-for-like comparison.
- The CPU backend stays ahead of Aer up to 19 qubits and falls behind from 20. At 20 qubits a 64-bit state is 16 MiB, the size of this CPU’s L3 cache, and the CPU backend’s time per extra qubit jumps from about 2× to 3–4×, so the likely cause is the state no longer fitting in cache.
- There is one benchmark circuit. qsengine merges the H and RZ on each qubit into one pass over the state, which suits this circuit; other circuits may compare differently.
- Against a plain Python loop, the CPU backend is about 100 times faster at 10 qubits and 840 times faster at 18.

## Setup

AMD Ryzen 5 5500 (6 cores), AMD Radeon RX 6600, Windows 10, Python 3.14, Qiskit Aer 0.18.2 with its default statevector method in 64-bit precision. These are one machine’s numbers; run the script to get yours.

```bash
pip install qiskit qiskit-aer matplotlib
python benchmarks/benchmark.py --max-qubits 22
```

The script and the raw [results.csv](../benchmarks/results.csv) are in the [benchmarks folder](../benchmarks/) of the repository.

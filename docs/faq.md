# Questions

Short answers to the questions people ask first. The user guide has the detail.

## Do I need a GPU?

No. Without one, or without a working driver, the default backend runs everything on the CPU and your code does not change.

## Which GPUs work?

Any that supports Vulkan, DirectX 12 or Metal: NVIDIA, AMD, Intel and Apple. qsengine talks to them through wgpu, so there is no CUDA to install.

## How many qubits can I simulate?

Memory doubles with every qubit: 16 bytes for each of the 2ⁿ amplitudes. 20 qubits take 16 MiB, 26 take 1 GiB, and 30 qubits (16 GiB) is the hard limit. If the state does not fit in memory, qsengine raises MemoryError.

## Why do GPU results differ in the last digits?

The GPU computes in 32-bit floats and the CPU in 64-bit. They agree to about 1e-5 for circuits of a few hundred gates, far below what sampling can show; the gap grows with circuit depth. Pass `backend="cpu"` for 64-bit results at every size.

## Which way round are the bits?

Qubit 0 is the rightmost character, as in Qiskit. On three qubits, `qc.x(0)` measures as `"001"`.

## Is it faster than Qiskit Aer?

In our benchmark the GPU backend is 3 to 8 times faster from 14 qubits. The CPU backend is faster up to 19 qubits and slower from 20, where the 16 MiB state no longer fits in our test CPU's cache. Our GPU backend is 32-bit while Aer ran in 64-bit, and below 14 qubits Aer's time is mostly per-call overhead.

## Will the same seed give the same counts?

Yes. `run(seed=42)` returns identical counts every time on the same backend.

## Can I measure part-way through a circuit?

Yes, from 1.1. Give the circuit classical bits, call `qc.measure(qubit, clbit)` at any point, and put gates that depend on the result inside `with qc.if_test(clbit, value)`. Each shot of such a circuit is simulated on its own, so it costs more than a circuit that only measures at the end.

## Which Python versions work?

CPython 3.9 and newer. One wheel per platform covers all of them.

## Is it free?

Yes. qsengine is open source under the MIT licence.

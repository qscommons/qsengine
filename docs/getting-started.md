# Installation and first circuit

This page installs qsengine, builds a two-qubit circuit and reads its measurement counts. It takes a few minutes.

## Install

qsengine needs CPython 3.9 or newer. One wheel per platform covers every version, so there is nothing to compile. NumPy is installed with it.

```bash
pip install qsengine
```

Check that it imports and shows its version:

```python
import qsengine
print(qsengine.__version__)
```

```output
{{version}}
```

A GPU is optional. With one, large circuits run on it; without one, everything runs on the CPU. See [CPU and GPU backends](backends.md).

## Your first circuit

A circuit has a fixed number of qubits that all start in |0⟩. You add gates by calling methods on it. Nothing runs until you ask for a result.

```python
import qsengine

qc = qsengine.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

counts = qc.run(shots=1000, seed=1)
print(counts)
```

```output caption="Only 00 and 11 appear: the two qubits always agree." bars="00:513 01:0 10:0 11:487"
{'00': 513, '11': 487}
```

Line by line:

- `QuantumCircuit(2)` makes a circuit on qubits 0 and 1.
- `qc.h(0)` puts qubit 0 into an equal superposition of 0 and 1.
- `qc.cx(0, 1)` flips qubit 1 whenever qubit 0 is 1, which ties the two together.
- `qc.run(shots=1000, seed=1)` simulates the circuit once, measures it 1000 times and returns how often each result appeared.

The keys are bitstrings with qubit 0 on the right. `seed` makes the counts repeatable; leave it out for fresh randomness.

## Next steps

- [Examples](examples.md) show exact amplitudes, rotations and error handling.
- [Gates](gates.md) lists every gate you can add.
- [Running circuits](running.md) explains shots, seeds and exact states.

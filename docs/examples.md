# Examples

Each example is a complete program. Copy it, run it, and you will see the output shown under it: every output on this page was produced by running the code with qsengine {{version}}.

- [Bell state](#bell)
- [Exact amplitudes](#ghz)
- [Rotation](#rotation)
- [Bad input](#errors)

<a id="bell"></a>

## Bell state

Two qubits put into an entangled state, then measured 1000 times.

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

<a id="ghz"></a>

## Exact amplitudes

A three-qubit GHZ state read exactly, without sampling.

```python
import qsengine

qc = qsengine.QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

print(qc.probabilities())
print(qc.statevector())
```

```output caption="The exact probability of each of the 8 basis states." bars="000:0.5 001:0 010:0 011:0 100:0 101:0 110:0 111:0.5"
[0.5 0.  0.  0.  0.  0.  0.  0.5]
[0.70710678+0.j 0.        +0.j 0.        +0.j 0.        +0.j
 0.        +0.j 0.        +0.j 0.        +0.j 0.70710678+0.j]
```

<a id="rotation"></a>

## Rotation

One qubit rotated by π/3 about the Y axis.

```python
import math
import qsengine

qc = qsengine.QuantumCircuit(1)
qc.ry(0, math.pi / 3)

print(qc.probabilities())
print(qc.run(shots=1000, seed=7))
```

```output caption="cos²(π/6) = 0.75, and 743 of 1000 shots measured 0." bars="0:743 1:257"
[0.75 0.25]
{'1': 257, '0': 743}
```

<a id="errors"></a>

## Bad input

Mistakes raise a plain Python ValueError on the line that made them.

```python
import qsengine

qc = qsengine.QuantumCircuit(2)
qc.cx(1, 1)
```

```output caption="The gate is not recorded, so the circuit stays valid."
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    qc.cx(1, 1)
ValueError: qubit 1 used more than once in one gate
```

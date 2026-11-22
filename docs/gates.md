# Gates

qsengine has thirty named gates, and `unitary()` for any other. Each is a method on `QuantumCircuit` that records the gate; the circuit runs only when you ask for a result. `q`, `control` and `target` are qubit numbers starting at 0, and angles are in radians.

## Single-qubit gates

| Gate | Method | What it does |
| --- | --- | --- |
| Hadamard | `qc.h(q)` | Puts a basis state into an equal superposition: $\ket{0}$ becomes $(\ket{0} + \ket{1})/\sqrt{2}$. |
| Pauli X | `qc.x(q)` | Bit flip, the quantum NOT: $\ket{0}$ and $\ket{1}$ swap. |
| Pauli Y | `qc.y(q)` | Bit flip and phase flip: $\ket{0}$ becomes $i\ket{1}$. |
| Pauli Z | `qc.z(q)` | Phase flip: $\ket{1}$ becomes $-\ket{1}$. |
| S | `qc.s(q)` | Quarter turn of phase: $\ket{1}$ becomes $i\ket{1}$. |
| S dagger | `qc.sdg(q)` | Undoes S: $\ket{1}$ becomes $-i\ket{1}$. |
| T | `qc.t(q)` | Eighth turn of phase: $\ket{1}$ becomes $e^{i\pi/4}\ket{1}$. |
| T dagger | `qc.tdg(q)` | Undoes T: $\ket{1}$ becomes $e^{-i\pi/4}\ket{1}$. |
| Square root of X | `qc.sx(q)` | Half an X: applied twice it is X. A native gate on many real devices. |
| SX dagger | `qc.sxdg(q)` | Undoes SX. |
| Phase | `qc.p(q, lam)` | Any turn of phase: $\ket{1}$ becomes $e^{i\lambda}\ket{1}$. `p(q, math.pi)` is Z. |
| RX(θ) | `qc.rx(q, theta)` | Rotation by θ radians about the X axis of the Bloch sphere. |
| RY(θ) | `qc.ry(q, theta)` | Rotation by θ radians about the Y axis. |
| RZ(θ) | `qc.rz(q, theta)` | Rotation by θ radians about the Z axis. |
| U | `qc.u(q, theta, phi, lam)` | Any single-qubit gate, from three angles, in the same convention as Qiskit. |

U is the general case. Every other gate in this table is U with particular angles, up to an overall phase:

$$
U(\theta, \varphi, \lambda) = \begin{pmatrix} \cos\tfrac{\theta}{2} & -e^{i\lambda}\sin\tfrac{\theta}{2} \\ e^{i\varphi}\sin\tfrac{\theta}{2} & e^{i(\varphi+\lambda)}\cos\tfrac{\theta}{2} \end{pmatrix}
$$

## Gates on two or more qubits

| Gate | Method | What it does |
| --- | --- | --- |
| CNOT | `qc.cx(control, target)` | Flips the target when the control is $\ket{1}$. |
| Controlled Y | `qc.cy(control, target)` | Applies Y to the target when the control is $\ket{1}$. |
| Controlled Z | `qc.cz(control, target)` | Flips the phase of $\ket{11}$. Either qubit can be the control. |
| Controlled Hadamard | `qc.ch(control, target)` | Applies H to the target when the control is $\ket{1}$. |
| Controlled phase | `qc.cp(control, target, lam)` | Multiplies $\ket{11}$ by $e^{i\lambda}$. Either qubit can be the control. |
| Controlled RX, RY, RZ | `qc.crx(control, target, theta)`, `qc.cry(…)`, `qc.crz(…)` | Rotates the target about X, Y or Z by θ when the control is $\ket{1}$. |
| SWAP | `qc.swap(qubit1, qubit2)` | Exchanges the states of two qubits. |
| RXX, RYY, RZZ | `qc.rxx(qubit1, qubit2, theta)`, `qc.ryy(…)`, `qc.rzz(…)` | $e^{-i\theta\, P \otimes P / 2}$ for $P$ = X, Y or Z. RZZ multiplies each basis state by $e^{-i\theta/2}$ when the two bits agree and $e^{i\theta/2}$ when they differ. These are the building blocks of QAOA and of simulating spin models. |
| Toffoli | `qc.ccx(control1, control2, target)` | Flips the target when both controls are $\ket{1}$. |
| Fredkin | `qc.cswap(control, qubit1, qubit2)` | Swaps the two qubits when the control is $\ket{1}$. |
| Multi-controlled X | `qc.mcx(controls, target)` | Flips the target when every qubit in the list `controls` is $\ket{1}$, for any number of controls. `mcx([c], t)` is `cx(c, t)` and `mcx([c1, c2], t)` is `ccx(c1, c2, t)`. |

SWAP, RXX, RYY, RZZ and Fredkin run as a few of the simpler gates (SWAP as three CNOTs, RZZ as CNOT, RZ, CNOT), but each is one operation in `len(qc)` and in the drawing. Here SWAP moves a 1 from qubit 0 to qubit 2:

```python
qc = qsengine.QuantumCircuit(3)
qc.x(0)
qc.swap(0, 2)
print(qc.run(shots=100, seed=0))
```

```output
{'100': 100}
```

## Your own gates

`qc.unitary(matrix, target, controls=[])` applies any 2 by 2 unitary matrix, given as nested lists or a NumPy array. With `controls`, it applies only where every control qubit is $\ket{1}$. This applies the square root of X twice, which makes a full X (the same as `qc.sx(0)` twice, written out as a matrix):

```python
import numpy as np
import qsengine

sx = np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2

qc = qsengine.QuantumCircuit(1)
qc.unitary(sx, 0)
qc.unitary(sx, 0)
print(qc.probabilities())
```

```output
[0. 1.]
```

A matrix that is not unitary raises `ValueError`, so a typo cannot quietly break the state. A matrix that is unitary to within 1e-9, such as one computed with floating-point arithmetic, is accepted and replaced by the nearest exactly unitary matrix, so small rounding errors cannot add up over a long circuit.

## Rules every gate follows

- A qubit number must be at least 0 and less than the circuit’s `num_qubits`.
- A gate on several qubits needs different qubits: `qc.cx(1, 1)` raises `ValueError`.
- A gate that raises is not recorded, so the circuit stays as it was.

## Combining gates

Gates apply in the order you add them. These lines make a three-qubit GHZ state:

```python
qc = qsengine.QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
```

Runs of single-qubit gates on the same qubit are merged into one before the simulation runs, so a long chain of rotations costs one pass over the state, not one per gate.

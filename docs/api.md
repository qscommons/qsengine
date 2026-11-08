---
home: true
---

# API reference

The whole public API is one class, `qsengine.QuantumCircuit`, and a version string. Backends are chosen with the `backend` argument: `"auto"`, `"cpu"` or `"gpu"`.

```python
import qsengine

qc = qsengine.QuantumCircuit(2)
```

## QuantumCircuit

<a id="init"></a>

### `QuantumCircuit(num_qubits, num_clbits=0)`

Create an empty circuit on num_qubits qubits, all starting in |0⟩, and num_clbits classical bits, all starting at 0. At most 30 qubits and 64 classical bits.

Raises ValueError if either is above its maximum.

<a id="num-qubits"></a>

### `qc.num_qubits`, `qc.num_clbits`

The number of qubits and of classical bits. Read-only.

Returns int.

<a id="len"></a>

### `len(qc)`

The number of operations recorded so far: gates, measurements and resets. A swap counts as one.

Returns int.

<a id="str"></a>

### `print(qc)`, `str(qc)`

A text drawing of the circuit, one wire per qubit with qubit 0 on top. ● marks a control, × the ends of a swap.

Returns str.

<a id="single"></a>

### `qc.h(q)`, `qc.x(q)`, `qc.y(q)`, `qc.z(q)`, `qc.s(q)`, `qc.sdg(q)`, `qc.t(q)`, `qc.tdg(q)`

Record a single-qubit gate on qubit q.

Raises ValueError if q is out of range.

<a id="rotations"></a>

### `qc.rx(q, theta)`, `qc.ry(q, theta)`, `qc.rz(q, theta)`, `qc.p(q, lam)`

Record a rotation of theta radians about the X, Y or Z axis, or a phase of lam radians.

Raises ValueError if q is out of range or the angle is NaN or infinite.

<a id="u"></a>

### `qc.u(q, theta, phi, lam)`

Record the general single-qubit gate U, in the same convention as Qiskit.

Raises ValueError if q is out of range or an angle is NaN or infinite.

<a id="two-qubit"></a>

### `qc.cx(control, target)`, `qc.cz(control, target)`, `qc.cp(control, target, lam)`, `qc.crz(control, target, theta)`

Record a CNOT, controlled-Z, controlled-phase or controlled-RZ gate.

Raises ValueError if a qubit is out of range, control equals target, or an angle is NaN or infinite.

<a id="swap"></a>

### `qc.swap(qubit1, qubit2)`

Record a SWAP, as three CNOTs.

Raises ValueError if a qubit is out of range or the two are equal.

<a id="ccx"></a>

### `qc.ccx(control1, control2, target)`

Record a Toffoli gate.

Raises ValueError if a qubit is out of range or used twice.

<a id="measure"></a>

### `qc.measure(qubit, clbit)`

Measure qubit into classical bit clbit, part-way through the circuit or at the end. Both may be equal-length lists, as in `qc.measure([0, 1], [0, 1])`, of Python or NumPy integers.

Raises ValueError if a qubit or classical bit is out of range, or inside if_test.

<a id="reset"></a>

### `qc.reset(qubit)`

Put qubit back to |0⟩, whatever state it is in, so it can be used again.

Raises ValueError if qubit is out of range, or inside if_test.

<a id="if-test"></a>

### `with qc.if_test(clbits, value):`

Gates added inside the block run only in shots where the classical bits equal value. clbits is one classical bit or a list; bit i of value is the value required of `clbits[i]`.

Raises ValueError if a classical bit is out of range, value does not fit, or blocks are nested.

<a id="unitary"></a>

### `qc.unitary(matrix, target, controls=[])`

Record any 2x2 unitary matrix (nested lists or a NumPy array) on target, applied only where every qubit in controls is |1⟩. A matrix within 1e-9 of unitary is replaced by the nearest unitary matrix.

Raises ValueError if the matrix is not 2x2 or not unitary, or a qubit is out of range or used twice.

<a id="run"></a>

### `qc.run(shots=1024, seed=None, backend="auto")`

Simulate the circuit shots times and count the results. If the circuit measures, the bitstrings are its classical bits; otherwise every qubit is measured at the end. A circuit that measures part-way is simulated once per shot. Pass seed for repeatable counts.

Returns `dict[str, int]` mapping bitstrings (bit 0 on the right) to counts.

<a id="probabilities"></a>

### `qc.probabilities(backend="auto")`

Simulate the circuit and return the probability of each of the 2ⁿ basis states, computed rather than sampled. Measurements at the very end are ignored. With `backend="auto"` the result has 32-bit precision from 14 qubits when a GPU is present; pass `backend="cpu"` for 64-bit.

Returns a NumPy float64 array. Raises ValueError if the circuit measures or resets before a later gate.

<a id="statevector"></a>

### `qc.statevector(backend="auto")`

Simulate the circuit and return the amplitudes, computed rather than sampled. Measurements at the very end are ignored. With `backend="auto"` the result has 32-bit precision from 14 qubits when a GPU is present; pass `backend="cpu"` for 64-bit.

Returns a NumPy complex128 array. Raises ValueError if the circuit measures or resets before a later gate.

<a id="expectation"></a>

### `qc.expectation(paulis, backend="auto")`

The expectation value of a Pauli string such as `"ZZI"` (one letter per qubit, qubit 0 on the right), or of each string in a list, from one simulation.

Returns float for one string, a NumPy float64 array for a list. Raises ValueError for a string of the wrong length or with letters other than I, X, Y, Z.

<a id="version"></a>

### `qsengine.__version__`

The installed version.

Returns str, for example `"{{version}}"`.

## Errors

Invalid input raises immediately, on the line that caused it, and the gate is not recorded. These are the exact messages:

| Call | Raises |
| --- | --- |
| `QuantumCircuit(31)` | `ValueError: requested 31 qubits, maximum is 30` |
| `qc.h(2)` on 2 qubits | `ValueError: qubit 2 out of range for a 2-qubit register` |
| `qc.cz(0, 0)` | `ValueError: qubit 0 used more than once in one gate` |
| `qc.rx(0, float("nan"))` | `ValueError: gate angles must be finite numbers, not NaN or infinity` |
| `qc.unitary([[1, 1], [0, 1]], 0)` | `ValueError: gate matrix must be a 2x2 unitary` |
| `qc.measure(0, 1)` with 1 classical bit | `ValueError: classical bit 1 out of range for a circuit with 1 classical bits` |
| `qc.statevector()` after a mid-circuit measurement | `ValueError: the circuit measures or resets a qubit before a later gate, so its final state is random; use run()` |
| `qc.expectation("ZQ")` | `ValueError: Pauli string "ZQ" may only contain I, X, Y and Z` |
| `qc.unitary(numpy.eye(4), 0)` | `ValueError: matrix must be 2x2` |
| `qc.run(backend="tpu")` | `ValueError: unknown backend "tpu"; expected "auto", "cpu" or "gpu"` |
| `qc.x(-1)` | `OverflowError: can't convert negative int to unsigned` |
| `backend="gpu"` with no usable GPU | `RuntimeError`, with the reason from the driver |
| A state too large for memory | `MemoryError: not enough memory for the state vector (16.0 GiB)` |

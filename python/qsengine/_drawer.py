"""Text drawing for `print(qc)`: one wire per qubit (q0 on top), one column per operation.

    q0: ──H──●─
             │
    q1: ─────X─

`●` marks a control, `×` the two ends of a swap, `M→c0` a measurement into
classical bit 0, `|0⟩` a reset, and `X if c1=1` a gate inside an `if_test`.
A gate on a pair of qubits (`rzz`, `rxx`, `ryy`) draws its label on both.

A drawing wider than FOLD characters continues in a new block below, separated
by a blank line, so long circuits stay readable in a terminal or notebook.

shortcut: columns are never packed, so gates on different qubits still take one column each.
"""

FOLD = 80  # characters per line before the drawing continues below

# Method name -> symbol drawn on the target wire.
SYMBOLS = {
    "x": "X", "y": "Y", "z": "Z", "h": "H", "s": "S", "t": "T", "sdg": "S†", "tdg": "T†",
    "rx": "RX", "ry": "RY", "rz": "RZ", "p": "P", "u": "U", "unitary": "U",
    "sx": "√X", "sxdg": "√X†",
    "cx": "X", "cy": "Y", "cz": "Z", "ch": "H", "cp": "P", "crx": "RX", "cry": "RY", "crz": "RZ",
    "ccx": "X", "mcx": "X", "swap": "×", "cswap": "×", "rxx": "RXX", "ryy": "RYY", "rzz": "RZZ",
}


def _label(kind, name, params, condition, clbit):
    if kind == "measure":
        return f"M→c{clbit}"
    if kind == "reset":
        return "|0⟩"
    text = SYMBOLS[name]
    if params:
        text += "(" + ",".join(f"{a:.2f}" for a in params) + ")"
    if condition is not None:
        mask, value = condition
        bits = [b for b in range(mask.bit_length()) if mask >> b & 1]
        text += " if " + ",".join(f"c{b}={value >> b & 1}" for b in bits)
    return text


def draw(circuit) -> str:
    n = circuit.num_qubits
    name_w = len(f"q{max(n - 1, 0)}")
    # Even rows are qubit wires, odd rows the gaps between them.
    names = [f"{f'q{r // 2}':>{name_w}}: ─" if r % 2 == 0 else " " * (name_w + 3) for r in range(max(2 * n - 1, 0))]
    blocks, rows = [], list(names)

    for kind, name, params, controls, targets, condition, clbit in circuit._ops():
        label = _label(kind, name, params, condition, clbit)
        # A gate with two targets (swap, cswap, rxx, ryy, rzz) draws on both, its condition (if any) only on the first.
        marks = {t: _label(kind, name, params, None, clbit) for t in targets[1:]} | {targets[0]: label}
        w = max(len(m) for m in marks.values()) + 2
        mid = w // 2
        qubits = controls + targets
        lo, hi = 2 * min(qubits), 2 * max(qubits)  # rows that carry the vertical line

        def at(ch, fill):
            return fill * mid + ch + fill * (w - mid - 1)

        # Start a new block when this column would overflow the line, unless the block is still empty.
        if rows and len(rows[0]) + w > FOLD and len(rows[0]) > len(names[0]):
            blocks.append(rows)
            rows = list(names)
        for r in range(len(rows)):
            q, inside = r // 2, lo <= r <= hi
            if r % 2 == 0 and q in marks:
                cell = ("─" + marks[q]).ljust(w, "─")
            elif r % 2 == 0 and q in controls:
                cell = at("●", "─")
            elif r % 2 == 0:
                cell = at("┼", "─") if inside else "─" * w
            else:
                cell = at("│", " ") if inside else " " * w
            rows[r] += cell
    blocks.append(rows)
    return "\n\n".join("\n".join(row.rstrip() for row in block) for block in blocks)

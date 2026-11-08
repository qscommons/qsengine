# qsengine documentation

This folder is the qsengine documentation. Every page here is published on [qsengine.kaiwave.dev/docs](https://qsengine.kaiwave.dev/docs/), and reads the same on GitHub. When you change how qsengine behaves, change the page that describes it in the same pull request.

The list below is the table of contents. The site builds its sidebar, its docs index and the links on its home page from it, in this order. Pages marked with `home: true` at the top are also listed on the home page.

## Getting started

- [Installation and first circuit](getting-started.md): Install the wheel, build a Bell state, read the counts.
- [Examples](examples.md): Complete programs with their real output.

## Quantum physics

- [Qubits and bra-ket notation](learn/qubits.md): What a qubit is and how to write its state.
- [Measurement](learn/measurement.md): Amplitudes, probabilities, shots and phase.
- [The Bloch sphere](learn/bloch-sphere.md): One qubit as a point on a sphere; gates as rotations.
- [Many qubits](learn/many-qubits.md): Tensor products, 2ⁿ amplitudes and bit order.
- [Entanglement](learn/entanglement.md): Bell states, step by step, and why they cannot be split.
- [The Deutsch-Jozsa algorithm](learn/deutsch-jozsa.md): A whole quantum algorithm, built and run with qsengine.

## User guide

- [Gates](gates.md): Every gate, the method that applies it, and your own unitaries.
- [Running circuits](running.md): Shots and counts, exact states, seeds and bit order.
- [CPU and GPU backends](backends.md): Precision, hardware and how auto chooses.

## Reference

- [API reference](api.md): QuantumCircuit, every method, every error.
- [Benchmarks](benchmarks.md): qsengine against pure Python and Qiskit Aer, up to 22 qubits.

## Help

- [Questions](faq.md): Short answers to common questions.
- [Release notes](release-notes.md): What is in version {{version}}.

# Writing a page

Pages are GitHub Markdown, with a few conventions the site understands. To add a page, create the file and add a line for it to the list above; the site build fails if a page is missing from the list or the list names a file that does not exist.

- **Title.** The page's `# Heading` is its title. The `## Headings` become the sections listed under the page in the sidebar.
- **Home page.** To list a page on the site's home page, start it with:

  ```
  ---
  home: true
  ---
  ```

- **Links.** Link to other pages by their file, `[Gates](gates.md#your-own-gates)`, and to other files in the repository by relative path, `[results.csv](../benchmarks/results.csv)`. Both work on GitHub and on the site.
- **Maths.** `$\ket{0}$` inline, and a block between two lines of `$$`. The site renders it with KaTeX and fails the build on a broken formula.
- **Program output.** Show what a snippet prints in an `output` block right after it. Re-run the code and paste the real output after any release that changes behaviour.

  ````
  ```output caption="Only 00 and 11 appear." bars="00:513 01:0 10:0 11:487"
  {'00': 513, '11': 487}
  ```
  ````

  `caption` and `bars` are optional. `bars` draws one bar per `label:value`, each against the sum of all values.
- **Version.** `{{version}}` is replaced with the version in Cargo.toml.
- **Anchors.** `<a id="name"></a>` on its own line gives a fixed link target. Keep the ids of existing anchors, since other sites may link to them.
- **HTML.** Other HTML must be valid JSX (self-closed tags such as `<br />`). `{` and `}` in ordinary text are fine.

To preview the site with your changes, run `npm install` once and then `npm run dev` in `site/`; it rebuilds pages as you edit files here.

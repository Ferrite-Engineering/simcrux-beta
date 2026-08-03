# SimCrux Test Fixtures

**This is what SimCrux tests against.** Every directory here is part of the
SimCrux test suite — each one has a known-correct expected result committed
beside it, and config parsing, process orchestration, pass/fail detection, the
RISC-V compatibility and formal flows, and the Pro analyses are validated
against it on every change. We publish the corpus so you can see exactly how
SimCrux is verified, run the cases yourself, and
[contribute your own](../docs/SUBMITTING_FIXTURES.md).

During the public beta all features are unlocked, so you can open both the
open-core and the Pro fixtures in the app and watch every feature work against
them.

> ⚙️ **This tree is generated.** It's mirrored from the SimCrux test suite by
> tooling — don't edit it here. To contribute a fixture, use the
> **[fixture submission form](../../issues/new?template=fixture_submission.yml)**;
> see [SUBMITTING_FIXTURES.md](../docs/SUBMITTING_FIXTURES.md).

Looking for something to *run* rather than something to read? The
[`examples/`](../examples/) tree next door holds two ready-to-open
`simcrux.yaml` projects, **neither of which needs a simulator or a RISC-V
toolchain installed**. They consume two of the corpora below. See
[`examples/README.md`](../examples/README.md).

## Layout

```
fixtures/
├── open-core/
│   ├── projects/         # 7 runnable regression projects, one directory each
│   ├── orchestration/    # 3 process-behavior scenarios (no simulator needed)
│   ├── fusesoc/          # 3 FuseSoC CAPI2 .core files for the importer
│   ├── golden_compare/   # 8 signature-comparison cases for the detector
│   └── riscv_formal/     # 7 captured SymbiYosys runs, one verdict each
└── pro/
    ├── flaky_detection/  # 6 run histories + expected flakiness classifications
    └── multi_project/    # 2-project workspace with disjoint test namespaces
```

## The fixture shapes

**Regression projects** (`open-core/projects/`, `pro/multi_project/`) are
directories holding a real `simcrux.yaml`, the testbench sources it names, and
a hidden `.expected_results.json` companion listing the status each test must
end up in. These are the only fixtures that need a simulator installed — the
corpus covers Icarus Verilog, Verilator, GHDL, cocotb, and mixed Verilog + VHDL
under cocotb, with matched pass and fail cases so **both** directions of the
pass/fail detector are pinned. A corpus of green cases cannot tell you a
detector reports failure at all.

**Orchestration scenarios** (`open-core/orchestration/`) test process behavior
without running a simulator at all. Each scenario is a `<name>/generated/`
directory with three files: the `simcrux.yaml` input, a `behaviors.json`
scripting a fake process per test (exit code, delay, whether it ignores
`SIGTERM`, how many grandchildren it forks), and an `expected_results.ndjson`
golden — one JSON object per test, in the exact order the scheduler must emit
them, with bucketed durations and the recorded kill *path* rather than only the
outcome. That is how `timeout_then_sigkill` and cocotb's `make` → Python →
simulator process tree (`cocotb_tree_reap`) get pinned deterministically, on
every platform, in milliseconds.

**Detector cases** (`open-core/golden_compare/`) are one directory per case,
each holding a hand-written `case.json` (the description, the comparison
`profile`, the two filenames), the signature dumps themselves, and an
`expected.json` golden written by replaying the real `GoldenCompareDetector`.
Three of the eight are the ones worth reading first: `first_word_mismatch`
diverges at word 0 — the boundary an off-by-one hides; `empty_dut` ships a
zero-byte dump; and `missing_dut` ships **no dump at all**. The last two are
load-bearing absences. Both must report *fail* — never `vacuous`, never
`unknown` — because either of those turns a core that produced no signature
into a green row.

**Captured engine runs** (`open-core/riscv_formal/`) are one directory per
bounded proof: the `sby.log` SymbiYosys wrote, any counterexample or cover
`engine_*/trace*.vcd`, a `case.json` of the run's inputs, and an
`expected.json` golden produced by the **production** log parser and verdict
mapping. The seven cases carry one verdict each — `PASS`, `FAIL`, `UNKNOWN`,
`TIMEOUT`, `ERROR`, a multi-trace cover run, and `liveness_no_outcome`, which is
the sharpest of them: no `DONE (…)` line at all and the process exits **0**.
Classifying from the exit code reports a proof that never happened as a pass.
That corpus carries its own [`README.md`](open-core/riscv_formal/README.md)
explaining each case; the regeneration commands in it run in the SimCrux source
tree, not here.

The Pro directories follow the same idea with analysis-specific companions —
`flaky_detection/generated/` is a deterministic 6-profile × 28-run history in
and a golden classification out, covering every `FlakyClassification` from
`stable` through `highlyFlaky`; `multi_project/` is two tiny Icarus projects
that deliberately share the `regression.yaml` basename and use disjoint
`alu_*` / `fifo_*` namespaces, so display-name disambiguation and per-project
state isolation are both observable.

`fusesoc/` is parse-only: the three `.core` files exercise the CAPI2 importer,
including one target shape it must reject. They name filesets rather than
shipping RTL, which is why there is no `rtl/` directory beside them.

## The two fixture tiers

- **`generated/`** — deterministic fixtures emitted by SimCrux's own
  generators. 100% reproducible; the unit-test backbone.
- **`captured/`** — projects taken from **permissively-licensed open-source
  repositories**, exercising the runners against testbenches nobody on this
  team wrote. Each `captured/` directory carries a **`PROVENANCE.md`**
  recording the source project, version/commit, license, and the simulator
  version used, plus the same expected-result companion.

There is no `captured/` directory in the corpus yet: everything published here
is either hand-authored by us or written by our own generators. Community
submissions land in `captured/`. If we can reproduce your bug with a generator
instead, it becomes a `generated/` case.

## Licensing

Everything in this tree is authored or generated by SimCrux and released into
the public domain (CC0). In particular, the `golden_compare/` signature dumps
and the `riscv_formal/` logs and traces are **hand-authored** — they are
written in the shape `riscv-arch-test` signatures and `sby` output take, because
that is the shape the parsers must handle, but nothing in them is derived from
riscv-arch-test, riscv-formal, SymbiYosys or any other upstream project, and no
third-party attribution obligation is created.

`captured/` fixtures, when they arrive, retain the license of the upstream
project they were derived from — always one of **MIT, BSD-2-Clause,
BSD-3-Clause, Apache-2.0, ISC, CC0, or public domain**. The exact source and
license for each is in that directory's `PROVENANCE.md`. SimCrux's publishing
tool refuses to publish a captured fixture that lacks a provenance record, and
the test suite blocks any fixture outside the license allow-list.

If you reuse a captured fixture, honor the upstream license named in its
`PROVENANCE.md`.

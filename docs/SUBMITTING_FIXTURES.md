# Submitting a Test Fixture

A **fixture** is a small regression project plus the result SimCrux *should*
produce from it. Fixtures are how SimCrux proves its orchestration, pass/fail
detection, and reporting stay correct: every fixture in
[`fixtures/`](../fixtures/) runs in the test suite, so once a project is in, the
behavior it captures can never silently regress.

If you found a project SimCrux runs wrong — a test it calls a pass when it
failed, a hang it doesn't kill, an output format it can't parse — **that project
is the most valuable thing you can give us.** This guide explains how to submit
one and the rules it has to follow.

## The fastest path

1. Open the
   **[fixture submission form](../../issues/new?template=fixture_submission.yml)**.
2. Attach (or link) the smallest project that reproduces it: a `simcrux.yaml`, the
   testbench sources it names (`.v`, `.sv`, `.vhd`, `.py`, a cocotb `Makefile`),
   and nothing else.
3. Tell us the simulator and version, what SimCrux currently does, and what it
   *should* do.
4. Confirm the licensing (below).

We take it from there: trim it, snapshot the expected result, document its
provenance, and fold it into the suite. You'll be credited on the resulting
change.

## What a SimCrux fixture actually looks like

There are two shapes, and picking the right one makes your submission land much
faster.

### 1. A regression project

A directory containing a real `simcrux.yaml` plus the testbench sources it
references, and a hidden `.expected_results.json` companion naming the status
each test must end up in:

```
my_fixture/
├── simcrux.yaml
├── tb_pass.v
└── .expected_results.json      # { "tests": [ { "id": "smoke/pass_basic",
                                #                "expected_status": "pass" } ] }
```

This is the right shape for config parsing, filelist expansion, seed sweeps,
mixed-language routing, and **pass/fail detection** bugs. It needs the simulator
installed to run, so keep it to a single tiny testbench.

### 2. An orchestration scenario

Some of the nastiest bugs are about *process behavior*, not simulation: a test
that ignores `SIGTERM`, a cocotb `make` that forks grandchildren, a timeout that
fires while output is still streaming. Those fixtures don't run a simulator at
all — they script a fake process (exit code, delay, whether it ignores signals,
how many grandchildren it forks) and record the exact results the scheduler must
emit, in order.

If your bug is "SimCrux left processes behind" or "the timeout didn't produce the
status I expected", describe the *process* behavior precisely — that's what we
turn into the scenario.

## What makes a great fixture

- **Small and focused.** One suite, one or two tests, the fewest lines of
  testbench that still reproduce the behavior. We can trim, but a tight project
  is gold.
- **Self-contained.** No vendor IP, no unshippable includes, no dependency on
  your build system. If it doesn't run on a clean machine with a stock
  simulator, it can't be a fixture.
- **A known-correct answer.** The bug isn't "the dashboard looks wrong" — it's
  "`smoke/uvm_error_case` should be reported as a fail because the log contains
  `UVM_ERROR`, and SimCrux reports it as a pass." The more precisely you can
  state the expected result, the faster it becomes a test.
- **Name the simulator and version.** `iverilog -V`, `verilator --version`,
  `ghdl --version`, `cocotb-config --version`. Output formats drift between
  releases, and half of all parsing bugs are version-specific.

## Licensing — please read

Fixtures we publish must be redistributable, because [`fixtures/`](../fixtures/)
is public. We can only accept fixtures under a permissive license:

> **MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, ISC, CC0, or public domain.**

- **Your own hand-written testbench?** Easiest case — by submitting it you agree
  to contribute it under CC0 / public domain so it can live in the test suite.
- **Derived from an open-source project?** Only if that project is under one of
  the licenses above. Tell us the project, the commit/version, and how you ran
  it. We record this as provenance.
- **From proprietary, GPL, or AGPL sources, or anything you can't relicense?**
  We can't accept it — please don't attach it. A *hand-rebuilt* minimal project
  that reproduces the same behavior without copying the original is fine.

Submissions without clear, permissive provenance can't be published, and our
tooling refuses to publish a captured fixture that lacks a provenance record.

## How fixtures are organized

See [`fixtures/README.md`](../fixtures/README.md) for the full layout. In short:

- `generated/` — deterministic scenarios produced by our own generators, each
  with a golden snapshot of the results the scheduler must emit.
- `captured/` — projects taken from **permissively-licensed** open-source
  repositories, each with a `PROVENANCE.md` recording the upstream project,
  commit, license, and the simulator version used.

Your submission typically becomes a new `captured/` entry (with provenance) or a
new `generated/` case if we can reproduce it with a generator.

Thank you — every project you contribute makes SimCrux more correct for everyone.

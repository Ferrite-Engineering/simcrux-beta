# SimCrux Test Fixtures

**This is what SimCrux tests against.** Every project here is part of the SimCrux
test suite — each one has a known-correct expected result, and config parsing,
orchestration, pass/fail detection, and the Pro analyses are validated against it
on every change. We publish the corpus so you can see exactly how SimCrux is
verified, run the projects yourself, and
[contribute your own](../docs/SUBMITTING_FIXTURES.md).

During the public beta all features are unlocked, so you can open both the
open-core and the Pro fixtures in the app and watch every feature work against
them.

> ⚙️ **This tree is generated.** It's mirrored from the SimCrux test suite by
> tooling — don't edit it here. The corpus is published as the beta opens up; the
> layout below is the shape it takes, and the shape a submission should follow.
> To contribute a fixture, use the
> **[fixture submission form](../../issues/new?template=fixture_submission.yml)**;
> see [SUBMITTING_FIXTURES.md](../docs/SUBMITTING_FIXTURES.md).

## Layout

```
fixtures/
├── open-core/
│   ├── projects/         # Runnable regression projects, one directory each
│   ├── orchestration/    # Process-behavior scenarios (no simulator required)
│   └── fusesoc/          # FuseSoC CAPI2 .core files for the importer
└── pro/
    ├── flaky_detection/  # Run histories + expected flakiness classifications
    └── multi_project/    # Multi-project workspace registry fixtures
```

## The two fixture shapes

**Regression projects** (`projects/`, `multi_project/`) are directories holding a
real `simcrux.yaml`, the testbench sources it names, and a hidden
`.expected_results.json` companion listing the status each test must end up in.
These need the simulator installed — the corpus covers Icarus Verilog, Verilator,
GHDL, cocotb, and mixed Verilog + VHDL, with matched pass and fail cases so both
directions of the pass/fail detector are pinned.

**Orchestration scenarios** (`orchestration/`) test process behavior without
running a simulator at all. Each scenario is a `<name>/generated/` directory with
three files: the `simcrux.yaml` input, a `behaviors.json` scripting a fake
process per test (exit code, delay, whether it ignores `SIGTERM`, how many
grandchildren it forks), and an `expected_results.ndjson` golden — one JSON
object per test, in the exact order the scheduler must emit them. That's how the
timeout-then-`SIGKILL` path and cocotb's `make` → Python → simulator process tree
get pinned deterministically, on every platform, in milliseconds.

The Pro directories follow the same idea with analysis-specific companions — a
run history in and a golden classification out.

## The two fixture tiers

- **`generated/`** — deterministic fixtures emitted by SimCrux's own generators.
  100% reproducible; the unit-test backbone.
- **`captured/`** — projects taken from **permissively-licensed open-source
  repositories**, exercising the runners against testbenches nobody on this team
  wrote. Each `captured/` directory carries a **`PROVENANCE.md`** recording the
  source project, version/commit, license, and the simulator version used, plus
  the same expected-result companion.

Community submissions land in `captured/`. If we can reproduce your bug with a
generator instead, it becomes a `generated/` case.

## Licensing

`generated/` fixtures are produced by SimCrux's own generators and are released
into the public domain (CC0).

`captured/` fixtures retain the license of the upstream project they were derived
from — always one of **MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, ISC, CC0, or
public domain**. The exact source and license for each is in that directory's
`PROVENANCE.md`. SimCrux's tooling refuses to publish a captured fixture that
lacks a provenance record, and the test suite blocks any fixture outside the
license allow-list.

If you reuse a captured fixture, honor the upstream license named in its
`PROVENANCE.md`.

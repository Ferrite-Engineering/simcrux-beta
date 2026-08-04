# SimCrux Examples

**Neither example needs a simulator, a RISC-V toolchain, or a network.** Clone
this repo, open one config, press run, and a real regression report appears —
with a genuine mixed pass/fail spread. That is the whole point of them: nothing
to install first, and nothing uniformly green at the end.

These are configs you *run*. Everything in [`fixtures/`](../fixtures/) exists to
be checked by the test suite; everything here exists to be opened by you.

> ⚙️ **This tree is generated.** It's mirrored from the SimCrux source tree by
> tooling — don't edit it here. One thing *is* rewritten on the way out: each
> config's demo-corpus path is repointed at this repo's copy of the corpus under
> [`fixtures/open-core/`](../fixtures/open-core/), which is the same committed
> fixture the test suite runs against. The publishing tool resolves every
> rewritten path and refuses to ship an example that would not run.

## Run one in three steps

1. **File → Open Config…** (`Cmd/Ctrl+O`, or the folder button at the left of
   the toolbar) and pick the `simcrux.yaml` in one of the directories below.
2. **Tools → Run Regression** (`F5`, or the run button on the toolbar).
3. Watch the rows land. `Esc` — **Tools → Cancel Regression** — stops a run.

There is no "Run" menu: opening lives under **File**, running lives under
**Tools**.

Each config is also a positional argument, so you can skip step 1:

```bash
simcrux examples/riscv-formal-demo/simcrux.yaml
```

## The examples

| Example | What it demonstrates | Needs a toolchain? |
|---|---|---|
| [`riscv-compatibility-demo/`](riscv-compatibility-demo/simcrux.yaml) | The `riscv_arch` driver and the `golden_compare` detector running the RISC-V architectural-compatibility flow against a committed signature corpus. 8 tests, **3 pass / 5 fail**, in four extension suites. | **No** |
| [`riscv-formal-demo/`](riscv-formal-demo/simcrux.yaml) | The `riscv_formal` driver replaying committed SymbiYosys outputs — one bounded proof per test, with the four-way PASS / FAIL / UNKNOWN / TIMEOUT verdict distinction. 7 tests, **2 pass / 5 fail**. | **No** |

## Why they need nothing installed

Both run in `mode: demo`, declared **in the config, never in the environment**.
Demo mode skips only the *spawn* steps and proceeds through the identical
signature reading, log parsing, comparison, metric emission and event
construction as a real run. It is the same driver, not a stand-in — an
env-gated separate driver would exercise a different code path, and then the
demo would be evidence about nothing. So you need:

- no RISC-V cross-compiler (`riscv32-unknown-elf-gcc`),
- no reference model (Spike or Sail),
- no `riscv-arch-test` or `riscv-formal` checkout,
- no SymbiYosys, Yosys or SMT solver,
- and no network.

That claim is not asserted, it is *enforced*: both configs are executed end to
end in the SimCrux test suite through the real `ConfigLoader` and the real
`LocalJobScheduler`, with a process launcher that **throws if anything is ever
spawned**, and the pass/fail spread is checked per test by name in both
directions. The same check was run against the published copies in this repo
before they shipped.

This is where SimCrux differs from its siblings: NetCrux needs a live Yosys to
draw anything, so it has no toolchain-free entry point. SimCrux has two.

## Neither example is all-green, on purpose

A report that shows only passes demonstrates nothing. Both corpora are shaped
around the cases where a naive implementation goes quietly wrong.

**`riscv-compatibility-demo`** — 8 tests in four extension suites, so the
per-extension rollup has one mixed group, two all-failing groups and one
all-passing group:

| Suite | Test | Result | Why it is in the corpus |
|---|---|---|---|
| `I` | `clean_pass` | pass | identical signatures |
| `I` | `first_word_mismatch` | fail | diverges at word 0 — the boundary an off-by-one hides |
| `M` | `mid_file_mismatch` | fail | diverges mid-file |
| `M` | `length_mismatch` | fail | the DUT signature is a prefix of the reference |
| `C` | `empty_dut` | fail | an empty DUT dump must never report `vacuous` |
| `C` | `missing_dut` | fail | a missing DUT dump must never report `unknown` |
| `Zicsr` | `format_variance_riscv` | pass | read under `profile: riscv_signature` |
| `Zicsr` | `format_variance_generic` | pass | the *same bytes*; they report `fail` only under `profile: generic`, and this driver is ISA-coupled by construction |

**`riscv-formal-demo`** — 7 tests, one verdict each. The four-way distinction is
exactly what reading an exit code collapses, and collapsing it is how a broken
core goes green:

| Suite | Test | Verdict | Result |
|---|---|---|---|
| `insn` | `insn_add_pass` | `PASS` | pass |
| `insn` | `insn_sub_counterexample` | `FAIL` | fail — with the counterexample VCD SymbiYosys wrote |
| `pc_fwd` | `pc_fwd_unknown` | `UNKNOWN` | fail — nothing proved, nothing refuted |
| `reg` | `reg_timeout` | `TIMEOUT` | fail — SymbiYosys's own solver budget expired, deliberately *not* the status that means SimCrux killed the job |
| `causal` | `causal_error` | `ERROR` | fail — Yosys could not read a source, so the proof never ran |
| `liveness` | `liveness_no_outcome` | `NO_OUTCOME` | fail — no `DONE (…)` line at all and the process exits **0**; reading the exit code would report a proof that never happened as a pass |
| `cover` | `cover_multi_trace` | `PASS` | pass — two cover statements reached, one trace each |

## What to click once the rows land

- Select a row and open the **Inspector** (**View → Toggle Inspector**,
  `Cmd/Ctrl+2`) for that test's status, metrics and **Open full log**. The
  formal demo's per-test metrics carry the raw `PASS` / `UNKNOWN` / `TIMEOUT` /
  `ERROR` / `NO_OUTCOME` verdict, which is what the failure rows are for.
- The **Test Browser** (**View → Toggle Test Browser**, `Cmd/Ctrl+1`) and the
  **Log Panel** (**View → Toggle Log Panel**, `Cmd/Ctrl+3`) toggle the same way.
- On `insn/insn_sub_counterexample`, the Inspector's **Debug in WaveCrux**
  button hands the counterexample trace to WaveCrux over cross-probe. It needs
  WaveCrux running with cross-probe enabled (Settings → CXP Cross-Probe); the
  app tells you if no peer is connected.

## Pointing them at a real core

Each config ends with a note on the switch. In both cases it is `mode: normal`
plus the plumbing that mode needs — for compatibility, your DUT command, the
arch-test suite and a reference model; for formal, the `checks/` directory
riscv-formal's `genchecks.py` writes. There is **no `simcrux import` command
for either yet**, so the per-test entries are hand-written today. The YAML is
yours to read, diff and commit either way — which is the point.

Nothing on the `riscv:` path is tier-gated, in any tier, ever: a compatibility
verdict is correctness, and correctness is free.

## Found a bug in one of these?

That's a good find — an example failing is a bug report with the reproduction
already attached, and these two need no toolchain, so we can reproduce it
exactly. [File an issue](../../issues/new?template=bug_report.yml), name the
example, and paste the row that went the wrong way.

# SimCrux Release Notes

All notable changes between beta builds. New builds are announced in
[Discussions → Announcements](../../discussions/categories/announcements), which
is also where the download links are posted while the beta is opening up.

---

## 0.6.0 — 2026-08-04

A RISC-V release. SimCrux can now answer two questions a core team asks
constantly: *does this core actually implement the ISA it claims?* and *does
this property hold?* Both arrive with dashboards, an exportable report, and —
when something fails — a counterexample that opens in WaveCrux on the exact
cycle.

### New

- **RISC-V compatibility checking.** A new `riscv:` block in your project runs
  the `riscv_arch` driver against your core and reports which extensions and
  behaviours it genuinely implements versus what it advertises. It runs in demo
  mode with no toolchain installed, so you can see the shape of the result
  before committing to a setup.
- **The Compatibility Dashboard (Pro).** A rollup across your configurations,
  the core's own ISA attestation, and a signature diff showing exactly where
  the implementation and the claim part company.
- **An exportable compatibility report (Pro).** Provenance included — which
  core, which toolchain, which run produced each result — so the artifact is
  something you can hand to someone else and have it mean something.
- **Bounded formal proofs.** The `riscv_formal` driver runs property proofs on
  the existing job model, so proofs schedule and report like any other job.
  Pro adds a **formal property dashboard** for the results.
- **Counterexamples open in WaveCrux on the failing step.** When a proof fails,
  the trace hands off with the relevant signals already on the canvas. If the
  hand-off cannot land precisely, SimCrux now says so rather than leaving you
  to wonder whether the cycle it picked was meaningful.
- **`golden_compare` pass/fail detector.** Compare a DUT against a golden
  reference and get the first divergent word, not a wall of diff.
- **Two RISC-V demo projects that open with no toolchain.**

### Fixed

- **The dashboard's centre pane stops overflowing** at ordinary window sizes.
- **Driver resolution keeps looking** past a plugin that declines a job,
  instead of stopping there.
- **The orchestration example project loads** — its corpus was incomplete.
- **The formal demo corpus ships** — a `.gitignore` rule had been eating its
  logs.

### Also

- **Linux requirements are now measured, not asserted.** Our published glibc
  figure had drifted from what we actually shipped; every release build now
  verifies it. SimCrux requires glibc 2.34, which means it runs on RHEL /
  Rocky / AlmaLinux 9, Ubuntu 22.04+ and Debian 12+.
- Other performance and quality enhancements.

---

## 0.5.0 — 2026-07-31

The release that makes two half-reachable features fully reachable — plugin
management and PR annotation — and stops long regression runs from quietly
filling your disk.

### New

- **Manage simulator plugins from inside SimCrux.** Install one from a `.zip`,
  enable or disable it, inspect its manifest, and uninstall it. Previously a
  plugin was something you placed on disk and hoped about.
- **Waveform retention that survives a restart.** A sweeper plus a retention
  policy, with a waveform-runs setting, so a long regression campaign stops
  accumulating waveform artifacts indefinitely.
- **PR annotation is reachable.** The Settings UI and dispatch wiring landed,
  so annotating a pull request with regression results is something you can
  turn on rather than a seam with no front door.
- **A live statistics strip** with job-scheduler segments, and per-pane
  dashboard paint timing, so you can see where a slow dashboard is spending
  its time.
- **App Diagnostics has an opener.** The dialog existed but nothing in the UI
  could reach it; it is now a menu item.

### Fixed

- **Simulator binaries default to your system install**, not to a bundled
  location that does not exist — the single most likely reason a fresh
  install failed to find `iverilog` or `verilator`.
- **Icarus and Verilator are found on Windows.** SimCrux now augments the
  persistent PATH to locate the simulators.
- **Driver resolution keeps looking past a plugin that declines** a config,
  instead of giving up at the first refusal.
- **A run whose tab closed under it no longer loads.**
- **The welcome screen scrolls** rather than clipping its recent-projects list
  on a short window.
- **Quit works from every route.** The menu item did nothing on some screens.
- **A sensible minimum window size** (800×500) on macOS, Windows and Linux,
  so the layout can no longer be crushed into an unusable state.

### Also

- **One consistent suite.** The menu bar, toolbar, status bar and Settings are
  now shared components across all four apps, and panels moved to a
  VS Code-style dock model: bottom, right and left regions, tabs you can drag
  between docks, restore bars for collapsed regions, and direction-aware hide
  controls. Run moved out of the File menu to where it belongs, and the
  stacked duplicate status strip is gone. The welcome screen gained an
  animated app logo and now shows the running version — handy in the browser,
  where there is no menu bar to check.
- Other performance and quality enhancements.

> **A note on version numbers.** SimCrux desktop builds shipped as part of the
> 2026.07 suite beta before this file caught up. The app now reports `0.5.0`,
> matching its three siblings and the suite release it ships in.

---

## Unreleased — 0.1.0

The first public beta. Notes land here the day it ships; until then this file is
the placeholder that tells you where to look.

What 0.1.0 is expected to cover, so you know what to point at it:

- **Regression orchestration** driven by a `simcrux.yaml` in your project —
  suites, tests, per-test defaults, seed sweeps, and filelist expansion — running
  **Icarus Verilog**, **Verilator**, **GHDL**, and **cocotb** in parallel with
  per-test timeouts, sandboxed work directories, and reliable process-tree
  cleanup on cancel or timeout.
- **Live results dashboard** — filter bar, results table, test browser, status
  heatmap, and a streaming log panel while the run is in flight.
- **Drill-in** — per-test detail with the full log, a searchable log viewer, and
  an inspector that shows the test's recent pass/fail history as a sparkline.
- **Configurable pass/fail detection**, including composite detector trees,
  reusable named detectors, and a UVM report parser.
- **Re-run** failed or selected tests, with a configurable retry policy.
- **Export** to JUnit XML, JSON, CSV, and HTML, plus a self-contained dashboard
  bundle you can host.
- **CLI and CI mode** — run headless, filter, export, and fail the build on
  regressions.
- **FuseSoC `.core` import** — synthesize a `simcrux.yaml` from an existing CAPI2
  core file.
- **Cross-probing over CXP**, including **Debug in WaveCrux** — send a failing
  test's captured waveform straight to a running WaveCrux.
- Linux, macOS, and Windows, plus a read-only web dashboard that loads an
  exported results bundle.
- Four display languages: English, 简体中文, 日本語, 한국어.

Pro-tier features — flaky-test detection and scoring, trend charts and the
calendar heatmap, seed-sweep parameterization with the seed-failure heatmap,
baselines and regression comparison, multi-project workspaces, PR annotation for
GitHub / GitLab / webhooks, and the subprocess simulator-driver plugin SDK — are
**unlocked for everyone during the beta**, and carry a `PRO` badge so you can
tell which is which.

# SimCrux Release Notes

All notable changes between beta builds. New builds are announced in
[Discussions → Announcements](../../discussions/categories/announcements), which
is also where the download links are posted while the beta is opening up.

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

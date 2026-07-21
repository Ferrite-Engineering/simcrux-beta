# SimCrux Public Beta — Participant Guide

Thanks for taking part in the SimCrux public beta. This guide explains what the
beta is, how to get the most out of it, and how your feedback turns into a better
release.

## What the beta is

SimCrux is in **free, all-features-unlocked public beta**. Every capability —
including the Pro features (flaky detection, trend charts, seed-sweep
parameterization, baselines and regression comparison, multi-project workspaces,
PR annotation, the driver-plugin SDK) — is enabled for every beta user, with no
license key required. Pro features still carry a `PRO` badge so you know which
tier they'll land in; during the beta the badge is information, not a gate.

The application source is closed during the beta. This repository
(`simcrux-beta`) is the public channel for bug reports, feature requests, help,
and the test-fixture corpus.

## Installing

Download the latest beta build for your platform from the SimCrux website; new
builds are announced in
[Discussions → Announcements](../../discussions/categories/announcements). Beta
builds self-identify in **Help → About SimCrux** — the version and build SHA are
one click away via **Copy Version Info**, and the in-app reporter fills them in
for you.

Supported platforms: **Linux**, **macOS**, and **Windows**. There is also a
**read-only web dashboard** that loads an exported results bundle in the
browser — browsers can't spawn simulators, so orchestration is desktop-only.

### You bring the simulators

SimCrux doesn't bundle a simulator. It drives the tools you already have:

| Simulator | What SimCrux runs |
|---|---|
| **Icarus Verilog** | `iverilog` to compile, `vvp` to execute |
| **Verilator** | `verilator --cc`, the C++ build, then the executable — modelled as one test |
| **GHDL** | analyse / elaborate / run for VHDL |
| **cocotb** | your existing cocotb `Makefile`, with the summary table parsed back |

Anything else — Questa, Xcelium, VCS, xsim — is **not** supported today. Pro
ships a subprocess driver-plugin SDK so a driver can live outside the app, but no
commercial-simulator driver ships with SimCrux.

Telling us the simulator version in a bug report is the single highest-value line
you can add.

## What's most useful to test

All feedback is welcome, but these areas move the needle most during beta:

- **Point it at a real regression.** A `simcrux.yaml` describing your actual
  suites, run against your actual testbenches. Tell us what's awkward to express,
  what the config can't say, and what you had to work around.
- **Orchestration under stress.** Crank the parallelism. Cancel a run mid-flight.
  Let a test hang until the timeout fires. Kill the app while a hundred
  simulators are running. **Anything SimCrux leaves behind as an orphaned
  process is a serious bug** — process-tree reaping is one of the hardest parts
  of the product, especially with cocotb's `make` → Python → simulator chain.
- **Pass/fail detection.** SimCrux decides pass/fail from exit codes and log
  patterns, with composite detectors and a UVM report parser. A test that your
  team calls a pass and SimCrux calls a fail (or vice versa) is a top-priority
  report — tell us the log line that should have decided it.
- **Log volume.** Point it at a test that emits hundreds of megabytes of log.
  Does the streaming panel keep up? Does the log viewer stay searchable?
- **Trends and flaky detection.** Run the same suite repeatedly, with and without
  seed sweeps. Do the trend charts match what actually happened? Does the flaky
  classifier agree with your intuition about which tests are unreliable?
- **CI and export.** Run headless, export JUnit XML into your CI's test reporter,
  export the dashboard bundle and host it. Anything your CI can't consume is a
  bug.
- **FuseSoC import.** If you keep `.core` files, import one and tell us what the
  generated `simcrux.yaml` got wrong.
- **Debug in WaveCrux.** Run SimCrux and WaveCrux side by side, fail a test with
  waveform capture enabled, and send it across. Report anything that dispatches
  but doesn't land.
- **Cross-platform + window behaviour.** Resize aggressively, go full-screen, try
  a narrow window, switch light/dark themes and the colour presets.

## How to report

### Bugs and crashes — from inside the app (best)

Use **Help → Submit Issue** (also in the command palette and the About box). It
assembles a report with your app version, platform, OS, locale, and an optional
diagnostics snapshot and screenshot, then opens a pre-filled new-issue form in
this repo. This is the highest-signal way to report, because the reproduction
context is captured automatically.

**Privacy:** the report never includes test names, simulator output, config
contents, or file paths — only counts, formats, and environment metadata. Each
toggle in the dialog shows exactly what it adds, and you see the full body before
it's sent.

Filing by hand works too: [bug report form](../../issues/new?template=bug_report.yml).

### Feature requests and ideas

Post them in [Discussions → Ideas](../../discussions/categories/ideas), where
other beta users can discuss and upvote them and we turn accepted ones into
tracked issues. Tell us the regression workflow you're trying to complete, not
just the widget you want — it helps us find the best solution.

### Questions, help, and discussion

[GitHub Discussions](../../discussions) is the single community hub for the
beta — [Q&A](../../discussions/categories/q-a) for help,
[Ideas](../../discussions/categories/ideas) for feature requests,
[Show and tell](../../discussions/categories/show-and-tell) for what you've
built. (We're keeping everything here rather than running a Discord or Slack, so
answers stay searchable and in one place.) Keep crashes and defects in Issues so
they hit the triage queue.

## How feedback is handled

- Issues are triaged and labelled (`bug`, `beta-feedback`, platform). The in-app
  reporter applies these automatically.
- Reproducible reports — *especially ones with an attached project* — are
  prioritized, because we can turn them into a regression test.
- Fixture submissions that pass the license check are folded into the SimCrux
  test suite, so the bug you found stays fixed.

## Contributor recognition

The beta runs on community help, and we don't take it for granted. Meaningful
contributions during the beta — solid reproducible bug reports, project
donations that expose real orchestration or pass/fail edge cases, translations,
and community help — are recognized when SimCrux launches. Details of the
contributor program are announced on the SimCrux website and in Discussions.

## After the beta

When SimCrux opens its source, the canonical repo becomes
[`Ferrite-Engineering/simcrux`](https://github.com/Ferrite-Engineering/simcrux)
and the in-app reporter retargets it automatically. This beta repo is archived
at that point. Until then, everything happens here.

Thank you for helping shape SimCrux.

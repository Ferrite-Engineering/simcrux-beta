"""Cocotb fixture testbench paired with dff.v.

Runs two trivial @cocotb.test()s:
* ``test_passes`` clocks the DFF once and checks ``q == d``.
* ``test_fails`` (intentionally skipped under ``COCOTB_SKIP_FAIL=1``) is the
  fail-path test contributors can flip on locally to verify the SimCrux
  fail-classification path against a real Cocotb run.

Imports are wrapped so a static-analysis pass without ``cocotb`` installed
doesn't error; the file is only ever consumed via ``make SIM=icarus`` after
cocotb-config is on PATH.
"""

# pylint: disable=import-error
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_passes(dut):
    """Pass-path: clocks the DFF and checks q follows d."""
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.q.value == 1, f"Expected q=1, got q={int(dut.q.value)}"


if os.environ.get("COCOTB_SKIP_FAIL") != "1":

    @cocotb.test()
    async def test_fails(dut):
        """Fail-path: deliberately asserts the wrong value so SimCrux sees a
        FAIL row in the Cocotb summary table.

        Contributors verifying the fail-classification path locally set
        ``COCOTB_SKIP_FAIL=0`` (the default). Setting it to ``1`` removes the
        test from the registration so the fixture can also be run as a pure
        pass-path smoke test.
        """
        cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
        dut.d.value = 1
        await RisingEdge(dut.clk)
        assert dut.q.value == 0, "Intentional fail for fixture testing."

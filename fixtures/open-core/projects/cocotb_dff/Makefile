# Minimal Cocotb-style Makefile for the SimCrux fixture.
#
# SimCrux's CocotbDriver invokes:
#   make SIM=<sim> TOPLEVEL=dff [TOPLEVEL_LANG=verilog] [MODULE=test_dff]
# from inside the per-test working directory the scheduler allocates.
#
# To run this fixture by hand:
#   cd test/fixtures/projects/cocotb_dff
#   make SIM=icarus
SIM            ?= icarus
TOPLEVEL_LANG  ?= verilog
TOPLEVEL       ?= dff
MODULE         ?= test_dff
VERILOG_SOURCES = $(shell pwd)/dff.v

# Skip the deliberately-failing test by default so a contributor running
# this fixture by hand sees a green run; flip to 0 to verify SimCrux's
# fail classification.
COCOTB_SKIP_FAIL ?= 1
export COCOTB_SKIP_FAIL

include $(shell cocotb-config --makefiles)/Makefile.sim

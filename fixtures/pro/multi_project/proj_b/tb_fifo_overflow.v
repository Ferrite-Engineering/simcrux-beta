// Multi-project verification fixture (project B). Deliberately prints
// a failure line (never the pass string), so project B always carries
// one red row — making per-project dashboard/baseline/trend state
// visibly distinct from all-green project A.
module tb_fifo_overflow;
  initial begin
    $display("TEST FAILED: fifo overflow at depth 16");
    $finish;
  end
endmodule

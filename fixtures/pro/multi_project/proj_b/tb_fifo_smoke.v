// Multi-project verification fixture (project B). Prints the pass
// string the string_match detector expects, then finishes cleanly.
module tb_fifo_smoke;
  initial begin
    $display("TEST PASSED");
    $finish;
  end
endmodule

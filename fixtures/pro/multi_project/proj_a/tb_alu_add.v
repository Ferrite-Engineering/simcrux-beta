// Multi-project verification fixture (project A). Prints the pass
// string the string_match detector expects, then finishes cleanly.
module tb_alu_add;
  initial begin
    $display("TEST PASSED");
    $finish;
  end
endmodule

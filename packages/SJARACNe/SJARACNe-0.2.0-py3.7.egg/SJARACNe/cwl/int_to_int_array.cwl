#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: ExpressionTool

requirements:
 - class: InlineJavascriptRequirement

inputs:
  number:
    type: int
    label: a positive integer

outputs:
  int_array:
    type: int[]

expression: |
  ${ var i_arr = [];
     for (var i = 1; i < inputs.number+1; i++) {
       i_arr.push(i);
     }
     return { "int_array": i_arr };
   }

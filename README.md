# V2SV

V2SV is a basic Verilog to SystemVerilog converter. While all Verilog code is valid SystemVerilog code as well, this tool aims to modify Verilog code to take advantage of new SystemVerilog constructs.

## Features

This tool takes advantage of these SystemVerilog constructs, which offer improvements over their Verilog counterparts:
* The `logic` datatype (as opposed to `wire` and `reg`)
* `always_comb` and `always_ff` blocks (as opposed to `always`)
* Enumerations (as opposed to `localparam`)

## Usage

Clone this repo:
```
git clone https://github.com/jamesjiang52/V2SV.git
cd V2SV
```

Run:
```
python v2sv.py filename
```

where `filename` is the path to a valid Verilog file (.v). This generates a SystemVerilog file (.sv) of the same name, in the same location.

## Known issues

* Comments within a module will cause undocumented behavior

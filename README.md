# Turing Machine Simulator

## Machines
Start with the lexicon and syntax the machine will use to follow the rules and interact with the tape.

- Blank character
- Returned characters
- Initial state
- Final state
- Rules syntax
- Rules

One rule per line.

## Tapes
One tape per line.

## Debugging
Use the option `-d` to display process information.

`./tmsim.py -d machine_name tape_name`

## Examples
Turing Machine examples are located in `machines/examples` and their according tapes in `tapes/examples`.
To run an example, use the following command line replacing `X` with the name of the turing machine and `Y` with the tape to use.

`./tmsim.py examples/X examples/Y`

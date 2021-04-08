# Turing Machine Simulator

## Machines
A machine will use a lexicon and a syntax to follow the rules and interact with the tape.

Turing Machine file content:

- Blank character
- Returned characters
- Initial state
- Final state
- Rule syntax
- Rules

One rule per line.

### Rule syntax
The rule syntax lets the machine know how to read the rules. It must include the current state (Q) and the read (r) 
lexicons for being unique sets to find the correct rule to follow.

Application of a rule by the machine is independent to the syntax.

| Label         | Lexicon | Description                                                 |
| ------------- | ------- | ----------------------------------------------------------- |
| Current state | Q       | State to be in to follow the rule                           |
| Next state    | N       | State of the machine at the end of the executed rule        |
| Move          | m       | Direction in which to move pointer at the end of the rule   |
| Read          | r       | Character to be read at pointer location to follow the rule |
| Write         | w       | Character to write at pointer location                      |

### Rule construction
| Action       | Lexicon | Description                              |
| ------------ | ------- | ---------------------------------------- |
| Move         | L       | Move pointer on cell to the left         |
|              | R       | Move pointer on cell to the right        |
|              | -       | Don't move pointer                       |
| Read         | *       | All characters (wildcard)                |
|              | ~       | All characters but blank                 |
| Write        | *       | Write read character (i.e., don't write) |
|              | ~       | Write read character (i.e., don't write) |

| Action | ST-SP | MT-SP       |
| ------ | ----- | ----------- |
| Move   | m     | (m, ..., m) |
| Read   | r     | (r, ..., r) |
| Write  | w     | (w, ..., w) |
*ST: Single tape - MT: Multiple tapes - SP: Single pointer*

### Rule examples
All below examples use the syntax `Q r w m N` and `B` as the blank character.

#### ST-SP

`q0 B | R q1`

In state `q0`, if `B` is read at pointer location, then write `|` at same location and move pointer one cell to the 
right. Next state will be `q1`.

#### MT-SP (3 tapes)

`q0 (B, ~, *) (|, B, *) (R, -, L) q1`

*Px: pointer of tape x*

In state `q0`, if P1 reads `B`, P2 reads a character other than `B` and P3 reads any character, then write `|` at P1, 
write `B` at P2 and write read character at P3 (i.e., don't write). Once done, move P1 one cell to the right, don't 
move P2 and move P3 one cell to the left. Next state will be `q1`.

## Tapes
One tape per line.

## Debugging
Use the option `-d` to display process information.

`./tmsim.py -d machine_name tape_name`

## Examples
Turing Machine examples are located in `machines/examples` and their according tapes in `tapes/examples`.
To run an example, use the following command line replacing `X` with the name of the turing machine and `Y` with the 
tape to use.

`./tmsim.py machines/examples/X tapes/examples/Y`

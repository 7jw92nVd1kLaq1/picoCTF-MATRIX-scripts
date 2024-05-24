# picoCTF-MATRIX-scripts

There are four scripts used to solve the challenge.

* matrix.py
  * This script directly simulates the binary involved in the challenge.
  * If an answer is correct, then it outputs the congratulatory message for providing a right input.
* matrix_stop.py
  * The debugging version of `matrix.py`. It stops after each execution of a command.
* matrix_commands_json.py
  * The script used to generate the JSON file containing all the commands. The very JSON file is used in `matrix.py`
* matrix_map.py
  * The script used to generate the JSON file that outputs the 16 * 16 maze. The key to solving the challenge.


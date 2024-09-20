#!/bin/bash
source ~/cron_vars

~/anaconda3/envs/qiskitv1/bin/python ~/risc_dev/RISC2024-SEQCURE/SEQCURE-Dashboard/pulling_results/risc2024/$1.py --target="$2" --qubits="$3" --shots=500 "$4" "$5"

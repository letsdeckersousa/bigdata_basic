#!/bin/sh
SEQ="seqFile.txt"
SEQFILE="$SEQ$1" 
echo $SEQFILE
python2.7 HMM_parametric_2.py probabilityEmission.txt probabilityTransmission.txt $SEQFILE
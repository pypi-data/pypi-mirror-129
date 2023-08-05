# tf-seq2seq-losses
Tensorflow implementations for
[Connectionist Temporal Classification](file:///home/alexey/Downloads/Connectionist_temporal_classification_Labelling_un.pdf)
(CTC) loss in TensorFlow.

## Installation
Tested with Python 3.7. 
```bash
$ pip install tf-seq2seq-losses
```

## Why
### 1. Faster
official CTC loss implementation 
[`tf.nn.ctc_loss`](https://www.tensorflow.org/api_docs/python/tf/nn/ctc_loss)
is dramatically slow. 
The proposed implementation is approximately 15 times faster as it follows form the benchmark:

| Name                       | forward time          | gradient calculation time                 
|:---:                       |:---:                  |:---:             
| tf.nn.ctc_loss             | 13.2 ± 0.02           | 10.4 ± 3.
| classic_ctc_loss           | 0.138 ± 0.006         | 0.28 ± 0.01
| simple_ctc_loss            | 0.0531 ± 0.003        | 0.119 ± 0.004

(Tested on single GPU: GeForce GTX 970,  Driver Version: 460.91.03, CUDA Version: 11.2). See 
[`benchmark.py`](tests/performance_test.py)
for the experimental setup. To run this benchmark use
```bash
$ pytest -o log_cli=true --log-level=INFO tests/benchmark.py
```
from the project root directory.
Here `classic_ctc_loss` is the standard version of CTC loss
that corresponds to the decoding with repeated tokens collapse like 
> a_bb_ccc_c   ->   abcc

(equivalent to `tensorflow.nn.ctc_loss`).
The loss function `simple_ctc_loss` is a simplified version corresponding to straight decoding rule like

> a_bb_ccc_c   ->   abbcccc

(simple blank removing).

### 2. Numerically stable 
1. Proposed implementation is more numerically stable, for example it calculates resonable output for
`logits` of order `1e+10` and even for `-tf.inf`.
2. If logit length is too short to predict label output the probability of expected prediction is zero.
Thus, the loss output is `-tf.inf` for this sample but not `702.` like for`tf.nn.ctc_loss`.


### 3. No C++ compilation
This is a pure Python/TensorFlow implementation. We do not have to build or compile any C++/CUDA stuff.


## Usage
The interface is identical to `tensorflow.nn.ctc_loss` with `logits_time_major=False`.
```python
import tensorflow as tf
from tf_seq2seq_losses import classic_ctc_loss

batch_size = 1
num_token = 3 # = 2 tokens + blank
logit_length = 5
loss = classic_ctc_loss(
    labels = tf.constant([[1,2,2,1]], dtype=tf.int32),
    logits = tf.zeros(shape=[batch_size, logit_length, num_token], dtype=tf.float32),
    label_length = tf.constant([4], dtype=tf.int32),
    logit_length = tf.constant([logit_length], dtype=tf.int32),
    blank_index = 0,
)
```

## Under the roof
TensorFlow operations sich as `tf.while_loop` and `tf.TensorArray`. 
The bottleneck is the iterations over the logit length in order to calculate
α and β
(see, for example, the original 
[paper](file:///home/alexey/Downloads/Connectionist_temporal_classification_Labelling_un.pdf)
). Expected gradient GPU calculation time is linear over logit length. 

## Known Probelems:
1. Warning:
> AutoGraph could not transform <function classic_ctc_loss at ...> and will run it as-is.
Please report this to the TensorFlow team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output.

observed for tensorflow version 2.4.1
has no effect for performance. It is caused by `Union` in type annotations. 

## Future plans
1. Add decoding (inference)
2. Add rnn-t loss.
3. Add m-wer loss.





grad:

remove union
+------------------------+----------------------------+-------+
|                        |   mean processing time (s) |   std |
+========================+============================+=======+
| tensorflow.nn.ctc_loss |                      9.42  | 0.1   |
+------------------------+----------------------------+-------+
| classic_ctc_loss       |                      0.271 | 0.005 |
+------------------------+----------------------------+-------+
| simple_ctc_loss        |                      0.121 | 0.006 |
+------------------------+----------------------------+-------+


+------------------------+----------------------------+-------+
|                        |   mean processing time (s) |   std |
+========================+============================+=======+
| tensorflow.nn.ctc_loss |                     23.3   | 5     |
+------------------------+----------------------------+-------+
| classic_ctc_loss       |                      0.27  | 0.003 |
+------------------------+----------------------------+-------+
| simple_ctc_loss        |                      0.117 | 0.004 |
+------------------------+----------------------------+-------+


tensorflow.nn.ctc_loss  18.582688  0.241295
classic_ctc_loss         0.548777  0.004851
simple_ctc_loss          0.308365  0.005894


tensorflow.nn.ctc_loss  8.712257  0.142457
classic_ctc_loss        0.554044  0.012687
simple_ctc_loss         0.294473  0.002924



tensorflow.nn.ctc_loss  9.619491  0.023562
classic_ctc_loss        0.341878  0.006051
simple_ctc_loss         0.290321  0.004223



forward:

remove union
+------------------------+----------------------------+-------+
|                        |   mean processing time (s) |   std |
+========================+============================+=======+
| tensorflow.nn.ctc_loss |                     15.1   | 3     |
+------------------------+----------------------------+-------+
| classic_ctc_loss       |                      0.135 | 0.001 |
+------------------------+----------------------------+-------+
| simple_ctc_loss        |                      0.053 | 0.003 |
+------------------------+----------------------------+-------+


+------------------------+----------------------------+--------+
|                        |   mean processing time (s) |    std |
+========================+============================+========+
| tensorflow.nn.ctc_loss |                    12.3    | 1      |
+------------------------+----------------------------+--------+
| classic_ctc_loss       |                     0.134  | 0.0009 |
+------------------------+----------------------------+--------+
| simple_ctc_loss        |                     0.0547 | 0.003  |
+------------------------+----------------------------+--------+

tensorflow.nn.ctc_loss  8.421478  0.039425
classic_ctc_loss        0.086655  0.003825
simple_ctc_loss         0.059665  0.002828



tensorflow.nn.ctc_loss  24.156974  5.085383
classic_ctc_loss         0.089546  0.002290
simple_ctc_loss          0.062101  0.003325

classic_ctc_loss         0.089270  0.002333
simple_ctc_loss          0.060012  0.001957
tensorflow.nn.ctc_loss  18.544750  3.352792
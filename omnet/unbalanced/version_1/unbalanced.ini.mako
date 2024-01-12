[General]
ned-path = .;../queueinglib
network = unbalanced
#cpu-time-limit = 60s
cmdenv-config-name = unbalanced
#tkenv-default-config = unbalanced
qtenv-default-config = unbalanced
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config unbalancedBase]
description = "Global scenario"
**.srv_high.queueLength.result-recording-modes = +histogram
**.srv_low.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:
[Config unbalanced_delta${delta}]
extends = unbalancedBase
**.delta = ${delta}
%endfor
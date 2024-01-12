[General]
ned-path = .;../queueinglib
network = unbalanced_2
#cpu-time-limit = 60s
cmdenv-config-name = unbalanced_2
#tkenv-default-config = unbalanced_2
qtenv-default-config = unbalanced_2
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config unbalancedBase2]
description = "Global scenario"
**.srv_high.queueLength.result-recording-modes = +histogram
**.srv_low.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:
[Config unbalanced2_delta${delta}]
extends = unbalancedBase2
**.delta = ${delta}
%endfor
[General]
ned-path = .;../queueinglib
network = advanced_1
#cpu-time-limit = 60s
cmdenv-config-name = advanced_1
#tkenv-default-config = advanced_1
qtenv-default-config = advanced_1
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config advanced1]
description = "Global scenario"
**.srv_high.queueLength.result-recording-modes = +histogram
**.srv_low.queueLength.result-recording-modes = +histogram
**.sink_high.lifeTime.result-recording-modes = +histogram
**.sink_low.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:
[Config advanced1_delta${delta}]
extends = advanced1
**.delta = ${delta}
%endfor
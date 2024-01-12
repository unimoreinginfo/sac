[General]
ned-path = .;../queueinglib
network = advanced_2
#cpu-time-limit = 60s
cmdenv-config-name = advanced_2
#tkenv-default-config = advanced_2
qtenv-default-config = advanced_2
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config advanced2]
description = "Global scenario"
**.srv_high.queueLength.result-recording-modes = +histogram
**.srv_low.queueLength.result-recording-modes = +histogram
**.sink_high.lifeTime.result-recording-modes = +histogram
**.sink_low.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:
[Config advanced2_delta${delta}]
extends = advanced2
**.delta = ${delta}
%endfor
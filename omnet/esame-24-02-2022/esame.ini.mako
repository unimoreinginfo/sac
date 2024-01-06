[General]
ned-path = .;../queueinglib
network = esame
#cpu-time-limit = 60s
cmdenv-config-name = esame_base
# tkenv-default-config = mm1_base
qtenv-default-config = esame_base
repeat = 3
sim-time-limit = 300s
# debug-on-errors = true
**.vector-recording = false

[Config esame_base]
description = "global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
%for rho in [0.7, 0.9]:
        %for cv in [0.5, 1.0, 1.5]:
[Config esame_rho${"%03d" % int (rho * 100)}_cv${"%03d" % int (cv * 100)}]
extends = esame_base
**.cv = ${cv} 
**.rho = ${rho}
%endfor
%endfor


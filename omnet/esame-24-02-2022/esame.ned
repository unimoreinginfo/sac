import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network esame {
        parameters:
                double mu = default(100); // 1/mu = 10ms => mu = 100 r/s 
                double rho = default(0.7); // input da config
                double lambda = rho * mu;
                double cv = default(0.5); // input da config
                src.interArrivalTime = 1.0s * exponential(1/lambda);
                srv.serviceTime = 1.0s * lognormal(log(1.0(mu * sqrt(1 + cv^2))), sqrt(log(1 + cv^2)));
        submodules:
                src: Source;
                srv: Queue;
                sink: Sink;
        connections:
                src.out-->srv.in++;
                srv.out-->sink.in++;
}


import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network unbalanced
{
	parameters:
		double lambda = 6;
		double delta = default(0);
		double lambda_low = lambda - delta;
		double lambda_high = lambda + delta;
		double mu = 10;		

		src_high.interArrivalTime = exponential(1s/lambda_high);
		src_low.interArrivalTime = exponential(1s/lambda_low);

		srv_high.serviceTime = 1s * exponential(1/mu);	
		srv_low.serviceTime = 1s * exponential(1/mu);

	submodules:
		src_high: Source;
		src_low: Source;
		srv_high: Queue;
		srv_low: Queue;
		sink: Sink;
	connections:
		src_high.out --> srv_high.in++;
		src_low.out --> srv_low.in++;
		srv_high.out --> sink.in++;
		srv_low.out --> sink.in++;
}


import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network unbalanced_2
{
	parameters:
		double lambda = 6;
		double delta = default(0);
		double mu = 10;		
		double mu_low = mu - delta;
		double mu_high = mu + delta;

		src_high.interArrivalTime = exponential(1s/lambda);
		src_low.interArrivalTime = exponential(1s/lambda);

		srv_high.serviceTime = 1s * exponential(1/mu_high);	
		srv_low.serviceTime = 1s * exponential(1/mu_low);

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


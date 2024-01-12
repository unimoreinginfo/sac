import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Classifier;

network advanced_2
{
	parameters:
		double lambda = 6;
		double delta = default(0);
		
		double mu = 10;		
		double mu_low = mu - delta;
		double mu_high = mu + delta;

		src_high.interArrivalTime = exponential(1s/lambda);
		src_low.interArrivalTime = exponential(1s/lambda);

		src_high.jobType = 1;
		src_low.jobType = 0;
		classifier.dispatcherField = 1;

		srv_high.serviceTime = 1s * exponential(1/mu_high);	
		srv_low.serviceTime = 1s * exponential(1/mu_low);

	submodules:
		src_high: Source;
		src_low: Source;
		srv_high: Queue;
		srv_low: Queue;
		sink_high: Sink;
		sink_low: Sink;
		classifier: Classifier;
	connections:
		src_high.out --> srv_high.in++;
		src_low.out --> srv_low.in++;
		srv_high.out --> classifier.in++;
		srv_low.out --> classifier.in++;
		classifier.out++ --> sink_high.in++;
		classifier.rest --> sink_low.in++;
}


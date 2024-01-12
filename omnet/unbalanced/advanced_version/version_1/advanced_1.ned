import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Classifier;

network advanced_1
{
	parameters:
		double lambda = 6;
		double delta = default(0);
		double lambda_low = lambda - delta;
		double lambda_high = lambda + delta;
		double mu = 10;		

		src_high.interArrivalTime = exponential(1s/lambda_high);
		src_low.interArrivalTime = exponential(1s/lambda_low);

		src_high.jobType = 1;
		src_low.jobType = 0;
		classifier.dispatcherField = 1;

		srv_high.serviceTime = 1s * exponential(1/mu);	
		srv_low.serviceTime = 1s * exponential(1/mu);

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


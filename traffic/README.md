There are two factors to consider when optimizing the algorithm. The first is accuracy and the second is time. 

For each of the following adjustments there was an impact on accuracy and time. I went through and while keeping all else equal, I adjusted these factors to see their effects.

Pool size: I found that not pooling led to a severe inefficiency in accuracy and time and that anything above 3x3 discounted time but at a severe cost for accuracy. So I decided to set my pooling parameter at 3x3

Batch-size of hidden layer: I found that typically the larger the batch-size the more accuracy, but once passing the 1000 mark started costing the algorithm a lot of time. So I decided to leave my first hidden layer batch-size at 1024.

Dropout: This factor mostly had a consequence of accuracy. There is a certain percentage that works well and above and bellow that level you experience inaccuracy. I found that level to be .3

Another hidden layer: This only marginally improved accuracy at some expense of time, but I also found that batch-size of this layer also impacted accuracy. I found that a smaller batch-size and second hidden layer allowed for improved accuracy at a relatively normal increase in time.

Time and accuracy aren't linearly related. typically I found that low accuracy improves much faster than high accuracy, and once you pass around 90% accuracy, to increase accuracy further is a much bigger time toll. However, at that level of accuracy I found some combinations of the aforementioned factors leads to large increases in time with a decrease in accuracy. I believe this may th be the result of over-fitting.

At the levels that I set in the algorithm, I believe I am slightly on the inefficient side of timing, but have a relatively high level of accuracy.

# NervtechDevelopmentTask
Git reposytory for Nervtech entry task 
 
##  What the code does?
The code in Nervtech_task.py file reads data from predetermined .csv files in predetermined locations.
When needed data is extracted from dataFrame, function for caluclating acceleration and jerk is called.
Function calculates resultant velocity that is product of comoponents in dataframe, than calculate acceleration as temporal gradient of resultatnt velocity.
Gradient is fuction in numpy library. Acceleration is filtrated by moving average filter to smoothen profile and thus make numeric calulation of jerk credible [1].
Jerk is calculated as temporal gradient of acceleration. 

For class definiton ther are two criteria. First classification is done using adaptation of algorithm in given in reference [2]. 
Adaptation is changing number of classes given by algorithm and concluding overall style of driver rather than classfying just driving style in certain moments of time.
Other classification is relative, drivers are just sorted by percentage of time of driving during which they caused jerk beyond safty limit given in reference [3].
Code prints results in a simple tables.

Next iteration of code development could be passing data file names as argument in command line. Ajusting the algorithm to be more accurate and reliable.
Then it could be base for neural network for Driving style classification. Relative classification can be improved by more complex scoring system.


## How to run a program?
Simple command can be executed in terminal:
python <path>/Nervtech_task.py

 
## What the final results represent?
Result in the first table represents degree of agresivness of the given driver. 
Result in the second table represents relative positioning of a driver among other driver by how frequent the driver cause unsafe jerk.
 
 
## The limit of a “safe” jerk
In reference [3] maximum of safe jerk is set at 0.9 m/s^3. 
 
## References
 
  [1] MARTIN, Delton; LITWHILER, Dale. An investigation of acceleration and jerk profiles of public transportation vehicles. 
     In: 2008 Annual Conference & Exposition. 2008. p. 13.194. 1-13.194. 13.
 
  [2] MURPHEY, Yi Lu; MILTON, Robert; KILIARIS, Leonidas. Driver's style classification using jerk analysis. 
      In: 2009 IEEE Workshop on Computational Intelligence in Vehicles and        Vehicular Systems. IEEE, 2009. p. 23-28.
 
  [3] BAE, Il; MOON, Jaeyoung; SEO, Jeongseok. Toward a comfortable driving experience for a self-driving shuttle bus. Electronics, 2019, 8.9: 943.



 





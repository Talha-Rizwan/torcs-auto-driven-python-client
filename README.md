# torcs-auto-driven-python-client

We generated the data for training our model. In this phase we needed to control our
car with the help of keyboard keys.
•
We used the library of keyboard in order to accomplish the task. By this the key pressed by
the user was detected.
•
When the user pressed the up key, we basically increased the acceleration of the car and the
brake was assigned the value of none
•
Similarly, when the down key was pressed. We deaccelerated our car and brake was also
applied.
•
When the user pressed right arrow steer was adjusted keeping in mind the acceleration. So
that our car turned appropriately.
• Similarly when the left key was pressed steer was also adjusted.
• Gears were incremented and decremented depending upon the rpm that the car has at that
specific moment.
•
We then pushed the data including acceleration,brake,opponents and other in csv file. For
this I initialized two lists. In list one I basically stored the attribute at every instance. And
that list1 was then appended to list2. After appending list1 was cleared.
• At at the end we pushed the list2 in our csv file.
• We also pushed the arrow key pressed by the user at that instance along with the data. By
doing this we got the data that was needed to train our model.
Description of Phase 2:
In phase two our task was to automate the car. We were supposed to train our model using the data
that we got from phase 1. In this case, we used DECISION TREE in order to train our data.
•
First of all, we have imported the data from csv file that we created in phase 1. We kept the
data in data frame.
•
After that we have applied the feature selection. In feature selection we selected the
attributes that were having an impact on the results (accuracy). The results that were having
no impact (in order to lower the overhead) were removed.
•
The data we got from phase 1 was imbalanced as the up key was pressed frequently. We
performed the technique of SMOTE for oversampling.
•
We used the techniques of both GINI index and entropy. But we have used GINI index in
order to select the node.•
The data was then split in training and testing data. We used 70% of data as our training data
and 30% of data for testing. We split the data in order to measure the accuracy that we got
from decision tree. The accuracy was 98%.
•
After that we integrated the decision tree with our game. We made the decision tree as
separate class. We have build the decision tree just once at the start of our game. And after
that we are giving the data to your model and getting prediction.
• The arrow keys (up,down,right,left) are used as class label.
• In our game, the data of csv file was used as training data and the data received while
playing the game was used as test data. Depending upon the attributes our model predicted
the arrow key and we performed the action.

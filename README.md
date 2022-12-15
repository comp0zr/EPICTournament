Concept:

Having been a remote worker myself since April 2020, I’m personally well-acquainted with the many pros and cons of working from home full time. For me personally, one of the greatest advantages to remote work has been the fact that I have the ability to do my work at any time of day or night, and continue working as long as I’d like without interruption. However, I, like many others, will often suffer physical consequences when I overdo it, particularly since I have the tendency to slouch. After a very busy week, I’ve often experienced extreme neck and shoulder pain from my poor posture-related habits.
The idea occurred to me that you could deduce fairly easily whether or not an individual was slouching or sitting too close to their monitor if you had a frame of reference for where their head “should” be positioned under ideal circumstances. So the idea I attempted to implement was an application that would record statistics about one’s posture-related habits while at work, with the goal of helping them develop better ergonomic practices.

______________________________________________________

Implementation:

I intended to accomplish my goal as follows:
Have the user go through a setup process that would involve them sitting with ideal posture in front of a webcam. Using facial recognition, the application would take a series of snapshots of the position and size of their head, which would be used as the basis for determining when and how often they were sitting “improperly”.

⦁	Through their work day, the application would run in the background and compare their current position to the basis. Since time was limited, I intended to keep the logic behind this comparison very simple:

⦁	If the top of their head sunk below the basis beyond a certain threshold, the program would determine that they are slouching.

⦁	If the “size” of their head increased beyond a certain threshold, the program would determine that they had moved too close to the monitor.

⦁	Whenever this would happen, a timer would be triggered, and a “violation” would be recorded only if the length of time they remained in this position exceeded a certain number of seconds that could be set by the user.

This information would be viewable later, or the application could send a push notification to warn the user about it.

______________________________________________________

Challenges:

Honestly, the concept itself was straightforward, and would have been quite easy to implement if I had been using APIs that I was familiar with. Unfortunately, I have never attempted to create an actual application using python, and I spend an inordinate amount of time figuring out how to get the APIs to do the simplest things. My biggest holdups were related to dealing with the UI, which is unfortunate, because the fun part for me is derived from the logical/mathetmatical/algorithmic aspects of programming. 
The other major issue I encountered was that the facial recognition was picking up all sorts of “noise” around me and determining there were many other faces present around my office. I attempted to filter these out using basic concepts in probability/statistics, and implementing a very simple low-variance filter to get rid of stationary objects that were erroneously being interpreted as faces. Unfortunately, by the time I was able to start delving into this, I had already wasted so much time trying to figure out how to handle the UI, that it was basically a lost cause.
______________________________________________________

Conclusion:

Despite the fact that I did not accomplish my goal, this was very educational on numerous levels, and I’m strongly considering fleshing out this idea further and attempting to turn it into a legitimate application. While I do wish I had something to present, I hope that this write up will provide you, distinguished ladies and gentlemen of the panel, with a decent idea of my thought processes and general approach.

Thanks a lot, it’s been fun!
-John


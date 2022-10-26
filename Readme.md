# Image Morphing

> 聯絡資訊：mailto: p78101027@gs.ncku.edu.tw



## Description

In this homework, we are asked to implement the algorithm from [1]. The feature-based image metamorphosis needs pre-defined feature lines for image morphing. The approach gives the animator high-level control of the visual effect by providing natural feature-based specification and interaction. 



## Algorithm

For the transformation with one pair of lines, the algorithm can be simple as following:

```pseudocode
For each pixel X in the destination image
	find the corresponding u, v
	find the Xs in the source image for that u, v
	destinationImage(X) = sourceImage(Xs)
```

We could further explain the procedure by Fig. 1. For these two feature lines in destination image and source image, the pixel $X'$ In source image can be calculated under below equations ( eq 1-3 ). 

|                   Fig 1. Single line pair                    |
| :----------------------------------------------------------: |
| ![SinglePairLine](/Users/popo/Desktop/phd-fall2021/openGL/Hw2/Fig/SinglePairLine.png) |

$$
u = \frac{(X-P)\cdot(Q-P)}{\norm{Q-P}^2}
$$

$$
v = \frac{(X-P) \cdot Perpendicular(Q-P)}{\norm {Q-P}}
$$

$$
X' = P' + u \cdot (Q'-P') + \frac {v \cdot Perpendicular(Q'- P')}{\norm {Q'- P'}}
$$

The algorithm can be expanded when we got more than a single pair of feature lines as following:

```pseudocode
For each pixel X in the destination
	DSUM = (0,0)
	weightsum = 0
	For each line PiQi
		calculate u, v based on (Pi Qi)
		calculate X'i based on u, v and (P'i Q'i)
		dist = shortest distance from X to (Pi Qi)
		weight = (length^p / (a+dist))^b
		DSUM += Di * weight
		weightsum += weight
	Xs = X + DSUM / weightsum
	destinationImage(X) = sourceImage(Xs)
```



## Usage

1. open the terminal under project’s root directory
2. install the requirements by `pip3 install -r requirements.txt`
3. execute `python3 main.py`

4. GUI application

   ![Slide1](/Users/popo/Desktop/phd-fall2021/openGL/Hw2/Fig/Presentation2/Slide1.png)

5. click `Draw` button for feature line(s) drawing. A new window would open after clicked. Follow the instructions to draw the line.

   ![Slide2](/Users/popo/Desktop/phd-fall2021/openGL/Hw2/Fig/Presentation2/Slide2.png)

6. You can modify the configuration parameters and then clicked `warping` button  for displaying the following results.![Slide3](/Users/popo/Desktop/phd-fall2021/openGL/Hw2/Fig/Presentation2/Slide3.png)

## Reference

[1] Beier, Thaddeus, and Shawn Neely. "Feature-based image metamorphosis." *ACM SIGGRAPH computer graphics* 26.2 (1992): 35-42.

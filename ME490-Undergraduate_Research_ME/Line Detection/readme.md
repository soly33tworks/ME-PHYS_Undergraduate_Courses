# NEMS Project (WORK-IN-PROGRESS)

**Note :** Many of these examples were question specific; however, I modified them for general use.

## Problem Definition

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>


Usage of VS code is highly recommended for convenience
Run "Manual_Processor" to start the program

Required libraries to pip install:
	-cv2
	-numpy
	-random
	-time
	-matplotlib
	-pickle
	-scipy

Current set of general methods in the order of usage:
	-Custom denoising filter
	-Tracker to adjust for horizontal shifting of the recording
	*Tracker to adjust for vertical shifting also needs to be added
	-Connection points (top and bottom):
		-Maximum pixel value search
		-Ridge Regression (Linear but with small lambda for numerical stability)
	-Beam points:
		-Maximum pixel value search
		-Find orthogonal distances of all points
		-Eliminate outliers via continuity
		-Eliminate more outliers outside of the "curves"
		-Ridge Regression with small lamdba
	-Mark the points and lines on the image, record the data
	-Plot the results (raw and with low pass filter)


## User Interface

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>

## Step 1: Maximum Pixel Search

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>

## Step 2: Continuity Condition

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>

## Step 3: Apply Regression

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>

## Helper 1: Image Denoising Filter  

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>

## Helper 2: Curve Outlier Elimination  

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME361-Numerical_Methods_4_Engineers/assets/HW1%20fig%202.png?raw=true">
</p>


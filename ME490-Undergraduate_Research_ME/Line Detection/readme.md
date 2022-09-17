# NEMS Project

**Note 1:** Run "Manual_Processor" to start the program and enter your video directory and parameters into the code.

**Note 2:** Usage of VS code is highly recommended for convenience.

**Note 3:** The code for the interface does not have the most up to date "image processor", so I didn't include the GUI codes.

## Problem Definition
The aim is to extract of positional data and observe wave behaviour from microscope recordings of buckling nanomechanical membranes. See the recordings on the university YouTube page for more details: https://www.youtube.com/watch?v=EXk4vOJH4_4 

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Setup_annotated.png">
</p>

## User Interface

<p align="center">
  <img width=75% height=75% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Tab1.jfif">
</p>

<p align="center">
  <img width=75% height=75% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Tab2.jfif">
</p>

<p align="center">
  <img width=75% height=75% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Tab3.jfif">
</p>

## Step 1: Maximum Pixel Search

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Simple.png">
</p>

## Step 2: Continuity Condition Elimination (without/with noise)

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Continuity%20FOV.jfif">
</p>

<p align="center">
  <img width=45% height=45% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Continuity.png">
  <img width=45% height=45% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Continuity_noise%20at%20center.png">
</p>

## Step 3: Apply Ridge Regression

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Regression.png">
</p>

## Helper 1: Image Denoising Filter  

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Denoising%20filter.png">
</p>

## Helper 2: Curve Outlier Elimination  

<p align="center">
  <img width=50% height=50% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Detection%20points%20(not%20eliminated).png">
</p>

## Post Processing: Butterworth Filtering

<p align="center">
  <img width=75% height=75% src="https://github.com/soly33tworks/ME-PHYS_Undergraduate_Courses/blob/main/ME490-Undergraduate_Research_ME/Line%20Detection/assets/Butterworth.png">
</p>

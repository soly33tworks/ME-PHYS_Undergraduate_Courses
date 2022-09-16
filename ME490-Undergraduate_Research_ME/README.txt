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

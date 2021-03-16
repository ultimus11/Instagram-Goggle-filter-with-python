import numpy as np
import cv2

def overlay_transparent(background, overlay, x, y):
	# https://stackoverflow.com/a/54058766/11359097
	background_width = background.shape[1]
	background_height = background.shape[0]

	if x >= background_width or y >= background_height:
		return background

	h, w = overlay.shape[0], overlay.shape[1]

	if x + w > background_width:
		w = background_width - x
		overlay = overlay[:, :w]

	if y + h > background_height:
		h = background_height - y
		overlay = overlay[:h]

	if overlay.shape[2] < 4:
		overlay = np.concatenate(
					[
						overlay,
						np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
						],
					axis = 2,
		)

	overlay_image = overlay[..., :3]
	mask = overlay[..., 3:] / 255.0

	background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

	return background

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#Read original image to apply filter and convert it to grayscale
img = cv2.imread("gr5.png",cv2.IMREAD_UNCHANGED)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
widthh=0
#First do face detection and then detect eyes within face
#Record co-ordinates for eyes for width and height calculations to resize filter image i.e. goggle image
for (x,y,w,h) in faces:
	#img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = img[y:y+h, x:x+w]
	eyes = eye_cascade.detectMultiScale(roi_gray)
	for (ex,ey,ew,eh) in eyes:
		#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		if widthh==0:
			widthh=ex
		print(ex,ey,ew,eh)
widthh1=(ex+ew)-widthh
#Show original image
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#Read filter image and resize it
fram2=cv2.imread("fram3.png",cv2.IMREAD_UNCHANGED)
stretch_near = cv2.resize(fram2, (widthh1+80, eh-5))
print(ex,ey)

#Apply overlay
filter1 = overlay_transparent(img.copy(), stretch_near, widthh+x-35 ,ey+y+20)
#Show output image
cv2.imshow('img1',filter1)
cv2.waitKey(0)
cv2.destroyAllWindows()

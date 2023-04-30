import cv2
import numpy as np
from shapely.geometry import Polygon

# Read in the image
# img = cv2.imread('baseball_2.jpeg')
img = cv2.imread('sketch_pens.jpeg')



# img = cv2.medianBlur(img,5)
img = cv2.GaussianBlur(img,(5,5),0)
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold to create binary image
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]


# img = cv2.medianBlur(gray,5)
# ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

# th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#             cv2.THRESH_BINARY,11,2)




# cv2.imshow('image', thresh)
# cv2.waitKey(0)
cv2.imshow('image', th1)
cv2.imwrite('threshold.jpeg', th1)
cv2.waitKey(0)
# cv2.imshow('image', th2)
# cv2.waitKey(0)




# Find contours
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)




# # Find intersection points
# intersection_points = []
# for i, poly1 in enumerate(polygons):
#     for j, poly2 in enumerate(polygons[i+1:]):
#         inter = poly1.intersection(poly2)
#         if inter.geom_type == 'Point':
#             intersection_points.append(np.array(inter.coords[0], dtype=int))
# print(len(intersection_points))



#Draw contours greater than a min area
# set minimum area threshold
min_area = 1
contours_new = []
# loop over contours
for c in contours:
    # calculate area of contour
    area = cv2.contourArea(c)
    
    # only consider contours above minimum area
    if area > min_area:
        # draw contour on image
        cv2.drawContours(img, [c], 0, (0, 255, 0), 2)
        contours_new.append(c)
        
# print(contours)
# Create polygons from contours
polygons = []
for c in contours_new:
    if len(c) >= 4:  # Check if contour has at least 4 coordinates
        poly = Polygon(c.reshape(-1, 2))
        polygons.append(poly)

# Draw all contours on the image
# cv2.drawContours(img, contours, -1, (0, 255, 0), 2)


# # Draw circles at intersection points
# for p in intersection_points:
#     cv2.circle(img, tuple(p), 10, (0, 0, 255), -1)
#     # print(f"Color at ({p[0]}, {p[1]}): {color}")


################################################
# # Find intersection points and corresponding colors
# intersection_points = []
# touching_points = []
# colors = []
# for i, poly1 in enumerate(polygons):
#     for j, poly2 in enumerate(polygons[i+1:]):
#         inter = poly1.intersection(poly2)
#         if inter.geom_type == 'Point':
#             p = np.array(inter.coords[0], dtype=int)
#             intersection_points.append(p)
#             color = img[p[1], p[0]]
#             colors.append(color)
#         elif inter.geom_type == 'MultiPoint':
#             for p in inter:
#                 p = np.array(p.coords[0], dtype=int)
#                 touching_points.append(p)
#                 color = img[p[1], p[0]]
#                 colors.append(color)
# print(len(intersection_points))
# print(len(touching_points))

########################################################


# Define threshold for considering contours as touching
touching_threshold = 3

# Find intersection and touching points and corresponding colors
intersection_points = []
touching_points = []
colors = []

# Find nearby contours
nearby_contours = []
for i, poly1 in enumerate(polygons):
    for j, poly2 in enumerate(polygons[i+1:]):
        dist = poly1.distance(poly2)
        if dist < touching_threshold:
            nearby_contours.append((i, i+j+1))

for i, poly in enumerate(polygons):
    if i in [c[0] for c in nearby_contours]:
        touching_points += list(poly.exterior.coords[:-1])
        colors += [img[int(p[1]), int(p[0])] for p in poly.exterior.coords[:-1]]
    else:
        for j, other in nearby_contours:
            if i == other:
                continue
            dist = poly.distance(polygons[other])
            if dist < touching_threshold:
                touching_points += list(poly.exterior.coords[:-1])
                touching_points += list(polygons[other].exterior.coords[:-1])
                colors += [img[int(p[1]), int(p[0])] for p in poly.exterior.coords[:-1]]
                colors += [img[int(p[1]), int(p[0])] for p in polygons[other].exterior.coords[:-1]]
            else:
                inter = poly.intersection(polygons[other])
                if inter.geom_type == 'Point':
                    p = np.array(inter.coords[0], dtype=int)
                    intersection_points.append(p)
                    color = img[p[1], p[0]]
                    colors.append(color)

print(len(intersection_points))
print(len(touching_points))
#########################################################

# # Draw circles and print colors
# for p, color in zip(intersection_points + touching_points, colors):
#     if p:
#         print(p)
#         cv2.circle(img, tuple(p), 10, (0, 0, 255), -1)
#         print(f"Color at ({p[0]}, {p[1]}): {color}")

# Display image with contours and intersection points
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#since we need int values in p
px = []
py = []
for p in touching_points:
    x, y = p
    px.append(x)
    py.append(y)


# for p, color in zip(touching_points, colors):
# for px,py, color in zip(touching_points, colors):
# for p, color in zip(touching_points, colors):
for x, y, color in zip(px, py, colors):

    # print(p)
    # p = [(int(x), int(y)) for x, y in p]
    p = [(int(round(x)), int(round(y))) for x, y in zip(px, py)]
    for i in range (len(p)):
        # print(p[i])
        cv2.circle(img, tuple(p[i]), 1, (0, 0, 255), -1)
#     print(f"Color at ({p[0]}, {p[1]}): {color}")
# cv2.circle(img, (195, 88), 10, (0, 0, 255), -1)
# cv2.circle(img, (196, 89), 10, (0, 0, 255), -1)
# cv2.circle(img, (196, 90), 10, (0, 0, 255), -1)
# cv2.circle(img, (196, 88), 10, (0, 0, 255), -1)

# for p in touching_points:
    # cv2.circle(img, (171, 180), 10, (0, 0, 255), -1)
    # cv2.circle(img, ), 10, (0, 0, 255), -1)
    # print(f"Color at ({p[0]}, {p[1]}): {color}")




# for p, color in zip(intersection_points, colors):
#     print(p)
#     cv2.circle(img, tuple(p), 10, (0, 0, 255), -1)
#     print(f"Color at ({p[0]}, {p[1]}): {color}")

# Display image
cv2.imshow('image', img)
cv2.imwrite('final.jpeg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import operator
import sys
import random

def lazySolution(photos):
    solution = list()
    verticalJoin = list()
    slides = list()
    for photo in photos:
        if photo.orientation is "H":
            solution.append(Slide(photo))
        else:
            verticalJoin.append(photo)
            if len(verticalJoin) is 2:
                solution.append(Slide(*verticalJoin))
                verticalJoin = list()
    return solution

def solution2(photos):
    # photos.sort(key=lambda photo : photo.index, reverse=True)
    return lazySolution(photos)

def solution3(photos):
    photos.sort(key=lambda photo : len(photo.tags), reverse=True)
    photos = photos[:8000]
    result = list()

    counter = 0
    while True:
        print("%%%f" % (100.0 * counter / (len(photos) + 1)))
        counter += 1
        
        haveFound = False
        for photo in photos:
            if photo.hasBeenUsed is False:
                haveFound = True
                bestPhoto = photo
                break
        if haveFound is False:
            return result
        
        bestPhoto.hasBeenUsed = True
        if bestPhoto.orientation is "H":
            bestSlide = Slide(bestPhoto)
        else:
            for photo in photos:
                if photo.hasBeenUsed:
                    continue
                if photo.orientation is "V":
                    photo.hasBeenUsed = True
                    bestSlide = Slide(bestPhoto, photo)
                    break

        result.append(bestSlide)

        for photo in bestSlide.photos:
            photos.remove(photo)

        slides = list()
        for index, photo in enumerate(photos):
            if photo.hasBeenUsed:
                continue
            if photo.orientation is "H":
                slide = Slide(photo)
                photo.hasBeenUsed = True
                slide.score = score(bestSlide, slide)
                slides.append(slide)
            else:
                for remainingPhoto in photos[index+1:]:
                    if remainingPhoto.hasBeenUsed is True:
                        continue
                    if remainingPhoto.orientation is "V":
                        remainingPhoto.hasBeenUsed = True
                        slide = Slide(photo, remainingPhoto)
                        slide.score = score(bestSlide, slide)
                        slides.append(slide)
                        break

        if len(slides) is 0:
            return result;

        slides.sort(key=lambda slide: slide.score, reverse=True)
        result.append(slides[0])
        
        for photo in slides[0].photos:
            photos.remove(photo)

        for photo in photos:
            photo.hasBeenUsed = False

        for slides in result:
            for photo in slides.photos:
                photo.hasBeenUsed = True
        

class Photo:
    def __init__(self, *args):
        self.orientation = args[0]
        self.tags = args[1]
        self.index = args[2]
        self.hasBeenUsed = False

class Slide:
    def __init__(self, *args):
        self.tags = set(args[0].tags)
        self.indexes = list()
        self.indexes.append(args[0].index)
        self.score = 0
        self.photos = list()
        self.photos.append(args[0])
        if len(args) > 1:
            self.indexes.append(args[1].index)
            self.photos.append(args[1])
            for tag in args[1].tags:
                self.tags.add(tag)
                
        
def common(slide1, slide2):
    solution = list()
    
    for tag in slide2.tags:
        if tag in slide1.tags:
            solution.append(tag)

    return len(solution)
    
def subtract(slide1, slide2):
    tags = slide1.tags
    for tag in slide2.tags:
        if tag in tags:
            tags.remove(tag)
    return len(tags)

def fullScore(photos):
    total = 0
    for i in range(0, len(photos) - 2):
        total += score(photos[i], photos[i+1])
    return total


def monteCarlo(photos):
    scores = list()
    arrays = list()
    for i in range(0, 30):
        # print photos[1].tags
        random.shuffle(photos)
        arrays.append(lazySolution(photos))
        scores.append(fullScore(arrays[i]))

    max_value = max(scores)
    max_index = scores.index(max_value)

    return arrays[max_index]

def score(slide1, slide2):
    return min(common(slide1, slide2), subtract(slide1, slide2), subtract(slide2, slide1))

fileIn = open(sys.argv[1], "r")

photos = list()

for index, line in enumerate(fileIn):
    if index == 0:
        continue
    photos.append(Photo(line[0], list((line[2:].replace('\n', '').split(" "))[1:]), index - 1))

fileIn.close()

fileOut = open(sys.argv[2], "w")

photos2 = list(photos)
photos2.sort(key=lambda photo : len(photo.tags), reverse=True)
photos2 = photos2[8000:]

solution = solution3(photos)
solution2 = monteCarlo(photos2)

solution.extend(solution2)

fileOut.write("%d" % len(solution))
fileOut.write("\n")

for slide in solution:
    for index in slide.indexes:
        fileOut.write("%d " % index)
    fileOut.write("\n")

fileOut.close()
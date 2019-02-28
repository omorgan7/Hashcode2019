def lazySolution(photos):
    solution = list()
    verticalJoin = list()
    for photo in photos:
        if photo.orientation is "H":
            solution.append(photo.index)
        else:
            verticalJoin.append(photo.index)
            if len(verticalJoin) is 2:
                solution.append(verticalJoin)
                verticalJoin = list()
    return solution

def solution2(photos):
    photos.sort(key=lambda photo : photo.index, reverse=True)
    return lazySolution(photos)
        

class Photo:
    def __init__(self, *args):
        self.orientation = args[0]
        self.tags = args[1]
        self.index = args[2]

class Slide:
    def __init__(self, *args):
        self.tags = set(args[0].tags)
        if args[1]:
            self.tags.append(args[1].tags)
        
def common(slide1, slide2):
    return len(set(slide1.tags, slide2.tags))
    
def subtract(slide1, slide2):
    tags = tags(slide1)
    for tag in slide2.tags:
        if tag in tags:
            tags.remove(tag)
    return len(tags)

def score(slide1, slide2):
    return min(common(slide1, slide2), subtract(slide1, slide2), subtract(slide2, slide1))

fileIn = open("/Users/owen/Downloads/a_example.txt","r")

photos = list()

for index, line in enumerate(fileIn):
    if index == 0:
        continue
    photos.append(Photo(line[0], list(line[2:].replace('\n', '').split(" ")), index - 1))

fileIn.close()

fileOut = open("output.txt", "w")

solution = solution2(photos)

fileOut.write("%d" % len(solution))
fileOut.write("\n")

for numbers in solution:
    if type(numbers) is list:
        for x in numbers:
            fileOut.write("%d " % x)
        fileOut.write("\n")
    else:
        fileOut.write("%d\n" % numbers)

fileOut.close()
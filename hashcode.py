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
        if len(args) > 1:
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

def score(slide1, slide2):
    return min(common(slide1, slide2), subtract(slide1, slide2), subtract(slide2, slide1))

fileIn = open("/Users/owen/Downloads/a_example.txt","r")

photos = list()

for index, line in enumerate(fileIn):
    if index == 0:
        continue
    photos.append(Photo(line[0], list((line[2:].replace('\n', '').split(" "))[1:]), index - 1))

fileIn.close()

fileOut = open("output.txt", "w")

solution = solution2(photos)

for x in solution:
    print(x.tags)

print(score(solution[0], solution[1]))
print(score(solution[1], solution[2]))

fileOut.write("%d" % len(solution))
fileOut.write("\n")

for numbers in solution:
    if type(numbers) is list:
        for x in numbers:
            fileOut.write("%d " % x.index)
        fileOut.write("\n")
    else:
        fileOut.write("%d\n" % numbers.index)

fileOut.close()
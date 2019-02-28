def lazySolution(photos):
    solution = list()
    verticalJoin = list()
    for index, photo in enumerate(photos):
        if photo.orientation is "H":
            solution.append(index)
        else:
            verticalJoin.append(index)
            if len(verticalJoin) is 2:
                solution.append(verticalJoin)
                verticalJoin = list()
    return solution
        

fileIn = open("/Users/owen/Downloads/a_example.txt","r")

class Photo:
    def __init__(self, *args):
        self.orientation = args[0]
        self.tags = args[1]

photos = list()

for index, line in enumerate(fileIn):
    if index == 0:
        continue
    photos.append(Photo(line[0], list(line[2:].replace('\n', '').split(" "))))

fileIn.close()

fileOut = open("output.txt", "w")

solution = lazySolution(photos)

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
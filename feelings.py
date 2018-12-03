# Code for feeling translation in ARTuid
# Maria Markovska

from random import shuffle 
import copy

# Feelings class to translate from feelings to light parameters
class Feeling:
	def __init__(self, pattern, color=0, background=0, direction=0, size=0):
		self.pattern = pattern;
		self.color = color;
		self.background = background;
		self.direction = direction;
		self.size = size;

# Functions that return feeling objects according to the artists translation
def Anger():
	return Feeling('1')

def Fear():
	return Feeling('2')

def Joy():
	return Feeling('3')

def Sadness():
	return Feeling('4')

def Analytical():
	return Feeling('5')

def Confident():
	return Feeling('6')

def Tentative():
	return Feeling('7')

# Input: values on all feelings (0-1)
# Output: list of feeling objects that contains parameters for all 18 arm links
def normalize(anger = 0, fear=0, joy=0, sadness=0, analytical = 0, confident=0, tentative = 0):
	# Calculate a total
	total = anger + fear + joy + sadness + analytical + confident + tentative
	
	# Calculate percentages
	anger_percent = anger/float(total)
	fear_percent = fear/float(total)
	joy_percent = joy/float(total)
	sadness_percent = sadness/float(total)
	analytical_percent = analytical/float(total)
	confident_percent = confident/float(total)
	tentative_percent = tentative/float(total)

	# Calculate how many links will have each feeling (total nr of links is 18)
	anger_links = round(anger_percent*18)
	fear_links = round(fear_percent*18)
	joy_links = round(joy_percent*18)
	sadness_links = round(sadness_percent*18)
	analytical_links = round(analytical_percent*18)
	confident_links = round(confident_percent*18)
	tentative_links = round(tentative_percent*18)

	# print anger_links
	# print fear_links
	# print joy_links
	# print sadness_links
	# print analytical_links
	# print confident_links
	# print tentative_links

	# Create list of all the feelings
	feels = []

	for i in range(0,int(anger_links)):
		feels.append(Anger())

	for i in range(0,int(fear_links)):
		feels.append(Fear()) 

	for i in range(0,int(joy_links)):
		feels.append(Joy())

	for i in range(0,int(sadness_links)):
		feels.append(Sadness())

	for i in range(0,int(analytical_links)):
		feels.append(Analytical())

	for i in range(0,int(confident_links)):
		feels.append(Confident())

	for i in range(0,int(tentative_links)):
		feels.append(Tentative()) 

	#print len(feels)

	# Scramble the list in random order
	shuffle(feels)

	# Return the scrambled list with feeling objects
	return feels











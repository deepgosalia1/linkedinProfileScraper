# linkedinProfileScraper
Scrape the profiles of connections (profiles provided in a SEPARATE CSV) on linkedin, 
provided you obtain the list of you connections from linkedin userdata in linkedin Settings

## required files:
1. Downloaded chrome webdriver(based on the version of your chrome browser) should be located in the same directory where this python file is. (along with 'input.csv' in the same directory).
2. 'input.csv' file of profileLinks of the profiles you want scrapped. Name of the column in the csv does not matter, but the first column should contain the links of those profiles only.
3. To run, open cmd, and navigate to this folder, type 'py linkedinScraper.py'

## sample csv output row:
{Name};{location};{position};{company};{email};

John Doe 	Mumbai, Maharashtra, India	A budding computer Science student University of Michigan	JohnDoe@gmail.com imageHyperTextHere

## sample csv input row: (only the profileUrl field is required in the input csv)
profileUrl	firstName	lastName	fullName	title	connectionSince	profileImageUrl	timestamp

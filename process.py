import os, codecs, re, glob, fileinput, shutil
from operator import itemgetter
from jinja2 import Template, Environment, FileSystemLoader

def process_file(f):
    # Get the source file
    source = codecs.open(f, 'r', 'utf-8')

    # Read the text from the source file
    content = source.read().lower()

    # Strip punctuation and numbers
    content = re.sub(r"[^a-z\s]+", '', content, 0, re.IGNORECASE)
    # Remove line breaks/carriage returns
    content = re.sub(r"[\r\n]+", '', content, 0, re.IGNORECASE)
    # Replace multiple spaces with single spaces
    content = re.sub(r"\s+", ' ', content, 0, re.IGNORECASE)

    # Write the processed text out to a file
    # destination = codecs.open('text/output.txt', 'w', 'utf-8')
    # destination.write(content)
    # destination.close()

    # Split the content at space characters
    words = content.split(' ')

    # Remove empty strings from the list
    words = filter(None, words)

    # Dictionary: word as key, occurrences as value
    wordcount = {}

    for word in words:
        w = word.lower()
        if w not in stopwords: # If it's a stop word, ignore it
            if w not in wordcount: # If we haven't already seen the word
                wordcount[w] = 0 # Add it to the dictionary
            wordcount[w] += 1 # Increment the total occurrences
        
    # Get a list of the items sorted by descending value (occurrences)
    st = sorted(wordcount.items(), key=itemgetter(1), reverse=True)

    # Show everything with more than X occurrences
    #debug = [s[0] + ': ' + str(s[1]) for s in st if s[1] > 20]
    #for result in debug:
    #    print result

    filename = os.path.split(f)[1]
    output_filename = re.sub(r"(?si)^(.*\.)(txt)$", r"\1html", filename)
    output = template.render(title=output_filename, words=[s for s in st if s[1] > 5])
    # Write out the processed HTML file for this post
    o = codecs.open('output/' + output_filename, 'w', 'utf-8')
    o.write(output)
    o.close()



# Load the output templates
env = Environment(loader=FileSystemLoader('template/'))
template = env.get_template('template.html')

# Copy the CSS file to the output directory
shutil.copyfile('template/styles.css', 'output/styles.css')

# Get the list of stop words from our text file
file = open('stopwords.txt', 'r')
# Remember to strip the newline characters so they match our words
stopwords = [str(line).rstrip() for line in file]

# Get all the text files
text_files = [f for f in glob.glob('text/*.txt')]

for f in text_files:
    process_file(f)
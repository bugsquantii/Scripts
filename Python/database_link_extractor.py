import sqlite3
import re
import optparse


parser = optparse.OptionParser()
parser.add_option('-i', '--input', dest='input', help='Input database file')
parser.add_option('-o', '--output', dest='output', help='Output database file')
parser.add_option('-t', '--type', dest='type', help='sqlite, txt')
(options, args) = parser.parse_args()

if not options.input:
    parser.error('Input database file not provided')
if not options.output:
    parser.error('Output database file not provided')    

dbFile = options.input  # Input database
outputDBFile = options.output  # Output database

# Function to extract HTTPS links from text
def extract_https_links(text):
    https_pattern = r'https://[^\s]+'
    return re.findall(https_pattern, text)


# Establish a connection to the input database
conn_source = sqlite3.connect(dbFile)
cursor_source = conn_source.cursor()

# Retrieve all tables in the input database
cursor_source.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_source.fetchall()

# Store HTTPS links in a list
https_links = []
for table in tables:
    table_name = table[0]
    sql_query = f"SELECT * FROM {table_name}"
    cursor_source.execute(sql_query)
    table_data = cursor_source.fetchall()
    for row in table_data:
        for cell in row:
            if cell:
                links_in_cell = extract_https_links(str(cell))
                https_links.extend(links_in_cell)

# Close the connection to the input database
conn_source.close()

if options.type == 'txt':
    with open(options.output + '.txt', 'w') as f:
        for link in https_links:
            f.write(f'{link}\n')
else:

    # Establish a connection to the output database
    conn_target = sqlite3.connect(outputDBFile + '.db')
    cursor_target = conn_target.cursor()

    # Create a table in the output database if it doesn't exist
    cursor_target.execute('''CREATE TABLE IF NOT EXISTS https_links (link TEXT)''')

    # Check if the links already exist in the output database and only add them if they do not exist
    for link in https_links:
        cursor_target.execute("SELECT link FROM https_links WHERE link=?", (link,))
        existing_link = cursor_target.fetchone()
        if not existing_link:
            cursor_target.execute("INSERT INTO https_links (link) VALUES (?)", (link,))

    # Save changes in the output database and close the connection
    conn_target.commit()
    conn_target.close()
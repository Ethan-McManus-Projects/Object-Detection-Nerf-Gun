# Define the file path
file_path = 'C:/Users/ethan/notebooksmlprojects/labelmap.pbtxt'

# Define the content to be written to the file
content = """
item {
  id: 1
  name: 'white'
}
item {
  id: 2
  name: 'black'
}
item {
  id: 3
  name: 'brown'
}
item {
  id: 4
  name: 'yellow'
}
"""

# Create and write to the file
with open(file_path, 'w') as file:
    file.write(content)

print(f'File created at {file_path}')
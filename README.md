# Just Cause modding tool bank

A collection of powerful tools to elevate and accelerate your Just Cause modding experience 🛠️.
Currently contains 1 tool category and 6 variants

# Tools list

### @files.xml and @tocFiles.xml generator

#### Description
This generator is capable of creating two xml files that contain the relative paths to each file in a folder, including files in its sub-folders, as well as existing external paths.  

These xml files can then be used as a reference for repacking .ee archives using standard JC tools.
#### Pros
- Reduces the time spent on adding files
- Reduces writing errors
- Provides a good file sorting
#### Cons
- Less control over the xml file
- Does not handle that much xml error detection atm
#### Other
Does not include .xml files when processing

### External path generator

#### Description
This generator can make external paths from files or multiples folders with their size. These paths are then used in the @files.xml and @tocFiles.xml.  
#### Pros
- Reduces the time spent on adding files
- Reduces writing errors
- Write the correct size of a file
#### Cons
- No paths sorting based on extensions yet.
- Does not add these paths automatically in @files.xml and @tocFiles.xml yet.
#### Other
the "OutputTXT" version of the exe generates a txt in the folder of the last generated path, useful if the amout of file is very high.

### DDSC/DDS converter

#### Description
Can convert dds images based on their header as ddsc textures files.
#### Pros
- Can handle files and folders in just one drag and drop
- Detects DDS or DDSC files based on their header, not their extension
- Gives information about the input file and errors detection
- Fast
#### Cons
- Does not support .atx and .hmddsc textures yet.
#### Other
if there are dds and ddsc files with the same name dragged and dropped together at the same time, the exe won't be able to convert them, it will show an error
#### Credits
Based on [Brooen](https://github.com/Brooen/)'s script: https://github.com/Brooen/DDS-to-DDSC-Converter

# Usage
### EXEs
ddsc/dds converter: drag and drop files and/or folders at the same time
External path generator: drag and drop files and/or folders at the same time
@files.xml and @tocFiles.xml generator: drag and drop only one folder

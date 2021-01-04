# Huffman Compression

## Introduction ✏️
Math-Info project carried out in 2019, as part of studies in the engineering 
preparatory cycle. The aim of the project is to reduce the size of the files, 
as much as possible, as desired using the Huffman method.

All scripts are written in UTF-8, the docstring and comments are in UTF-8
comply with the standard PEP 484(https://www.python.org/dev/peps/pep-0484/) 
as follows
than the standard for Docstrings 
Google(http://google.github.io/styleguide/pyguide.html).

All the libraries used are native.


## Objectives ✔️
Implement a compression algorithm, recursively, reducing the size of the files.
With the Huffman method.
#### Bonus 🥉
It is possible to decompress previously compressed files. Always by the Huffman 
method.

## Start the program 🏁

To do this, open the ``Main.py`` file in a terminal.
A graphical window opens :

You can choose between compressing or decompressing a document.

Only ``.hf`` files can be unzipped. This is an extension created for de Huffman
compression.

### Compression

To compress a file, of any size or type, click on the ``Compression``button.
And choose the file you are interested in.


You can then choose the directory and name of your file to be saved. Here 
``logo.hf``.

When the file compression is complete, you will hear an audible alert 
(Windows only). And you see the statistics of the compressed file. 

So we have :
* The name of file to be compressed
* Size in bytes
* Number of different bytes in the file
* The Huffman tree's construction time
* The size of the file after compression
* Byte gain in percent
* Entropy in base 2 designates the minimum number of bits per symbol that our 
information takes
* Average byte size after compression
* Writing time of the file

File name     | File size (bytes) | Different number of bytes | Gain   | Entropy |
------------  | ----------------- | ------------------------- | ------ | ------- |
fichier_1.txt |	10 347            |	38                        | 41,49% | 4,10    |
fichier_2.txt |	20 597            |	42                        | 44,57% | 4,10    |
fichier_3.txt |	102 843           | 42                        | 47,71% | 4,10    |
fichier_4.txt |	1 028 560         |	42                        | 48,42% | 4,10    |
fichier_5.txt |	10 285 870        |	42                        | 48,49% | 4,10    |
fichier_6.txt |	102 864 419       |	42                        | 48,50% | 4,10    |

These are only examples of the results of file compression according to their
size. Depending on the files these results change. As a general rule, the 
larger the file, the greater the byte gain. Up to 90%. But the operation takes
longer.

### Decompression

As before, click on the ``Décompression`` button. Once you have selected the 
file you are interested in, save it where you want. 

Only ``.hf`` files can be unzipped and are displayed in the file explorer.

When the file decompression is complete, you will hear an audible alert 
(Windows only). And you see the statistics of the compressed file.

So we have :
* The name of the file to decompress
* The name of the file decompressed
* Number of bytes of the dictionary, where the data of the binary aber is 
stored.
* The size of the file after decompression
* Execution time 

File name     | Dictionary size (bytes) | 
------------  | ----------------------- | 
fichier_1.txt |	690                     |	
fichier_2.txt |	793                     |	
fichier_3.txt |	787                     |
fichier_4.txt |	788                     |
fichier_5.txt |	785                     |	
fichier_6.txt |	787                     |

**These are only examples of the results of file decompression according to 
their size. Depending on the files these results change.**

## Limits ⚠️
* The code is in French 🇫🇷
* It is not possible to compress folders, only files
* We choose to have a strong compression but an important execution time
* The binary tree is specific to each file. It increases the execution time, 
but is more efficient.
* The binary tree is saved in the compressed file. It increases its size
* Little or no efficiency with small files for the reasons mentioned above
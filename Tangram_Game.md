### Tangram Game
#### Background

The game of tangram consists in creating shapes out of pieces. We assume that each piece has its own colour, different to the colour of any other piece in the set we are working with.

A representation of the pieces will be stored in an .xml file thanks to a simple, fixed syntax.

**Pieces:**  
Here is an example of the contents of the file pieces_A.xml, typical of the contents of any file of this kind (so only the number of pieces, the colour names, and the various coordinates can differ from one such file to another–we do not bother with allowing for variations, in the use of space in particular).

```
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M 50 50 L 50 90 L 90 90 z" fill="red"/> 
<path d="M 160 170 L 160 130 L 120 130 z" fill="green"/> 
<path d="M 200 30 L 180 30 L 180 50 L 220 50 z" fill="blue"/> <path d="M 40 100 L 40 140 L 60 140 L 60 120 z" fill="yellow"/> <path d="M 210 70 L 230 90 L 270 90 L 270 50 L 230 50 z" fill="purple"/> 
<path d="M 180 130 L 180 170 L 220 210 L 240 190 z" fill="olive"/> 
<path d="M 100 200 L 120 180 L 80 140 L 80 180 z" fill="magenta"/> 
</svg>
```

Note that the coordinates are nonnegative integers. This means that the sets of pieces we consider rule out √ those of the traditional game of tangram, where 2 is involved everywhere...

We require every piece to be a convex polygon. An .xml file should represent a piece with n sides (n ≥ 3) by an enumeration of n pairs of coordinates, those of consecutive vertices, the first vertex being arbitrary, and the enumeration being either clockwise or anticlockwise.

**Shapes:**. 
A representation of a shape is provided thanks to an .xml file with the same structure, storing the coordinates of the vertices of just one polygon. One example is as below:
```
<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M 30 20 L 110 20 L 110 120 L 30 120 z" fill="grey"/> </svg>
```
<svg version="1.1" xmlns="http://www.w3.org/2000/svg"> <path d="M 30 20 L 110 20 L 110 120 L 30 120 z" fill="grey"/> </svg>

**Problem 1:**  
Have to check that the pieces represented in an .xml file satisfy our constraints. So you have to check that each piece is convex, and if it represents a polygon with n sides (n ≥ 3) then the representation consists of an enumeration of the n vertices, either clockwise or anticlockwise. Here is the expected behaviour of your program.

**Problem 2:**  
You have to check whether the sets of pieces represented in two .xml files are identical, allowing for pieces to be flipped over and allowing for different orientations. Here is the expected behaviour of your program.

**Problem 3:**  
You have to check whether the pieces represented in an .xml file are a solution to a tangram puzzle represented in another .xml file.

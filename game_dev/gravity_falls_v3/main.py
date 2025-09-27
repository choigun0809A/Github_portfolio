import pygame as py
import sys, copy, numpy, math
from src import blocks

py.init()

def level(width: float, height: float):
    blockss: dict[int, list[blocks.Block]] = {}
    objectss: dict[int, list] = {}
    spawns: dict[int, py.rect.FRect] = {}
    centers: dict[int, list] = {}
    backgrounds: dict[int, py.rect.FRect] = {}
    lvl = 0

    lvl1 = [
        "############",
        "#oooooooooo#",
        "#o$ooooooo@#",
        "############",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
    
    lvl += 1

    lvl1 = [
        "############",
        "#oooooooooo#",
        "#$oo|'^oo*@#",
        "####kwE##e##",
        "####kwE##e##",
        "####kwE##e##",
        "####kwE##e##",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "'":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        1,
                        1,
                        False
                    )
                )
            elif char == "w":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        py.Color(0, 0, 0),
                        1
                    )
                )
            elif char == "^":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        2,
                        1,
                        False
                    )
                )
            elif char == "E":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        py.Color(0, 0, 0),
                        2
                    )
                )
            elif char == "*":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        3,
                        1,
                        False
                    )
                )
            elif char == "e":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        3
                    )
                )
            elif char == "|":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        5,
                        1,
                        False
                    )
                )
            elif char == "k":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        5
                    )
                )
    lvl += 1
    

    lvl1 = [
        "############",
        "#####EEEEE##",
        "#oooooooooo#",
        "#o@oo^oooo$#",
        "############",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "^":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        1,
                        1,
                        False
                    )
                )
            elif char == "E":
                objectss[lvl].append(
                    blocks.Falling_block(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        1,
                        3,
                        2500,
                        True
                    )
                )
    lvl += 1



    lvl1 = [
        "###############",
        "#Eoooooooooooo#",
        "#hoooooooooooe#",
        "#ooooooooooooo#",
        "#o$owb!o*o^o@o#",
        "########k######",
        "########k######",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "^":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        1,
                        1,
                        False
                    )
                )
            elif char == "!":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        10,
                        1,
                        False
                    )
                )
            elif char == "E":
                objectss[lvl].append(
                    blocks.Falling_block(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size*13, size
                        ),
                        None,
                        10,
                        0.5,
                        10000,
                        True
                    )
                )
            elif char == "e":
                objectss[lvl].append(
                    blocks.Sliding_block(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size*4
                        ),
                        None,
                        1,
                        -2,
                        10000,
                        True,
                        True,
                    )
                )
            elif char == "b":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        2,
                        1,
                        False
                    )
                )
            elif char == "h":
                objectss[lvl].append(
                    blocks.Sliding_block(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size*3
                        ),
                        None,
                        2,
                        0.5,
                        10000,
                        True
                    )
                )
            elif char == "w":
                s_h = size/2.5
                objectss[lvl].append(
                    blocks.Magic_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + size - s_h + centers[lvl][1],
                            size, s_h
                        ),
                        py.color.Color(0, 0, 0),
                        2
                    )
                )
            elif char == "*":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        5,
                        1,
                        False
                    )
                )
            elif char == "k":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        5
                    )
                )
    
    
    lvl += 1


    lvl1 = [
        "###############",
        "#hoooooooooooo#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o$o*ooooo^oo@#",
        "###kk##########",
        "###kk##########",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "^":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        1,
                        1,
                        False
                    )
                )
            elif char == "h":
                objectss[lvl].append(
                    blocks.Slide_pushing_block(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size*4
                        ),
                        None,
                        1,
                        5.2,
                        3000,
                        True
                    )
                )
            elif char == "*":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        2,
                        1,
                        False
                    )
                )
            elif char == "k":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size + centers[lvl][0], 
                            y*size + centers[lvl][1],
                            size, size
                        ),
                        None,
                        2,
                    )
                )
            
    
    
    lvl += 1


    lvl1 = [
        "###############",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o@ooooooooo$o#",
        "###############",
        "###############",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
           
            
    
    
    lvl += 1


    lvl1 = [
        "###############",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o$ooooooooo@o#",
        "###############",
        "###############",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
           
            
    
    
    lvl += 1

    lvl1 = [
        "###############",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o@oooooo*oo$o#",
        "#########kk####",
        "#########kk####",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "*":
                blck = blocks.Trigger(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0),
                    10,
                    1,
                    False
                )
                objectss[lvl].append(blck)
            elif char == "k":
                blck = blocks.Trap_door(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    None,
                    10,
                )
                objectss[lvl].append(blck)

            
    
    
    lvl += 1


    lvl1 = [
        "###############",
        "eooooooooooooo#",
        "oooooooooooooo#",
        "oooooooooooooo#",
        "o^ooooooooo@o*$",
        "#############k#",
        "#############k#",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "^":
                blck = blocks.Trigger(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(0, 0, 0, 0),
                    2,
                    1,
                    True
                )
                objectss[lvl].append(blck)
            elif char == "e":
                objectss[lvl].append(
                    blocks.Sliding_block(
                        py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size*4,
                        ),
                        None,
                        2,
                        1,
                        25000,
                        True,
                        False,
                    )
                )
            elif char == "*":
                blck = blocks.Trigger(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0),
                    4,
                    1,
                    False
                )
                objectss[lvl].append(blck)
            elif char == "k":
                objectss[lvl].append(
                        blocks.Trap_door(
                            py.rect.FRect(
                            x * size + centers[lvl][0], 
                            y * size + centers[lvl][1], 
                            size, 
                            size,
                        ),
                        py.color.Color(0, 0, 0, 0),
                        4

                    )
                )
    lvl += 1


    lvl1 = [
        "###############",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o$oooooo@ooKo#",
        "###############",
        "###############",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(100, 100, 100),
                    True,
                    1
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "K":
                si = size/2
                si_y = si/2
                objectss[lvl].append(
                    blocks.Door_Trigger(
                        py.rect.FRect(
                            x*size + size/2 - si/2 + centers[lvl][0],
                            y*size + size/2 - si_y/2 + centers[lvl][1],
                            si,
                            si_y,
                        ),
                        py.color.Color(250, 150, 30),
                        1, 
                        True
                    )
                )
           
            
    
    
    lvl += 1


    lvl1 = [
        "###############",
        "#ooooooooooooe#",
        "#ooooooooooooo#",
        "#ooooooooooooo#",
        "#o@ooo$o!oo*Ko#",
        "#o#ooo#oooggmo#",
        "#ooooooooooooo#",
    ]
    size = width / max(len(lvl1[0]), len(lvl1))
    door_size = (size/3, size/2)

    blockss[lvl] = []
    objectss[lvl] = []
    centers[lvl]= [width/2 - len(lvl1[0])/2*size, height/2 - len(lvl1)/2*size]
    backgrounds[lvl] = py.rect.FRect(
        centers[lvl][0], 
        centers[lvl][1],
        len(lvl1[0])*size,
        len(lvl1)*size,
    )
    for y in range(len(lvl1)):
        for x in range(len(lvl1[y])):
            char = lvl1[y][x]
            if char == "#":
                blck = blocks.Block(
                    py.rect.FRect(
                        x * size + centers[lvl][0], 
                        y * size + centers[lvl][1], 
                        size, 
                        size,
                    ),
                    py.color.Color(0, 0, 0, 0)
                )
                blockss[lvl].append(blck)
            elif char == "$":
                blck = blocks.Door(
                    py.rect.FRect(
                        x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                        y * size + size - door_size[1] + centers[lvl][1], 
                        door_size[0], 
                        door_size[1],
                    ),
                    py.color.Color(100, 100, 100),
                    True,
                    1
                )
                objectss[lvl].append(blck)
            elif char == "@":
                spawns[lvl] = py.rect.FRect(
                    x * size + size/2 - door_size[0]/2 + centers[lvl][0], 
                    y * size + size - door_size[1] + centers[lvl][1], 
                    door_size[0], 
                    door_size[1],
                )
            elif char == "K":
                si = size/2
                si_y = si/2
                objectss[lvl].append(
                    blocks.Door_Trigger(
                        py.rect.FRect(
                            x*size + size/2 - si/2 + centers[lvl][0],
                            y*size + size/2 - si_y/2 + centers[lvl][1],
                            si,
                            si_y,
                        ),
                        py.color.Color(250, 150, 30),
                        1, 
                        True
                    )
                )
            elif char == "!":
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size+centers[lvl][0],
                            y*size+centers[lvl][1],
                            size,
                            size
                        ),
                        None,
                        1,
                        1,
                        False
                    )
                )
            elif char == "g":
                objectss[lvl].append(
                    blocks.Magic_door(
                        py.rect.FRect(
                            x*size+centers[lvl][0],
                            y*size+centers[lvl][1],
                            size,
                            size
                        ),
                        None,
                        1
                    )
                )
            elif char == "m":
                objectss[lvl].append(
                    blocks.Trap_door(
                        py.rect.FRect(
                            x*size+centers[lvl][0],
                            y*size+centers[lvl][1],
                            size,
                            size
                        ),
                        None,
                        2
                    )
                )
            elif char == "*":
                s_x = size/3
                objectss[lvl].append(
                    blocks.Trigger(
                        py.rect.FRect(
                            x*size + size - s_x +centers[lvl][0],
                            y*size+centers[lvl][1],
                            s_x,
                            size
                        ),
                        None,
                        2,
                        1,
                        False
                    )
                )
            
    
    
    lvl += 1

    return (blockss, objectss, spawns, backgrounds)

class Game:
    def __init__(self):
        self.screen = py.display.set_mode((1200, 850))
        py.display.set_caption("Don't look up!")


        load = level(self.screen.get_width(), self.screen.get_height())
        self.level = 0
        self.blocks: dict[int, list[blocks.Block]] = copy.deepcopy(load[0])
        self.objects: dict[int, list] = copy.deepcopy(load[1])
        self.copy_object = copy.deepcopy(load[1])
        self.copy_blocks = copy.deepcopy(load[0])
        self.spawn: dict[int, py.rect.FRect] = load[2]
        self.backgrounds: dict[int, py.rect.FRect] = load[3]

        self.player = blocks.Player(self.spawn[self.level].copy())

    def main(self):
        clock = py.time.Clock()
        while True:
            self.screen.fill("BLACK")

            try:
                self.loop()
            except:
                text = "GAME OVER"
                font = py.font.Font(None, 25)
                d_text = font.render(text, True, "WHITE")
                size = d_text.get_size()
                self.screen.blit(
                    d_text,
                    (
                        self.screen.get_width()/2 - size[0]/2,
                        self.screen.get_height()/2 - size[1]/2,
                    )
                    )

            py.display.flip()
            clock.tick(60)
            for e in py.event.get():
                if e.type == py.QUIT:
                    py.quit()
                    sys.exit()


    def loop(self):
        py.draw.rect(
            self.screen,
            "YELLOW",
            self.backgrounds[self.level]
        )

        for block in self.blocks[self.level]:
            if block.draw:
                py.draw.rect(
                    self.screen, 
                    block.color, 
                    py.rect.FRect(
                        block.rect.x,
                        block.rect.y,
                        block.rect.width,
                        block.rect.height,
                    )
                )

        adder = []
        for obj in self.objects[self.level]:
            if isinstance(obj, blocks.Door):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                if obj.check(self.player) or py.key.get_just_pressed()[py.K_RSHIFT]:
                    
                    self.level += 1
                    self.player.rect = self.spawn[self.level].copy()
                
            elif isinstance(obj, blocks.Trap_door):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                
            elif isinstance(obj, blocks.Trigger):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                if obj.collision:
                    print("this is fuck")
                if obj.count != 0:
                    if obj.check(self.player.rect):
                        obj.count -= 1
                        for obj1 in self.objects[self.level]:
                            if (isinstance(obj1, blocks.Trap_door) or isinstance(obj1, blocks.Sliding_block) or isinstance(obj1, blocks.Slide_pushing_block) or isinstance(obj1, blocks.Falling_block) or isinstance(obj1, blocks.Magic_door) or isinstance(obj1, blocks.Slide_pushing_block)) and obj1.code == obj.target_code:
                                obj1.Activate()
                
            elif isinstance(obj, blocks.Falling_block):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                if obj.Move_check(self.player.rect):
                    self.restart_level()

            elif isinstance(obj, blocks.Sliding_block):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                if obj.Move_check(self.player.rect):
                    self.restart_level()

            elif isinstance(obj, blocks.Magic_door):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
            
            elif isinstance(obj, blocks.Slide_pushing_block):
                if obj.draw:
                    py.draw.rect(
                        self.screen,
                        obj.color,
                        obj.rect,
                    )
                obj.Move_check(self.player.rect)

            elif isinstance(obj, blocks.Door_Trigger):
                if obj.draw:
                    rect = copy.deepcopy(obj.rect)
                    rect.y += obj.xo * math.sin(obj.float_speed * py.time.get_ticks()/1000)
                    py.draw.rect(self.screen, obj.color, rect)
                    # print(1, rect,  math.sin(obj.float_speed * py.time.get_ticks(), py.time.get_ticks()/100))

                if obj.check(self.player.rect):
                    for ob in self.objects[self.level]:
                        if isinstance(ob, blocks.Door):
                            ob.Activate()
                            obj.draw = False
                            break

            if obj.collision:
                adder.append(obj)

        blocks11 = self.blocks[self.level].copy()+adder.copy()
        self.player.Move(blocks11)

        # draw player
        py.draw.rect(
            self.screen,
            self.player.color,
            self.player.rect
        )
        self.restart_level_checker(self.backgrounds[self.level])

    def restart_level_checker(self, rect: py.rect.FRect):
        if not rect.colliderect(self.player.rect):
            # if self.objects[self.level] == self.copy_object[self.level].copy():
            #     print("is equal")
            self.objects = copy.deepcopy(self.copy_object)
            self.blocks = copy.deepcopy(self.copy_blocks)
            self.player.rect = self.spawn[self.level].copy()
            self.player.velocity = blocks.Vector()

    def restart_level(self):
        self.objects = copy.deepcopy(self.copy_object)
        self.blocks = copy.deepcopy(self.copy_blocks)
        self.player.rect = self.spawn[self.level].copy()
        self.player.velocity = blocks.Vector()
        

Game().main()
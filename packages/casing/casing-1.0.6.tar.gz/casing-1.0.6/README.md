# casing

This project aim to manage automatically you casing names of variables.

## Usage

There is 3 functions that you save you time:
    
`casing.analyse` will parse your string.

    >>> casing.analyze("stringToDetect")
    >>> ['string', 'to', 'detect']
    
`casing.transform` will transform a string or a list into a casing.

    >>> casing.transform("stringToDetect", case="snake")
    >>> "string_to_detect"
    
    >>> casing.transform(['string', 'to', 'detect'], case="snake")
    >>> "string_to_detect"

`casing.detect` will detect the casing of a string.

    >>> casing.detect("string_to_detect")
    >>> "snake"
    

## Options
You can switch between all this cases:

attachedcase: stringtodetect 
attacheduppercase: STRINGTODETECT 
camelcase: stringToDetect    
dashcase: string-to-detect   
dashuppercase: STRING-TO-DETECT   
normalcase: string to detect 
normaluppercase: STRING TO DETECT 
pascalcase: StringToDetect   
prettycase: String To Detect 
reversedcase: string To Detect    
sentencecase: String to detect    
snakecase: string_to_detect  
snakeuppercase: STRING_TO_DETECT


[![Build Status](https://travis-ci.org/vincentBenet/casing.svg?branch=main)](https://travis-ci.org/vincentBenet/casing)
[![Coverage Status](https://coveralls.io/repos/github/vincentBenet/casing/badge.svg)](https://coveralls.io/github/vincentBenet/casing)

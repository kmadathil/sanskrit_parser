# sanskrit_parser
Parsers for Sanskrit / सम्स्कृतम् 


## Seq2Seq based Sanskrit Parser

See: Grammar as a Foreign Language : Vinyals & Kaiser et. al. Google
http://arxiv.org/abs/1412.7449

* Method: Seq2Seq Neural Network (n? layers)
* Input Embedding with word2vec (optional)

### Input
Sanskrit sentence
### Output
Sentence split into padas with tags
### Train/Test data
DCS corpus , converted by Vishvas Vasuki


## Sanskrit Parser Stack

Stack of parsing tools

### Level 0) 
Sandhi splitting subroutine 
       Input: Phoneme sequence and Phoneme number to split at 
       Action: Perform a sandhi split at given input phoneme number
       Ouptut:  left and right sequences (multiple options will be output). 
       No semantic validation will be performed (up to higher levels)

### Level 1
* From dhatu + lakAra + puruSha + vachana to pada and vice versa
* From prAtipadika + vibhakti + vachana to pada and vice versa
* Upasarga + dhAtu forms - forward and backwards
* nAmadhAtu forms
* Krt forms  - forwards and backwards
* Taddhita forms  - forwards and backwards

### Level 2

#### Input
Sanskrit Sentence
#### Action
*   Traverse the sentence, splitting it (or not) at each location to determine all possible valid splits
*   Traverse from left to right
*   Using dynamic programming, assemble the results of all choices
 
      To split or not to split at each phoneme
      
      If split, all possible left/right combination of phonemes that can result
      
      Once split, check if the left section is a valid pada (use level 1 tools to pick pada type and tag morphologically) 
      
      If left section is valid, proceed to split the right section
* At the end of this step, we will have all possible syntactically valid splits with morphological tags 

#### Output
All semantically valid sandhi split sequences

###    Level 3
#### Input
Semantically valid sequence of tagged padas (output of Level 1)
#### Action:
* Assemble graphs of morphological constraints 

    viseShaNa - viseShya

    karaka/vibhakti
    
    vachana/puruSha constraints on tiGantas and subantas
* Check validity of graphs
#### Output
1.  Is the input sequence a morphologically valid sentence?
1.  Enhanced sequence of tagged padas, with karakas tagged, and a dependency graph associated

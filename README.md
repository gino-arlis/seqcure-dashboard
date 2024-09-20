# This repo is a reorganization of the seqcure dashboard created with the RISC 2024 interns.

## Notes
* The most significant change is the file structure, that separates code from data
* The new file structure is an indication of how the repo should be organized, so the structure can change by changing the names of the folder or adding new ones as long as the principle of partitioning the repo in an organized way is preserved
* Of course as a side effect of this reorg nothing works as of today
* I (gino) will be concentrating on the dashboard but the main effort will probably be on making the code work again 
* When you work on the repo you should do it from your own branch and when code is tested and you fill confident let's work on merging to the development branch
* Merging to the master branch should be very carefully done,. since we envision the dashboard eventually reaching other people and this would be the visible branch

## Goals
* Re-factoring all the code (for legibility and efficiency ) is a large endevour, so instead for now lets try to modularize the code into small (~50-100 lines) manageable chunks (functions) of code. 
* As much as possible let\'s make functions pretty much black boxes, well defined inputs and outputs with no leakage (docstrings are your friend, or will be)
* File naming conventions should be logical and easy to grasp. 
* When in doubt reread "The Zen of Python":


### The Zen of Python

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

Comments, suggestions? 

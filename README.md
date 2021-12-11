# 50.007 Machine Learning Project

Developed by: Chua Qi Bao (1004494), Ng Peng Yu (1004269), Yap Swee En (1004340)

## How to Run the Code

### Requirements 
Please make sure you have installed Python 3.4 or above!

### Getting started
1. Clone the repository on your local machine
```
git clone https://github.com/sutd-50-007-ml-project/Project.git
```
2. Navigate into the `Project` folder
```
cd path-to-repository
cd Project
```


### Question 1

1. Run the code with your training and test set files, and indicate the path for the output.
```
python3 Part1.py ES/train ES/dev.in ES/dev.p1.out
python3 Part1.py RU/train RU/dev.in RU/dev.p1.out
```
2. Generate scores for the prediction
```
python3 EvalScript/evalResult.py ES/dev.out ES/dev.p1.out
python3 EvalScript/evalResult.py RU/dev.out RU/dev.p1.out
```


### Question 2

To run the code for Q2 and produce a dev.p2.out for both ES and RU, replace the paths to the appropriate ES/RU files with your own.
Take note of the path and ensure that the path is correct, which are lines 85, 86, 183, 184, 186, 203 and 205, according to ES or RU

To evaluate, 
```
python3 EvalScript/evalResult.py ES/dev.out ES/dev.p2.out
python3 EvalScript/evalResult.py RU/dev.out RU/dev.p2.out
```
### Question 3
To run the code for Q3 and produce a dev.p3.out for both ES and RU, replace the paths to the appropriate ES/RU files with your own.
Since the code for Q3 includes some of the functions written for Q2, it is necessary to replace the paths in the codes for both Q2 and Q3.
Specifically, the lines that need to be replaced are:

Lines 85, 86, 183, 184, 186, 203, 205 in Part2.py, and
Lines 127-130, 137, 138, 140 and 142 in Part3.py

To run the evaluation script, simply open up the terminal and type the following:
```
python3 EvalScript/evalResult.py ES/dev.out ES/dev.p3.out
python3 EvalScript/evalResult.py RU/dev.out RU/dev.p3.out
```

### Question 4
To run the code for Q3, replace the paths to the appropriate ES/RU files with your own in the following lines:
Lines 135-142, comment out/uncomment the necessary paths
Lines 152 onwards, comment out/uncomment the necessary paths, and change the inputs accordingly

To run the evaluation script, simply open up the terminal and type the following:
```
python3 EvalScript/evalResult.py ES/dev.out ES/dev.p4.out
python3 EvalScript/evalResult.py RU/dev.out RU/dev.p4.out
```



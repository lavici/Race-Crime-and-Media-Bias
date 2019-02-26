EECS 486 Final Project 
Race, Crime, and Media Bias

This project examines racial bias present in different news outlets. Our dataset consists of 222 articles about crimes committed by people of three ethnicities: Hispanic, White, and Black. 

In order to run our algorithm, simply run run_tests.py. The conditional probabilities of each word, as well as the set difference of words from each ethnicity, is printed to standard out. The current implementation will report the top 20 words for Black perpetrators and the top 20 for White perpetrators, but this number can be changed in the topWordsVennDiagram function.
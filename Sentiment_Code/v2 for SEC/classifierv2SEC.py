import nltk.classify.naivebayes
from nltk import word_tokenize
import re

import random

def sentence_features(sentence):
    num_commas = sentence.count(",")
    if( 0 <=num_commas and num_commas <= 3):
        num_commas = "few"
    else:
        num_commas = "many"
    numbers = False
    for x in sentence:
        if x.isdigit():
            numbers = True
            break
    finance_numbers = numbers and (bool( re.search(r'$',sentence)) or bool(re.search(r'%', sentence))  ) or bool( re.search(r'revenue',sentence)) or bool( re.search(r'sale',sentence))
    change_words = bool(re.search(r'increase',sentence)) or bool(re.search(r'decrease', sentence)) 
    modal_verb = bool(re.search(r'could', sentence)) or bool(re.search(r'may', sentence)) or bool(re.search(r'might', sentence)) 
    
    info = {
        "Commas": num_commas,
        "Numbers": numbers,
        "Change": change_words,
        "Modal": modal_verb, 
        "Fin_Num": finance_numbers
    }
    return info
def load_training_data():
    generic = open("GENERICv2SEC.txt", mode = 'r')
    company = open("COMPANYv2SEC.txt", mode = 'r')
    labeled_sentences = [ (s.strip(), "GENERIC") for s in generic ]
    labeled_sentences += [ (s.strip(), "COMPANY") for s in company]
    random.shuffle(labeled_sentences)
    return labeled_sentences

def with_test_classifier():
    labeled_sentences = load_training_data()
    featuresets = [(sentence_features(n), label) for (n, label) in labeled_sentences]
    train_set, test_set = featuresets[:80], featuresets[80:]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(f"test acc: {nltk.classify.accuracy(classifier, test_set)}")
    errors = []
    for (n,tag) in labeled_sentences:
        guess = classifier.classify(sentence_features(n))
        if guess != tag:
            errors.append( (guess, tag, n) )      
    print(f'Errors: {len(errors)} out of {len(labeled_sentences)}')      
    for (guess, tag, n) in errors:
        print(f'Guess: {guess}, Real Answer: {tag}, Sentence: {n}')
    classifier.show_most_informative_features(10)    
    return classifier

def without_test_classifier():
    labeled_sentences = load_training_data()
    train_set = [(sentence_features(n), label) for (n, label) in labeled_sentences]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    """
    print(nltk.classify.accuracy(classifier, train_set))
    classifier.show_most_informative_features(10) 
    """ 
    return classifier

def test_sentences(sentences):
    classifier = without_test_classifier()
    weight_list = []
    for sentence in sentences:
        label = classifier.classify(sentence_features(sentence))
        def test_sentences(sentences):
    classifier = without_test_classifier()
    weight_list = []
    for sentence in sentences:
        label = classifier.classify(sentence_features(sentence))
        if label == "COMPANY":
            weight_list.append(1)
        else:
            weight_list.append(0)
    return weight_list
    return weight_list

if __name__ == "__main__":
    with_test_classifier()

# Project : Text Keyword Match
# author： guohang
# --------------------------------
import re
from nltk.translate.bleu_score import sentence_bleu
import jieba
import numpy as np




def sent_tokenize(para):

    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


class scoreText(object):
    """
    A class used to score sentences based on the input keyword
    """

    def __init__(self):

        self.sentences = []

    def cleanText(self, sentences):
        """
        Eliminates the duplicates and cleans the text
        """
        try:
            sentences = list(set(sentences))
            mainBody = []
            for i, text in enumerate(sentences):
                # text = re.sub("[-()\"#/@&&^*();:<>{}`+=~|!?,]", "", text)
                text = ''.join(re.findall(r'[\u4e00-\u9fa5]', text))
                mainBody.append(text)
            return mainBody
        except:
            print("Error occured in text clean")

    def preProcessText(self, sentences):
        """
        Tokenization of sentence and lemmatization of words
        """
        try:

            # Tokenize words in a sentence
            # word_tokens = word_tokenize(sentences)
            word_tokens = jieba.lcut(sentences)
            # Lemmatization of words
            stop_words = np.loadtxt(open("stopwords.txt", encoding='utf-8'), dtype=np.str, delimiter=',')
            wordlist = [w for w in word_tokens if not w in stop_words]

            return wordlist
        except:
            print("Error occured in text preprocessing")

    # similarity of subject
    def scoreText(self, keyword, sentences):
        """
        Compares sentences with keyword with bleu scoring technique
        """
        try:

            # Remove symbols from text
            sentences = self.cleanText(sentences)

            # Tokenization and Lennatization of the keyword
            keywordList = self.preProcessText(keyword)
            tmp =[]
            for item in keywordList:
                if " " != item:
                    tmp.append(item)
            keywordList = tmp
            scoredSentencesList = []
            for i in range(len(sentences)):
                # Tokenization and Lennatization of the sentences
                wordlist = self.preProcessText(sentences[i])
                # list of keyword taken as reference
                reference = [keywordList]
                # sentence bleu calculates the score based on 1-gram,2-gram,3-gram-4-gram,
                # and a cumulative of the above is taken as score of the sentence.
                bleu_score_1 = sentence_bleu(reference, wordlist, weights=(1, 0, 0, 0))
                bleu_score_2 = sentence_bleu(reference, wordlist, weights=(0.5, 0.5, 0, 0))
                bleu_score_3 = sentence_bleu(reference, wordlist, weights=(0.33, 0.33, 0.34, 0))
                bleu_score_4 = sentence_bleu(reference, wordlist, weights=(0.25, 0.25, 0.25, 0.25))
                bleu_score = (4 * bleu_score_4 + 3 * bleu_score_3 + 2 * bleu_score_2 + bleu_score_1) / 10
                # append the score with sentence to the list
                scList = [bleu_score, sentences[i]]
                scoredSentencesList.append(scList)
            return scoredSentencesList


        except:
            print("Error occured in score text")

    def sortText(self, scoredText):
        """
        Returns 3 top scored list of sentences
        """
        try:

            scoredTexts = sorted(scoredText, key=lambda x: x[0], reverse=True)
            scoredTexts = [v[1] for i, v in enumerate(scoredTexts) if 0<i<3]
            return scoredTexts
        except:
            print("Error occured in sorting text")


    def sentenceMatch(self, keyword, paragraph):
        """
        Converts paragraph into list and calls scoreText and sortText functions,
        and returns the most matching sentences with the keywords.
        """
        try:

            sentencesList = sent_tokenize(paragraph)
            scoredSentence = self.scoreText(keyword, sentencesList)
            sortedSentence = self.sortText(scoredSentence)
            return sortedSentence
        except:
            print("Error occured in sentence match")

import nltk
import sys
import string
import math
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dictionary = dict()
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            path = os.path.join(directory, file_name)
            with open(path, 'r', encoding='utf8') as file:
                file_dictionary[file_name] = file.read()
    return file_dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    final_token_list = []
    document = document.lower()
    tokenized_list = nltk.tokenize.word_tokenize(document)
    for token in tokenized_list:
        if token not in nltk.corpus.stopwords.words('english'):
            if not all(char in string.punctuation for char in token):
                final_token_list.append(token)
    return final_token_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_counts = dict()
    for file in documents:
        for word in documents[file]:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    word_idfs = dict()
    for word in word_counts:
        word_idfs[word] = math.log(len(documents) / word_counts[word])
    return word_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = dict()
    for name, content in files.items():
        score = 0
        for word in query:
            if word in content:
                idf = idfs[word]
                word_count = content.count(word)
                score += idf * word_count
        scores[name] = score * -1
    scores = [key for key, value in sorted(
        scores.items(),
        key=lambda item: item[1], reverse=True)][:n]
    return scores


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = dict()
    for sentence, words in sentences.items():
        score = 0
        for word in query:
            if word in words:
                score += idfs[word]
        density = 0
        for word in query:
            density += (words.count(word) / len(words))
        scores[sentence] = (score, density)
    scores = [key for key, value in sorted(
        scores.items(),
        key=lambda item: (item[1][0], item[1][1]), reverse=True)][:n]
    return scores


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------
# indexer.py
#
# Class definition for in-memory search index
# -----------------------------------------------------------------------------

import sys
import gzip
import csv
import json
import re
from itertools import chain

# -----------------------------------------------------------------------------
# class definitions
# -----------------------------------------------------------------------------

class WordStats:

  # method: constructor
  def __init__(self):
    # this set contains the line number of the entries
    self.entries = set()

# -----------------------------------------------------------------------------

class Entry:

  # method: constructor
  #
  # @param lineNum {int}
  #   The line number where the entry was encountered
  # @param values {list}
  #   A list containing the attributes of the entry
  #
  def __init__(self, lineNum, values):
    self.lineNum = lineNum
    self.values = values

  # method: toJson
  #
  # Serialize the entry into a JSON object
  #
  # @return A dictionary object for JSON serialization
  #
  def toJson(self):
    return {
      'lineNum': self.lineNum,
      'values': self.values
    }
    
# -----------------------------------------------------------------------------

class Index:

  # method: constructor
  #
  # Builds an index by loading the csv file at the given path
  #
  # @param path {string}
  #   The path to the csv file to load
  #
  def __init__(self, path):

    # the header values
    self.header = None

    # the list of entries, where each entry is a json-serializable dictionary
    self.entries = []
    
    # lookup, keyed by words encountered by the index
    # values are instances of the WordStat class
    self.words = {}

    # build the index
    self.build(path)

  # method: build 
  #
  # builds the list of entries by parsing the given file
  #
  # @param path {string}
  #   Path to the file to build the index from
  #
  def build(self, path):

    with gzip.open(path, 'rt', encoding='utf-8') as gzIn:
      csvReader = csv.reader(gzIn, delimiter=',', quotechar='"')
      lineNum = 0

      # need to support hyphenated quoted words, parenthesized, etc.
      rgx = re.compile('(\w[\w\']*\w|\w)')

      for row in csvReader:

        if not self.header:
          self.header = row
          continue

        entry = Entry(lineNum, row)

        # parse each word out of each entry
        # lowercase for case-insensitive search
        wordChain = chain.from_iterable([rgx.findall(ii.lower()) for ii in row])

        for word in wordChain:

          stats = self.words.get(word, None)

          if not stats:
            stats = WordStats()
            self.words[word] = stats

          # multiple WordStats will reference this entry
          stats.entries.add(lineNum)  

        lineNum += 1

        # pre-convert the entry to JSON, since it is static
        self.entries.append(entry.toJson())

  # method: search
  #
  # Performs a search of the index and returns a list of the results
  #
  # @param terms {list}
  #   A list of terms to search for.  All results will include all terms in the
  #   list.
  # @return {list}
  #   A list of entries, where each entry is an a json-serializable dictionary
  #
  def search(self, terms):
    
    indices = []

    for term in terms:
      term = term.lower()
      stats = self.words.get(term)

      # if any term is not found, then we've found nothing
      if not stats:
        return []

      # if this is the first term, then the results so far are its entries
      if not indices:
        indices = stats.entries

      # otherwise, we need to intersect these entries
      else:
        # TODO: with more time, we could take advantage of the fact that all
        # results are encountered in order by line number and perform a 
        # simpler merge.  For now, we'll use set intersection.
        indices = indices.intersection(stats.entries)

    # de-reference the entries using the list of indices
    return [self.entries[ii] for ii in indices]

# -----------------------------------------------------------------------------
# end indexer.py
# -----------------------------------------------------------------------------


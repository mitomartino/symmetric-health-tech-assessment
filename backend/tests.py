# -----------------------------------------------------------------------------
# tests.py
#
# Unit tests for the in-memory indexer
# -----------------------------------------------------------------------------

import os
import os.path
import unittest
import indexer

# -----------------------------------------------------------------------------
# unit test definition
# -----------------------------------------------------------------------------

class TestIndexer(unittest.TestCase):

  def setUp(self):
    baseDir = os.path.dirname(os.path.realpath(__file__))
    self.index = indexer.Index(baseDir + '/../test_data.csv.gz')

  def tearDown(self):
    pass

  # test the header
  def test_header(self):
    assert ",".join(self.index.header) == 'these,are,the header,values'

  # test empty search:
  # should return no results (an empty list)
  def test_emptySearch(self):
    results = self.index.search([])
    assert len(results) == 0

  # test case-insensitive search
  def test_mixedCase(self):
    results = self.index.search(['mixed', 'case'])
    assert len(results) == 1
    firstRes = results[0]

    results = self.index.search(['MIXED', 'CASE'])
    assert len(results) == 1
    secRes = results[0]

    assert firstRes is secRes

  # test quoted strings
  def test_quoted(self):
    results = self.index.search(['quoted'])
    assert len(results) == 1

  # test embedded commas
  def test_embedded(self):
    results = self.index.search(['embedded', 'comma'])
    assert len(results) == 1

  # test compound terms: should return only entries that match all search terms
  def test_compoundTerms(self):
    results = self.index.search(['tworesults'])
    assert len(results) == 2

    results = self.index.search(['tworesults', 'oneresult'])
    assert len(results) == 1

# -----------------------------------------------------------------------------
# main script
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

# -----------------------------------------------------------------------------
# end tests.py
# -----------------------------------------------------------------------------

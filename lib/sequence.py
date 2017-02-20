# encoding: utf-8
import itertools


def find(sequence, predicate):
    return next(itertools.ifilter(predicate, sequence), None)

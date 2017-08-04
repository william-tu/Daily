# -*- coding: utf-8 -*-
import math

from flask import abort


class Paginate(object):
    def __init__(self, iterable, current_page, per_page):
        if current_page < 1 :
            abort(404)
        self.iterable = iterable
        self.page = current_page
        self.per_page = per_page
        self.total = len(iterable)

        start_index = (self.page - 1) * self.per_page
        end_index = self.page * self.per_page
        self.items = self.iterable[start_index:end_index]
        if not self.items and current_page != 1:
            abort(404)

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages



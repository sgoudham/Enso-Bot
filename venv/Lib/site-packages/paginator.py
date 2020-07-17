"""
Paginator
"""

from math import ceil
from six import string_types
from six.moves import range

class Paginator(object):
    PER_PAGE = 10
    total_pages = 0
    total_items = 0
    callback = None

    def __init__(self, query, page=1, per_page=PER_PAGE, total=None,
                 padding=0, callback=None, static_query=False,
                 left_edge=2, left_current=3, right_current=4, right_edge=2):
        """
        :param query: Iterable to paginate. Can be a query object, list or any iterables
        :param page: current page
        :param per_page: max number of items per page
        :param total: Max number of items. If not provided, it will use the query to count
        :param padding: Number of elements of the next page to show
        :param callback: a function to callback on each item being iterated.
        :param static_query: bool - When True it will return the query as is, without slicing/limit. Usally when using the paginator to just create the pagination.
        # To customize the pagination
        :param left_edge:
        :param left_current:
        :param right_current:
        :param right_edge:
        """

        self.query = query
        self.callback = callback
        self.static_query = static_query
        self.left_edge = left_edge
        self.left_current = left_current
        self.right_edge = right_edge
        self.right_current = right_current

        if not isinstance(per_page, int) or per_page < 1:
            raise TypeError('`per_page` must be a positive integer')
        self.per_page = per_page

        if not total:
            try:
                total = query.count()
            except (TypeError, AttributeError):
                total = len(query)
        self.total_items = total

        if page == "last":
            page == self.total_pages
        elif page == "first":
            page = 1
        self.page = self._sanitize_page_number(page)

        self.padding = padding

    def _sanitize_page_number(self, page):
        if page == 'last':
            return page
        if isinstance(page, string_types) and page.isdigit():
            page = int(page)
        if isinstance(page, int) and (page > 0):
            return page
        return 1

    @property
    def total_pages(self):
        """The total number of pages."""
        return int(ceil(self.total_items / float(self.per_page)))

    @property
    def has_prev(self):
        """True if a previous page exists."""
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.total_pages

    @property
    def next_page_number(self):
        """Number of the next page."""
        return self.page + 1

    @property
    def prev_page_number(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def pages_range(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page - 1
        return start, min(end, self.total_items - 1)

    @property
    def items(self):
        if self.static_query:
            return self.query

        offset = (self.page - 1) * self.per_page
        offset = max(offset - self.padding, 0)
        limit = self.per_page + self.padding
        if self.page > 1:
            limit = limit + self.padding

        if hasattr(self.query, 'limit') and hasattr(self.query, 'offset'):
            return self.query.limit(limit).offset(offset)
        elif isinstance(self.query, list):
            return self.query[offset:offset + limit]
        else:
            return self.query

    def __iter__(self):
        for i in self.items:
            yield self.callback(i) if self.callback else i

    def __len__(self):
        return self.total_pages

    @property
    def pages(self):
        """Iterates over the page numbers in the pagination."""
        return self.iter_pages()

    def iter_pages(self, left_edge=None, left_current=None, right_current=None, right_edge=None):
        left_edge = left_edge or self.left_edge
        left_current = left_current or self.left_current
        right_edge = right_edge or self.right_edge
        right_current = right_current or self.right_current

        last = 0
        for num in range(1, self.total_pages + 1):
            is_active_page = (
                num <= left_edge
                or (
                    (num >= self.page - left_current) and
                    (num < self.page + right_current)
                )
                or (
                    (num > self.total_pages - right_edge)
                )
            )
            if is_active_page:
                if last + 1 != num:
                    yield None
                yield num
                last = num

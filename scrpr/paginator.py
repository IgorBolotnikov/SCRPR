class VirtualPaginator:
    """
    This class is used for making mock pagination of results
    It uses page numbers, acquired from parsing websites and
    uses them to navigate these websites.
    """

    def __init__(self, current_page=1, num_pages=1):
        self.number = current_page
        self.num_pages = num_pages
        self.previous_page_number = self._get_previous_page_number()
        self.has_previous = True if self.number > 1 else False
        self.next_page_number = self._get_next_page_number()
        self.has_next = True if self.number < self.num_pages else False

    def _get_previous_page_number(self):
        if self.number > self.num_pages:
            return self.num_pages - 1
        return self.number - 1

    def _get_next_page_number(self):
        if self.number > self.num_pages:
            return self.num_pages
        return self.number + 1

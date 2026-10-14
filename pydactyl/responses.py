"""Classes used for creating responses."""
import inspect


class _ResponseBase(object):
    """Shared accessors for objects holding a page of API results.

    Subclasses must set ``data`` and ``meta`` attributes.
    """

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        if hasattr(self, item):
            return getattr(self, item, None)
        raise KeyError(item)

    def __str__(self):
        return '{}'.format(self.data)

    def get(self, key, default=None):
        """Retrieves a key from the response.

        Returns:
            Value for the specified key
        """
        return getattr(self, key, default)

    def get_next_page_link(self):
        """Get a link to the next page.

        Returns:
            str: Link provided by API
        """
        return self.meta['pagination']['links'].get('next')

    def get_previous_page_link(self):
        """Get a link to the previous page.

        Returns:
            str: Link provided by API
        """
        return self.meta['pagination']['links'].get('previous')


class Page(_ResponseBase):
    """A single page of results from a paginated API response.

    Iterating over a Page yields the individual items on that page.
    """

    def __init__(self, data, meta, number):
        self.data = data
        self.meta = meta
        self.number = number

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return '<Page {} ({} items)>'.format(self.number, len(self.data))


class PaginatedResponse(_ResponseBase):
    """An iterable API response that returns paginated results.

    Iterating over a PaginatedResponse (with ``for`` or ``async for``) yields
    a new :class:`Page` for each page of results, fetching subsequent pages
    from the API as required.  Each iteration starts again from the first
    page, so a response may be iterated over any number of times.

    ``data`` and ``meta`` always refer to the first page of results.
    """

    def __init__(self, client, endpoint, data):
        self._client = client
        self.data = data['data']
        self.endpoint = endpoint
        self.meta = data['meta']

    def __iter__(self):
        """Iterate over all pages of results.

        Yields:
            Page: Each page of results, starting with the first.

        Raises:
            PterodactylApiError: If an API request fails
        """
        page = Page(self.data, self.meta, 1)
        yield page
        while self._next_page_exists(page.meta):
            number = page.number + 1
            response = self._client._api_request(
                endpoint=self.endpoint, params={'page': number})
            page = Page(response['data'], response['meta'], number)
            yield page

    async def __aiter__(self):
        """Iterate over all pages of results asynchronously.

        Yields:
            Page: Each page of results, starting with the first.

        Raises:
            PterodactylApiError: If an API request fails
        """
        page = Page(self.data, self.meta, 1)
        yield page
        while self._next_page_exists(page.meta):
            number = page.number + 1
            response = self._client._api_request(
                endpoint=self.endpoint, params={'page': number})
            if inspect.isawaitable(response):
                response = await response
            page = Page(response['data'], response['meta'], number)
            yield page

    def __len__(self):
        return self.meta['pagination']['total']

    def collect(self):
        """Collect all results from all pages.

        Returns:
            list: Combined responses from all pages
        """
        return [item for page in self for item in page]

    async def collect_async(self):
        """Collect all results from all pages asynchronously.

        Returns:
            list: Combined responses from all pages
        """
        collected = []
        async for page in self:
            collected.extend(page.data)
        return collected

    @staticmethod
    def _next_page_exists(data):
        """Determine if the response contains a valid link to the next page.

        Returns:
            bool: True if next page exists.
        """
        exists = ('pagination' in data
                  and 'links' in data['pagination']
                  and 'next' in data['pagination']['links']
                  and data['pagination']['links']['next'] != '')
        return exists

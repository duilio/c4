from c4.book import Book, WIN, DRAW
from c4.evaluate import INF


class BookEngineMixin(object):
    def __init__(self, *args, **kwargs):
        filename = kwargs.pop('book_filename', 'book.data')
        self._book = Book(filename)
        super(BookEngineMixin, self).__init__(*args, **kwargs)

    def search(self, board, depth, ply=1, alpha=-INF, beta=INF):
        if ply > 1 and self._book[board] is not None:
            result = self._book[board]
            if result == WIN:
                return [], INF
            elif result == DRAW:
                return [], DRAW
            else:
                return [], -INF

        return super(BookEngineMixin, self).search(board, depth,
                                                   ply, alpha,
                                                   beta)

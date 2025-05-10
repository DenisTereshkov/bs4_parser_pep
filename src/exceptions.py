class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class VersionListNotFoundError(Exception):
    """Ошибка, возникающая, когда список с версиями Python не найден."""
    def __init__(self, message="Не найден список с версиями Python"):
        self.message = message
        super().__init__(self.message)


class PageLoadError(Exception):
    """Исключение, возникающее при ошибках загрузки страницы."""
    def __init__(self, url, message="Возникла ошибка при загрузке страницы"):
        self.url = url
        self.message = message
        super().__init__(f"{self.message}: {self.url}")

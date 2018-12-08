from datetime import datetime


class DateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        date = datetime.strptime(value, "%Y-%m-%d").date()
        return date

    def to_url(self, date):
        return date.strftime("%Y-%m-%d")

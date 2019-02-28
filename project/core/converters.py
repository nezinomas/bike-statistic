from datetime import datetime


class DateConverter:
    regex = '(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'

    def to_python(self, value):
        # date = datetime.strptime(value, "%Y-%m-%d").date()
        # return date
        return value

    def to_url(self, date):
        return date

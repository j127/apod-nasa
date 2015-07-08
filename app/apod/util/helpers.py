from datetime import datetime, date
import re


def pic2data(pic_data):
    print(pic_data)
    data = {}
    data['title'] = pic_data['title']
    data['media_url'] = pic_data['url']
    data['media_type'] = pic_data['media_type']
    data['explanation'] = pic_data['explanation']
    return data

class VulcanDateSlicer(object):
    """Takes a date in any of several formats, and gives it methods to return different formats.

    >>> d = VulcanDateSlicer('150707')
    >>> d.as_date()
    datetime.date(15, 7, 7)
    >>> d.as_6_digit_string()
    '150707'
    >>> d.as_6_digit_string(dashed=True)
    '15-07-07'
    >>> d2 = VulcanDateSlicer('13-10-01')
    >>> d2.as_8_digit_string()
    '20131001'
    >>> d3 = VulcanDateSlicer(datetime.date(14, 12, 8))
    >>> d3.as_8_digit_string(dashed=True)
    '2014-12-08'
    """

    def __init__(self, input):
        """Sets the self.date_str and self.current_date."""
        # TODO: fix this
        if type(input) == str:
            # Extracts the digits
            self.date_str = re.match(r'(\d{2,4}-?\d{2}-?\d{2})', input)
            if len(self.date_str) == 6:
                # e.g., '151207'
                # Add prefixes
                if int(self.date_str[:2]) > 60:
                    # It's 20th Century
                    self.date_str = '19{}'.format(self.date_str)
                else:
                    # It's 21st Century
                    self.date_str = '20{}'.format(self.date_str)
            self.current_date = date(self.date_str)
        else:
            # Make sure that it's date() not datetime()
            self.current_date = date(input)
            # self.date_str =

    def __repr__(self):
        return 'A date: {}'.format(self.date_str)

    def _chunk_it(self):
        """Splits up the self.date_str into 2-digit chunks in a list.

        Only used internally in the class.
        """
        return [int(self.date_str[i:i + 2]) for i in range(0, len(self.date_str), 2)]

    def as_date(self):
        """Returns the input as a datetime.date()."""
        return self.current_date

    def as_6_digit_string(self, dashed=False):
        """Returns the input like '151201' or '15-12-01'."""
        if dashed is True:
            return self._chunk_it()[1:].join('-')
        else:
            return self.date_str[2:]

    def as_8_digit_string(self, dashed=False):
        """Returns the input like '20151201' or '2015-12-01'."""
        if dashed is True:
            chunks = self._chunk_it()
            # TODO: make sure that the .pop(0) doesn't modify the list... or find alternate way.
            first_item = '{}{}'.format(chunks.pop(0), chunks.pop(1))
            output = [first_item, chunks[1], chunks[2]].join('-')
            return output
        else:
            return self.date_str

    def as_6_digit_list(self):
        """Returns the input like ['15', '12, '01']."""
        return self._chunk_it()[1:]

    def as_8_digit_list(self):
        """Returns the input like ['2015', '12, '01']."""
        chunks = self._chunk_it()
        first_item = '{}{}'.format(chunks.pop(0), chunks.pop(1))
        output = [first_item, chunks[1], chunks[2]]
        return output


def convert_date_format(digits,output_format='list',four_digit_year=True):
    """Takes a list or string and returns a list, string, or date.

    >>> convert_date_format('010101')
    ['2001', '01', '01']
    """
    if type(digits) == list:
        year, month, day = list
    else:
        year, month, day = [digits[i:i + 2] for i in range(0, len(digits), 2)]
    
    if four_digit_year == True:
        year = add_year_prefix(year)
    
    if output_format == 'list':
        return [year,month,day]
    elif output_format == 'date':
        return datetime(int(year),int(month),int(day))
    elif output_format == 'string':
        return '{}{}{}'.format(year,month,day)

def add_year_prefix(year):
    if int(year) > 40:
        year = '19' + str(year).zfill(2)
    else:
        year = '20' + str(year).zfill(2)

    return year

if __name__ == '__main__':
    import doctest
    doctest.testmod()
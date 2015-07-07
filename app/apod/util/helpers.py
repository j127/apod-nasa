from datetime import datetime


def pic2data(pic_data):
    print(pic_data)
    data = {}
    data['title'] = pic_data['title']
    data['media_url'] = pic_data['url']
    data['media_type'] = pic_data['media_type']
    data['explanation'] = pic_data['explanation']
    return data

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
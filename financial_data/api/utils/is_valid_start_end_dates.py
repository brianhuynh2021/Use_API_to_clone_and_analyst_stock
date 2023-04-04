from datetime import datetime

def valid_date(date:str):
    # Check if the dates are in the correct format
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    # Check if start_date is less than or equal to end_date
    return True

def valid_start_end_date(start_date=None, end_date=None):
    start_date = valid_date(start_date)
    end_date = valid_date(end_date)
    if start_date > end_date:
        return False
    else:
        return True
    
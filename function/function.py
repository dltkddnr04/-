import datetime

# 내부적으로 필요한 함수이기는 한데 별도 파일로 분리하기에는 애매한 function들을 모아놓은 파일이다.

def timezone_shift(date, original_zone, convert_zone):
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    shift = convert_zone - original_zone

    if original_zone == convert_zone:
        return date
    else:
        if shift > 0:
            date = date + datetime.timedelta(hours=shift)
        else:
            date = date - datetime.timedelta(hours=shift)

        date = date.strftime('%Y-%m-%dT%H:%M:%S')
        return date
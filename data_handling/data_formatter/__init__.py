import logging as log
import data_formatter

def formatData(data):
    '''
    format Data for DB
    - delete unnecessary data
    - delete empty data
    @Params
    --------
    data: dict; data, before removal
    '''
    _dict = data.copy()

    # formatData for all elements (_dict is list)
    if(type(_dict) is list):
        for i in range(0, len(_dict)):
            if type(_dict[i]) is dict or type(_dict[i]) is list:
                _dict[i] = formatData(_dict[i])

        return _dict

    # formatData for all elements (_dict is dict)
    subs = [key for key in _dict if type(_dict[key]) is dict or type(_dict[key]) is list]
    for sub in subs:
        _dict[sub] = formatData(_dict[sub])


    # remove *_urls
    rems = [key for key in _dict if key.endswith('_url') or key == 'url' or key == '_links']
    for rem in rems:
        log.debug(f'remove *_url: {rem}')
        del _dict[rem]

    # remove empty elements
    rems = [key for key in _dict if (type(_dict[key]) == list or type(_dict[key]) == dict) and not _dict[key]]
    for rem in rems:
        log.debug(f'remove empty element: {rem}')
        del _dict[rem]

    return _dict
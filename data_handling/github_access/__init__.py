import github_access.access as access

def getMostForkedProjects(amount, offset):
    amount += offset
    mock = []
    for i in range(offset, amount):
        mock.append(i)
    return mock


def getData(id): 
    mock = access.get_all_requests_from_repo(id)
    return mock


import github_access.access as access

def getRepoWithMostStars(amount, minStars):
    return access.getMostStarredRepos(amount=amount, minStars=minStars)



def getData(id): 
    mock = access.get_all_requests_from_repo(id)
    return mock


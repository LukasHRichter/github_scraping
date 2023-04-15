# #all must be 1:
#     'license': 1, #ja
#     'community/profile': 1, #ja
#     'stats/code_frequency': 1, #ja
#     'stats/commit_activity': 1, #ja not comprehensive; sieht man für 1 Jahr zurückgehend wsl
#     'stats/contributors': 1, #ja 
#     'stats/participation': 1, #ja
#     'stats/punch_card': 1, #ja geht eine Woche zurück
#     'import/authors': 1, #nein
#     'import/large_files': 1, #nein
#     'languages': 1, #ja
#     'readme': 1, #ja
#     'releases/latest': 1, #nein, steht schon in releases
#     'actions/cache/usage': 1, #nein
#     'topics': 1, #ja
#     'notifications': 1, #nein
#     'environments': 1, #ja
#     'projects': 1, #ja, mit vorbehalt
#     'actions/workflows': 1, #ja
#     'contents': 1, #ja
#     'contents/$path': 1, #nein
# #all must be 0:
#     'stargazers': 1, #nein  #In order to keep the API fast for everyone, pagination is limited for this resource
#     'subscribers': 0, #nein
#     'deployments': 0, #? wie sehr wird das genutzt? nur von 2016
#     'assignees': 0, #nein, liste von personen
#     'issues/comments': 1, #nein erstmal #422 response,. wenn keine 400 response höre auf zu scrapen #interessant besser anders lösen über issues #In order to keep the API fast for everyone, pagination is limited for this resource
#     'issues/events': 1, #? siehe issues/comments "message": "In order to keep the API fast for everyone, pagination is limited for this resource. Check the rel=last link relation in the Link response header to see how far back you can traverse.",
#     'labels': 0, #ja
#     'milestones': 0, #ja
#     # 'pulls/comments': 0, #nein #502 #server error
#     'contributors': 0, #ja #liste von contributors mit liste von anzahl an contributions
#     'forks': 0, #erstmal nein
#     'tags': 0, #nein
#     # 'pulls': 0, #ja #funktioniert manchmal mit bad gateway #server error
#     'issues': 0, #ja
#     'branches': 0, #ja
#     'branches/$name': 0, #nein -->erst in Version 2
#     'commits': 0, #ja
#     'comments': 0, #ja
#     'issues/$number': 0, #nein #erstmal nicht, case study ob relevant
#     'issues/$number/comments': 0,# nein erstmal nicht, nachträglich
#     'issues/$number/events': 0, #nein
#     'issues/$number/labels': 0, #nein, daten haben wir schon
#     'issues/$number/timeline': 0, #erstmal raus--> version 2
#     'issues/$number/reactions': 0, #nein, würde im issue direkt drin stehen
#     # 'pulls/$number': 0, #nein
#     # 'pulls/$number/commits': 0, #nein
#     # 'pulls/$number/files': 0, #nein
#     # 'pulls/$number/comments': 0, #! ja, aber viel zu aufwendig zu holen, also nein
#     # 'pulls/$number/requested_reviewers': 0, #schon in pulls drin
#     # 'pulls/$number/reviews': 0, #! ja, aber viel zu aufwendig zu holen, also nein
#     'releases': 0, #ja  #Only the first 10000 results are available oder []???
#     'releases/$id/assets': 1, #nein
#     'deployments/$id': 0, #nein
#     'deployments/$id/statuses': 0, #nein
#     'milestones/$number': 0, #nein haben wir schon
#     'milestones/$number/labels': 0, #nein habne wir schon
#     'comments/$id': 0, #nein, habne wir schon
#     'comments/$id/reactions': 0, #nein, haben wir schon
#     'releases/$id': 1, #nein
#     'releases/$id/reactions': 1, #nein
# #notfound:
#     'subscription': 1, #nein
#     'keys': 1, #nein
#     'git/tags': 1, #nein
#     'import': 1, #nein
#     'pages': 1, #(=Doku) nein ((((vielleicht))))
#     'pages/builds': 1, #nein
#     'pages/builds/latest': 1, #nein
#     'pages/health': 1, #nein
#     'codeowners/errors': 1, #nein
#     'dispatches': 1, #nein
#     'teams': 1, #nein
#     'vulnerability-alerts': 1, #nein
#     'autolinks': 1, #nein
#     'tags/protection': 1, #nein
#     'hooks': 1, #nein
#     'branches/$name/protection': 0, #! könnte interessant sein, kommen wir da ran?
#     'branches/$name/protection/enforce_admins': 0, #nein
#     'branches/$name/protection/required_pull_request_reviews': 0, #nein
#     'branches/$name/protection/required_signatures': 0, #nein
#     'branches/$name/protection/required_status_checks': 0, #nein
#     'branches/$name/protection/required_status_checks/contexts': 0, #nein
#     'branches/$name/protection/restrictions': 0, #nein
#     'branches/$name/protection/restrictions/apps': 0, #nein
#     'branches/$name/protection/restrictions/teams': 0, #nein
#     'branches/$name/protection/restrictions/users': 0, #nein

# #kann bei 0 nichtb getestet werden zu viele abfragen
#     # 'actions/artifacts': 1, #? könnte interessant sein

# #server error: und KeyError: 'actions':
#     # 'actions/runs': 1, #? könnte interessant sein
#     # 'actions/runs/$id/jobs': 1, #? könnte interessant sein
#     # 'actions/runs/$id/approvals': 1, #? könnte interessant sein
#     # 'actions/runs/$id/pending_deployments': 1, #? könnte interessant sein
#     # 'actions/runs/$id/timing': 1, #? könnte interessant sein
#     # 'actions/runs/$id/attempts': 1, #? könnte interessant sein
#     # 'actions/runs/$id/attempts/$number': 1, #? könnte interessant sein
#     # 'actions/runs/$id/attempts/$number/jobs': 1, #? könnte interessant sein
#     # 'actions/workflows/$id': 1, #? könnte interessant sein
#     # 'actions/workflows/$id/runs': 1, #? könnte interessant sein
#     # 'actions/workflows/$id/timing': 1, #? könnte interessant sein

# #Funktionieren nicht:
#     # 'issues/comments/$id': 1, #nein
#     # 'issues/comments/$id/reactions': 1, #nein
#     # 'pulls/comments/$id/reactions': 1, #nein
#     # 'events': 0, #? pagination besiegen? erstmal raus #könnte interessant sein

# #TypeError: string indices must be integers
#     # 'environments/$name': 1, #nein
#     # 'environments/$name/deployment-branch-policies': 1, #nein
#     # 'hooks/$id/config': 1, #nein
#     # 'hooks/$id/deliveries': 1, #nein
# }

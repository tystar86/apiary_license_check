import requests, json, requests_cache, base64, re
from requests.auth import HTTPBasicAuth
from datetime import datetime

f = ''
     global f
    requests_cache.install_cache('github_cache', backend='sqlite', expire_after=60)

    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    pattern = 'license_check_' + datestring + '.txt'
    f = open(pattern, 'w')

    token = get_token()
    list_all_repos = all_repositories(token)
    repos_without_license = []
    list_without_licence = []
    print(list_all_repos)


    for every_repo in list_all_repos:
        print('REPO: ', every_repo)
        contents_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/contents', token)
        fetch_license_file = False
        fetch_license = False
        for filename in contents_url:
            if re_findall(filename['name']) or filename['name'] == 'README.md' or filename['name'] == 'package.json':
                v = search_license(filename, token)
                print(filename['name'], ': ', v)
                if v:
                    fetch_license = True

            if filename['name'] == 'package.json':
                dep = dependencies_listing(filename, token)
                parsed_dependencies = json.loads(dep)
                for name_dep in parsed_dependencies:
                    if name_dep == 'dependencies' or name_dep == 'devDependencies':
                        print(name_dep, ': ')
                        list_dependencies = []
                        for name, version in parsed_dependencies[name_dep].items():
                            d = check_dependencies_license(name, version)
                            list_dependencies.append((name, version, d))
                        for s in list_dependencies:
                            print(s)
            if re_findall(filename['name']):
                fetch_license_file = True
        if not fetch_license_file:
            repos_without_license.append(every_repo)
        if not fetch_license:
            list_without_licence.append(every_repo)


        pulls_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/pulls', token)
        if pulls_url != []:
            for g in pulls_url:
                sha = g['base']['sha']
                print('pull: ', sha)
                trees_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/git/trees/' + sha,
                                         token)

        print('---------------------------------------')
    print('Repositories total: {}'.format(len(list_all_repos)))
    print('Repos without license file: {}'.format(len(repos_without_license)),': ', repos_without_license)
    print('Repos without license: {}'.format(len(list_without_licence)), ':', list_without_licence)


def all_repositories(token):
    list_all_repos = []
    all_repos_url = json_parsing('https://api.github.com/users/apiaryio/repos', token)
    for repo in all_repos_url:
        list_all_repos.append(repo['name'])
    return list_all_repos


def get_token():
    with open('auth_key.txt', encoding='utf-8') as file:
        token = file.read()
        return token


def json_parsing(url, token):
    content = requests.get(url, auth=HTTPBasicAuth('', token))  # headers={'Authorization' : 'token' + token}
    if content.status_code != 200:
        print(content.status_code)
    else:
        parsed_text = content.text
        return json.loads(parsed_text)


def re_findall(text):
    s = re.findall(r'\blicen[sc]es?d?', text, re.I)
    for x in s:
        return x


def base64_decoding(content):
    decoded = base64.b64decode(content)
    text = decoded.decode()
    return text


def search_license(file, token):
    parsed_text = json_parsing(file['url'], token)
    decoded_text = base64_decoding(parsed_text['content'])
    if re.search(r'\blicen[sc]es?d?', decoded_text, re.I):
        if re.search(r'\bmit', decoded_text, re.I):
            text = 'MIT'
        elif re.search(r'\bbsd', decoded_text, re.I):
            text = 'BSD'
        else:
            # print('README: ', decoded_readme)
            text = 'Other'
        return text


def dependencies_listing(file, token):
    parsed_text = json_parsing(file['url'], token)
    decoded_text = base64_decoding(parsed_text['content'])
    return decoded_text


def check_dependencies_license(name, version):
    url = requests.get('https://registry.npmjs.org/' + name + '/' + version)
    if url.status_code != 200:
        print(url.status_code, name, version)
    else:
        for a, b in url.json().items():
            dependencies_license = re.findall(r'\blicen[sc]ed?s?', a, re.I)
            for x in dependencies_license:
                if a == x:
                    return b


if __name__ == '__main__':
    main()
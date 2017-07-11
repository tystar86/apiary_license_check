import requests, json, requests_cache, base64, re, difflib, sys, argparse
from requests.auth import HTTPBasicAuth
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Apiary License Check")
    parser.add_argument("filename", help="Enter a file to compare.", nargs="?")
    args = parser.parse_args()
    f = create_file()
    license_check(f)

    if args.filename:
        compare_files(f.name, args.filename)

def license_check(f):
    requests_cache.install_cache('github_cache', backend='sqlite', expire_after=3600000)
    token = get_token()
    list_all_repos = all_repositories(token, f)
    list_repos_without_license_file = []
    list_without_licence = []

    for every_repo in list_all_repos:
        print('REPO: ', every_repo, file=f)
        contents_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/contents', token, f)
        list_licenses_compare = []
        found_license_file = False
        found_license = False
        for filename in contents_url:
            if re_findall(filename['name'], r'\blicen[sc]e[sd]?'):
                found_license_file = True
                r = search_license_type_in_license_file(filename, token, f)
                list_licenses_compare.append((filename['name'], r))
                print(filename['name'], ': ', r, file=f)
                if r:
                    found_license = True

            if re_findall(filename['name'], r'\breadme') or filename['name'] == 'package.json':
                v = search_license_type_in_readme_packagejson(filename, token, f)
                list_licenses_compare.append((filename['name'], v))
                print(filename['name'], ': ', v, file=f)
                if v:
                    found_license = True

            package_json_dependencies(every_repo, f, filename, token)

        if not found_license_file:
            list_repos_without_license_file.append(every_repo)
        if not found_license:
            list_without_licence.append(every_repo)

        compare_pull_requests_and_master(every_repo, f, list_licenses_compare, token)

        print('---------------------------------------', file=f)
    print()
    print('REPOSITORIES TOTAL: {}'.format(len(list_all_repos)))
    print('REPOSITORIES TOTAL: {}'.format(len(list_all_repos)), file=f)
    print()
    print('REPOSITORIES WITHOUT LICENSE FILE: {}'.format(len(list_repos_without_license_file)), ':', list_repos_without_license_file)
    print('REPOSITORIES WITHOUT LICENSE FILE: {}'.format(len(list_repos_without_license_file)), ':', list_repos_without_license_file, file=f)
    print()
    print('REPOSITORIES WITHOUT LICENSE: {}'.format(len(list_without_licence)), ':', list_without_licence)
    print('REPOSITORIES WITHOUT LICENSE: {}'.format(len(list_without_licence)), ':', list_without_licence, file=f)
    print()
    f.close()


def create_file():
    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    pattern = 'license_check_' + datestring + '.txt'
    return open(pattern, 'w')


def all_repositories(token, f):
    repos_sum_url = json_parsing('https://api.github.com/users/apiaryio', token, f)
    repos_sum = repos_sum_url['public_repos']
    list_all_repos = []
    for number in range(1, repos_sum//30 + 2):
        all_repos_url = json_parsing('https://api.github.com/users/apiaryio/repos?page= {}'.format(number), token, f)
        for repo in all_repos_url:
            list_all_repos.append(repo['name'])
    return list_all_repos


def get_token():
    with open('auth_key.txt', encoding='utf-8') as file:
        token = file.read()
        return token


def json_parsing(url, token, f):
    content = requests.get(url, auth=HTTPBasicAuth('', token))
    if content.status_code != 200:
        print(content.status_code)
        print(content.status_code, file=f)
    else:
        parsed_text = content.text
        return json.loads(parsed_text)


def re_findall(text, pattern):
    s = re.findall(pattern, text, re.I)
    for x in s:
        return x


def base64_decoding(content):
    decoded = base64.b64decode(content)
    text = decoded.decode()
    return text


def search_license_type_in_readme_packagejson(file, token, f):
    parsed_text = json_parsing(file['url'], token, f)
    decoded_text = base64_decoding(parsed_text['content'])
    if re.search(r'\blicen[sc]e[sd]?', decoded_text, re.I):
        return license_type(decoded_text)


def search_license_type_in_license_file(file, token, f):
    parsed_text = json_parsing(file['url'], token, f)
    decoded_text = base64_decoding(parsed_text['content'])
    return license_type(decoded_text)


def license_type(text):
    if re.search(r'\bmit\b', text, re.I):
        license = 'MIT'
    elif re.search(r'\bbsd\b', text, re.I):
        license = 'BSD'
    elif re.search(r'\bisc\b', text, re.I):
        license = 'ISC'
    else:
        license = 'Other'
    return license


def dependencies_listing(file, token, f):
    '''{
  "name": "package.json",
  "url": "https://api.github.com/repos/apiaryio/Amanda/contents/package.json?ref=master",
  "type": "file",
  "content": "ewoKICAibmFtZSI6ICJhbWFuZGEiLAogICJkZXNjcmlwdGlvbiI6ICJKU09O\nIFNjaGVtYSB2YWxpZGF0b3IiLAogICJ2ZXJzaW9uIjogIjAuNS4xIiwKICAi\nYXV0aG9yIjogIkZyYW50acWhZWsgSMOhYmEgPGZyYW50aXNla0BhcGlhcnku\naW8+IChodHRwczovL2dpdGh1Yi5jb20vQmFnZ3opIiwKICAiY29udHJpYnV0\nb3JzIjogWwogICAgewogICAgICAgICJuYW1lIjogIlBldGVyIEdyaWxsaSIs\nCiAgICAgICAgImVtYWlsIjogInR1bGx5QGFwaWFyeS5pbyIKICAgIH0KICBd\nLAogICJkZXZEZXBlbmRlbmNpZXMiOiB7CiAgICAibW9jaGEiOiAiMS4xMi4w\nIiwKICAgICJleHBlY3QuanMiOiAiMC4yLjAiLAogICAgImRlYnVnIjogIjAu\nNy4yIiwKICAgICJhc3luYyI6ICIwLjIuOSIsCiAgICAidWdsaWZ5LWpzIjog\nIjIuMy42IgogIH0sCgogICJrZXl3b3JkcyI6IFsKICAgICJKU09OIiwKICAg\nICJKU09OIFNjaGVtYSIsCiAgICAic2NoZW1hIiwKICAgICJ2YWxpZGF0b3Ii\nLAogICAgInZhbGlkYXRlIiwKICAgICJKU09OIHZhbGlkYXRvciIsCiAgICAi\nc2NoZW1hIHZhbGlkYXRvciIsCiAgICAiYXN5bmMiLAogICAgImJyb3dzZXIi\nCiAgXSwKCiAgImhvbWVwYWdlIjogImh0dHBzOi8vZ2l0aHViLmNvbS9hcGlh\ncnlpby9BbWFuZGEiLAoKICAicmVwb3NpdG9yeSI6IHsKICAgICJ0eXBlIjog\nImdpdCIsCiAgICAidXJsIjogImdpdDovL2dpdGh1Yi5jb20vYXBpYXJ5aW8v\nQW1hbmRhLmdpdCIKICB9LAoKICAibWFpbiI6ICIuL3JlbGVhc2VzL2xhdGVz\ndC9hbWFuZGEuanMiLAoKICAiZW5naW5lcyI6IHsKICAgICJub2RlIjogIj49\nIDAuNi4wIgogIH0sCgogICJidWdzIjogewogICAgInVybCI6ICJodHRwczov\nL2dpdGh1Yi5jb20vYXBpYXJ5aW8vQW1hbmRhL2lzc3VlcyIsCiAgICAiZW1h\naWwiOiAiaGVsbG9AZnJhbnRpc2VraGFiYS5jb20iCiAgfSwKCiAgImxpY2Vu\nc2VzIjogWwogICAgewogICAgICAidHlwZSI6ICJNSVQiLAogICAgICAidXJs\nIjogImh0dHBzOi8vZ2l0aHViLmNvbS9hcGlhcnlpby9BbWFuZGEvYmxvYi9t\nYXN0ZXIvUkVBRE1FLm1kIgogICAgfQogIF0sCgogICJzY3JpcHRzIjogewog\nICAgInRlc3QiIDogIm1vY2hhIC0tdWkgdGRkIC0tcmVwb3J0ZXIgc3BlYyAu\nL3Rlc3RzL2pzb24vYXR0cmlidXRlcy9yZXF1aXJlZC8qLmpzIC4vdGVzdHMv\nanNvbi9hdHRyaWJ1dGVzL2Zvcm1hdC8qLmpzIC4vdGVzdHMvanNvbi9hdHRy\naWJ1dGVzL3R5cGUvKi5qcyAuL3Rlc3RzL2pzb24vYXR0cmlidXRlcy8qLmpz\nIC4vdGVzdHMvanNvbi8qLmpzIgogIH0KCn0K\n",
  "encoding": "base64",

  }'''
    parsed_text = json_parsing(file['url'], token, f) #
    decoded_text = base64_decoding(parsed_text['content'])
    return decoded_text


def package_json_dependencies(every_repo, f, filename, token):
    ''' filename:
    {
    "name": "LICENSE",
    "path": "LICENSE",
    "size": 1105,
    "url": "https://api.github.com/repos/apiaryio/Amanda/contents/LICENSE?ref=master",
    }
    '''
    if filename['name'] == 'package.json':
        dep = dependencies_listing(filename, token, f)
        parsed_dependencies = json.loads(dep)
        for name_dep in parsed_dependencies:
            if name_dep == 'dependencies' or name_dep == 'devDependencies':
                list_dependencies = []
                for name, version in parsed_dependencies[name_dep].items():
                    d = check_dependencies_license(every_repo, name, f)
                    list_dependencies.append((name, d))
                if list_dependencies != []:
                    print(name_dep, ': ', file=f, flush=True)
                for s in list_dependencies:
                    print(s, file=f)


def check_dependencies_license(repo, name, f):
    url = requests.get('https://registry.npmjs.org/' + name)
    if url.status_code != 200:
        print(url.status_code, 'DEPENDENCIES: repo: ', repo, ', name: ', name)
        print(url.status_code, 'DEPENDENCIES: repo: ', repo, ', name: ', name, file=f)
    else:
        for a, b in url.json().items():
            dependencies_license = re.findall(r'\blicen[sc]e[sd]?', a, re.I)
            for x in dependencies_license:
                if a == x:
                    return b


def pull_requests_search_licence_type(repo, sha, token, f):
    list_tree = []
    trees_url = json_parsing('https://api.github.com/repos/apiaryio/' + repo + '/git/trees/' + sha, token, f)
    for l in trees_url['tree']:
        if re_findall(l['path'], r'\blicen[sc]e[sd]?'):
            r = search_license_type_in_license_file(l, token, f)
            list_tree.append((l['path'], r))
        if re_findall(l['path'], r'\breadme') or l['path'] == 'package.json':
            v = search_license_type_in_readme_packagejson(l, token, f)
            list_tree.append((l['path'], v))
    return list_tree


def compare_pull_requests_and_master(every_repo, f, list_licenses, token):
    pull_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/pulls', token, f)
    if pull_url != []:
        for g in pull_url:
            pull_licenses = pull_requests_search_licence_type(every_repo, g['head']['sha'], token, f)
            if list_licenses != pull_licenses:
                print('PULLS:', file=f)
                print('master: ', list_licenses, 'head: ', pull_licenses, file=f)


def compare_files(new_file, old_file):
    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    pattern = 'compare_files_' + datestring + '.txt'
    f_02 = open(pattern, 'w')
    with open(old_file, 'r') as f1, open(new_file, 'r') as f2:
        diff = difflib.ndiff(f1.readlines(), f2.readlines())
        f_02.write('Old file: {}, New file: {} \n'.format(f1.name, f2.name))
        for i, line in enumerate(diff):
            if line.startswith(' '):
                continue
            sys.stdout.write('Line: {}, Text: {}'.format(i, line))
            f_02.write('Line: {}, Text: {}'.format(i, line))
    f_02.close()


if __name__ == '__main__':
    main()
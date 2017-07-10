import requests, json, requests_cache, base64, re, difflib, sys, argparse
from requests.auth import HTTPBasicAuth
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Apiary License Check")
    parser.add_argument("filename",
                        help="Enter a file to compare.",
                        nargs="?")
    args = parser.parse_args()
    f = create_file()
    license_check(f)
    if args.filename:
        compare_files(f.name, args.filename)

def license_check(f):
    requests_cache.install_cache('github_cache', backend='sqlite', expire_after=3600000)
    token = get_token()
    list_all_repos = all_repositories(token, f)
    repos_without_license = []
    list_without_licence = []
    for every_repo in list_all_repos:
        print('REPO: ', every_repo, file=f)
        contents_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/contents', token, f)
        list_licenses = []
        find_license_file = False
        find_license = False
        for filename in contents_url:
            if re_findall(filename['name'], r'\blicen[sc]es?d?'):
                r = search_license_type_in_license_file(filename, token, f)
                list_licenses.append((filename['name'], r))
                print(filename['name'], ': ', r, file=f)
                if r:
                    find_license = True

            if re_findall(filename['name'], r'\breadme') or filename['name'] == 'package.json':
                v = search_license_type_in_readme_packagejson(filename, token, f)
                list_licenses.append((filename['name'], v))
                print(filename['name'], ': ', v, file=f)
                if v:
                    find_license = True

            if re_findall(filename['name'], r'\blicen[sc]es?d?'):
                find_license_file = True

            package_json_dependencies(every_repo, f, filename, token)

        if not find_license_file:
            repos_without_license.append(every_repo)
        if not find_license:
            list_without_licence.append(every_repo)

        process_pull_requests(every_repo, f, list_licenses, token)

        print('---------------------------------------', file=f)
    print()
    print('REPOSITORIES TOTAL: {}'.format(len(list_all_repos)))
    print('REPOSITORIES TOTAL: {}'.format(len(list_all_repos)), file=f)
    print()
    print('REPOSITORIES WITHOUT LICENSE FILE: {}'.format(len(repos_without_license)), ':', repos_without_license)
    print('REPOSITORIES WITHOUT LICENSE FILE: {}'.format(len(repos_without_license)), ':', repos_without_license, file=f)
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
    if re.search(r'\blicen[sc]ed?s?', decoded_text, re.I):
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
    parsed_text = json_parsing(file['url'], token, f)
    decoded_text = base64_decoding(parsed_text['content'])
    return decoded_text


def package_json_dependencies(every_repo, f, filename, token):
    if filename['name'] == 'package.json':
        dep = dependencies_listing(filename, token, f)
        parsed_dependencies = json.loads(dep)
        for name_dep in parsed_dependencies:
            if name_dep == 'dependencies' or name_dep == 'devDependencies':
                list_dependencies = []
                for name, version in parsed_dependencies[name_dep].items():
                    d = check_dependencies_license(every_repo, name, version, f)
                    list_dependencies.append((name, version, d))
                if list_dependencies != []:
                    print(name_dep, ': ', file=f)
                for s in list_dependencies:
                    print(s, file=f)


def check_dependencies_license(repo, name, version, f):
    url = requests.get('https://registry.npmjs.org/' + name + '/' + version)
    if url.status_code != 200:
        print(url.status_code, 'DEPENDENCIES: repo: ', repo, ', name: ', name, ', version: ', version)
        print(url.status_code, 'DEPENDENCIES: repo: ', repo, ', name: ', name, ', version: ', version, file=f)
    else:
        for a, b in url.json().items():
            dependencies_license = re.findall(r'\blicen[sc]ed?s?', a, re.I)
            for x in dependencies_license:
                if a == x:
                    return b


def pull_requests_search_licence_type(repo, sha, token, f):
    list_tree = []
    trees_url = json_parsing('https://api.github.com/repos/apiaryio/' + repo + '/git/trees/' + sha, token, f)
    for l in trees_url['tree']:
        if re_findall(l['path'], r'\blicen[sc]es?d?'):
            r = search_license_type_in_license_file(l, token, f)
            list_tree.append((l['path'], r))
        if re_findall(l['path'], r'\breadme') or l['path'] == 'package.json':
            v = search_license_type_in_readme_packagejson(l, token, f)
            list_tree.append((l['path'], v))
    return list_tree


def process_pull_requests(every_repo, f, list_licenses, token):
    pull_url = json_parsing('https://api.github.com/repos/apiaryio/' + every_repo + '/pulls', token, f)
    if pull_url != []:
        for g in pull_url:
            pull_licenses = pull_requests_search_licence_type(every_repo, g['head']['sha'], token, f)
            if list_licenses != pull_licenses:
                print('PULLS:', file=f)
                print('master: ', list_licenses, 'head: ', pull_licenses, file=f)


def compare_files(new_file, old_file):
    datestring = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
    pattern = 'compare_files' + datestring + '.txt'
    f_02 = open(pattern, 'w')
    with open(old_file, 'r') as f1, open(new_file, 'r') as f2:
        diff = difflib.ndiff(f1.readlines(), f2.readlines())
        f_02.write('File1: {}, File2: {} \n'.format(f1.name, f2.name))
        for i, line in enumerate(diff):
            if line.startswith(' '):
                continue
            sys.stdout.write('Line: {}, Text: {}'.format(i, line))
            f_02.write('Line: {}, Text: {}'.format(i, line))
    f_02.close()


if __name__ == '__main__':
    main()
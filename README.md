# apiary_license_check

`license_check.py` is checking all apiaryio repos for licenses (master + pull requests: readme, license, package.json) and printing it in a file and then compare the file to another file.

> **TASK**:
>I have Github organization (for example: github.com/apiaryio/) and I
>need to research all public projects about their dependency licenses.
>Are there only MIT, BSD license types in the project and their
>first-level dependencies? Which repositories violate this?
>
>Try to write a project so it can be re-used in the future, not just a
>one-time script.
>
>As the second part: We need to think of a solution how we can improve
>this to detect problematic dependencies before they get merged into
>master (e.g. detect this during the Pull Request phase).

---

### Getting Started

If you will run this app for the first time, please follow the `Check licenses` as you do not have `auth_key.txt` and any file to compare with yet. 

### Prerequisites

Please see the [requirements.txt](https://github.com/tystar86/apiary_license_check/blob/master/requirements.txt) for libraries you need to install.


### Check licenses

1.  Create file `auth_key.txt` with Github token in the same directory.
    
2.  Run:
        ```
        $ python3 license_check.py
        ```
    
3. In console you will get some basic results, for more details please see the created file `license_check_%Y-%m-%d_%H:%M:%S`.
      ```
      ### Console output

        REPOSITORIES TOTAL: 147

        REPOSITORIES WITHOUT LICENSE FILE: 30 : ['abagnale', 'api-blueprint-rfcs', 'apiaryio.github.com', 'batch', 'cloudwatch-to-papertrail', 'coffeescript-style-guide', 'difflet', 'documentation', 'dtl', 'dtl-1', 'googlediff', 'gzippo', 'heroku-datadog-drain', 'homebrew', 'hubot-redis-brain', 'JSON-js', 'kit-tooling', 'knox-mpu', 'lester', 'mongoose-dbref', 'natalie-venuto-test', 'nginx-buildpack', 'OKApi', 'pitboss', 'raven-node', 'stripe_to_xero', 'sundown', 'tully-test', 'uritemplate-js', 'winston-sentry']

        REPOSITORIES WITHOUT LICENSE: 9 : ['api-blueprint-rfcs', 'apiaryio.github.com', 'coffeescript-style-guide', 'JSON-js', 'kit-tooling', 'natalie-venuto-test', 'OKApi', 'raven-node', 'tully-test']
      ```
     
     
Name                                  | Description
------------------------------------- | ----------------------------------------------------------
`REPOSITORIES TOTAL:`                 | total count of all repositories for the user
`REPOSITORIES WITHOUT LICENSE FILE:`  | repositories without license file
`REPOSITORIES WITHOUT LICENSE:`       | repositories without any license (license, readme and package.json files)



```     
  ### File output


    REPO:  dredd-hooks-template
    LICENSE :  MIT
    README.md :  None
    package.json :  MIT
    devDependencies : 
    ('gherkin-lint', '^2.0.0', 'ISC')
    PULLS:
    master:  [('LICENSE', 'MIT'), ('README.md', None), ('package.json', 'MIT')] head:  [('README.md', None)]
 ```
 
Name                                     | Description
---------------------------------------- | ----------------------------------------------------------
`REPO:`                                  | repository name
`LICENSE:`                               | type of license, if not present = license file not in the repository
`README:`                                | type of license, if None = readme file is in the repository but contains nothing about license, if not present = readme file not in the repository
`package.json:`                          | type of license, if None = package.json file is in the repository but contains nothing about license, if not present = package.json file not in the repository
`dependencies/ devDependencies:`         | listing all dependencies and their license type
`PULLS:                            `     | if present it compares master files with head files


---


## Check licenses and compare with previous

1.  Run:
        ```
        $ python3 license_check.py license_check_2017-11-23_14:51:47
        ```
    
2. Please see **Check licenses point 3.** 
   
      
3. File `compare_files_%Y-%m-%d_%H:%M:%S` will be created. If compared files are same, the file will contain only their names.
    ```     
      ### compare_files_2017-10-21_12:45:56

        Old file: license_check_2017-07-10_10:32:05.txt, New file: license_check_2017-07-10_10:33:20.txt 
        Line: 1665, Text: - REPOSITORIES WITHOUT LICENSE FILE: 14 : ['abagnale', 'ace', 'Amanda', 'api-blueprint', 'api-blueprint-ast', 'api-blueprint-cheatsheet', 'api-blueprint-http-formatter', 'api-blueprint-rfcs', 'api-blueprint-sublime-plugin', 'api-elements', 'api-elements-jvm', 'api.apiblueprint.org', 'apiary-client', 'apiaryio.github.com', 'apiary_blueprint_convertor', 'apiblueprint.org', 'apiblueprintorg', 'attributes-kit', 'base-styles', 'batch']
        Line: 1666, Text: + REPOSITORIES WITHOUT LICENSE FILE: 30 : ['abagnale', 'api-blueprint-rfcs', 'apiaryio.github.com', 'batch', 'cloudwatch-to-papertrail', 'coffeescript-style-guide', 'difflet', 'documentation', 'dtl', 'dtl-1', 'googlediff', 'gzippo', 'heroku-datadog-drain', 'homebrew', 'hubot-redis-brain', 'JSON-js', 'kit-tooling', 'knox-mpu', 'lester', 'mongoose-dbref', 'natalie-venuto-test', 'nginx-buildpack', 'OKApi', 'pitboss', 'raven-node', 'stripe_to_xero', 'sundown', 'tully-test', 'uritemplate-js', 'winston-sentry']
      ```

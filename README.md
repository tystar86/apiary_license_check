# apiary_license_check

`license_check.py` is checking all apiaryio repos for licenses (master + pull requests: readme, license, package.json) and printing it in a file and compare the file to another file.

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


## Getting Started

If you will run this app for the first time, please follow the `Quick Start 1` as you do not have yet any file to compare with and `auth_key.txt`. 

### Prerequisites

What things you need to install the software and how to install them
Please see the [requirements.txt](https://github.com/tystar86/apiary_license_check/blob/master/requirements.txt) for libraries you need to install.

## Quick Start 1

1.  Create a file called `auth_key.txt` with Github token in the same directory.
    
2.  Run interactive configuration:

    ```shell
    $ python3 license_check.py
    ```
    
3. In console you will get some basics results, for more details please see the created file with DateTime stamp `license_check`.
      ```
      ### Console output

        404 DEPENDENCIES: repo: apiblueprintorg , name: winston , version: git://github.com/apiaryio/winston.git#production
        404 DEPENDENCIES: repo: blueprint-parser , name: pegjs , version: git://github.com/dmajda/pegjs.git#02af83f9b416778878e52e2cbbc22d96e312164e
        404 DEPENDENCIES: repo: broker , name: engine.io , version: Snyk/engine.io#1.6.11-patched
        404 DEPENDENCIES: repo: broker , name: engine.io-client , version: Snyk/engine.io-client#1.6.11-patched
        404 DEPENDENCIES: repo: cloudwatch-to-papertrail , name:  winston-papertrail , version: hyrwork/winston-papertrail
        404 DEPENDENCIES: repo: difflet , name: traverse , version: https://github.com/apiaryio/js-traverse/tarball/master
        404 DEPENDENCIES: repo: gavel.js , name: jsonlint , version: git+https://git@github.com/josdejong/jsonlint.git

        REPOSITORIES TOTAL: 147

        REPOSITORIES WITHOUT LICENSE FILE: 30 : ['abagnale', 'api-blueprint-rfcs', 'apiaryio.github.com', 'batch', 'cloudwatch-to-papertrail', 'coffeescript-style-guide', 'difflet', 'documentation', 'dtl', 'dtl-1', 'googlediff', 'gzippo', 'heroku-datadog-drain', 'homebrew', 'hubot-redis-brain', 'JSON-js', 'kit-tooling', 'knox-mpu', 'lester', 'mongoose-dbref', 'natalie-venuto-test', 'nginx-buildpack', 'OKApi', 'pitboss', 'raven-node', 'stripe_to_xero', 'sundown', 'tully-test', 'uritemplate-js', 'winston-sentry']

        REPOSITORIES WITHOUT LICENSE: 9 : ['api-blueprint-rfcs', 'apiaryio.github.com', 'coffeescript-style-guide', 'JSON-js', 'kit-tooling', 'natalie-venuto-test', 'OKApi', 'raven-node', 'tully-test']
      ```
      * **404 DEPENDENCIES:repo: apiblueprintorg, name: winston, version: git://github.com/apiaryio/winston.git#production** 
      is saying that wrong version is given.
      * **REPOSITORIES TOTAL:** (total count of all repositories for the user), **REPOSITORIES WITHOUT LICENSE FILE:**, **REPOSITORIES WITHOUT LICENSE:** (repositories without any license in license, readme or package.json file)
      
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
      * **REPO:** repository name, **LICENSE:** type of license, if not present = license file not in the repository, **README:** type of license, if None = readme file is in the directory but contains nothing about license, if not present = readme file not in the repository, **dependencies**/ **devDependencies:**listing all dependencies and their license type, **PULLS:** if present it compares master files with head files


## Quick Start 2

1.  Run interactive configuration:

    ```shell
    $ python3 license_check.py license_check_2017-11-23_14:51:47
    ```
    
2. Please see **Quick Start 1 point 3.** 
   
      
3. File `compare_files_%Y-%m-%d_%H:%M:%S` will be created. You can see it for compare details.
    ```     
      ### compare_files_2017-10-21_12:45:56

        File1: license_check_2017-07-10_10:32:05.txt, File2: license_check_2017-07-10_10:33:20.txt 
        Line: 1665, Text: - REPOSITORIES WITHOUT LICENSE FILE: 14 : ['abagnale', 'ace', 'Amanda', 'api-blueprint', 'api-blueprint-ast', 'api-blueprint-cheatsheet', 'api-blueprint-http-formatter', 'api-blueprint-rfcs', 'api-blueprint-sublime-plugin', 'api-elements', 'api-elements-jvm', 'api.apiblueprint.org', 'apiary-client', 'apiaryio.github.com', 'apiary_blueprint_convertor', 'apiblueprint.org', 'apiblueprintorg', 'attributes-kit', 'base-styles', 'batch']
        Line: 1666, Text: + REPOSITORIES WITHOUT LICENSE FILE: 30 : ['abagnale', 'api-blueprint-rfcs', 'apiaryio.github.com', 'batch', 'cloudwatch-to-papertrail', 'coffeescript-style-guide', 'difflet', 'documentation', 'dtl', 'dtl-1', 'googlediff', 'gzippo', 'heroku-datadog-drain', 'homebrew', 'hubot-redis-brain', 'JSON-js', 'kit-tooling', 'knox-mpu', 'lester', 'mongoose-dbref', 'natalie-venuto-test', 'nginx-buildpack', 'OKApi', 'pitboss', 'raven-node', 'stripe_to_xero', 'sundown', 'tully-test', 'uritemplate-js', 'winston-sentry']
      ```

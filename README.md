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

      
      ### File output

      - id: 1 (number, required) - The unique identifier for a product
      - name: A green door (string, required) - Name of the product
      - price: 12.50 (number, required)
      - tags: home, green (array[string])
      ```
      

## Quick Start 2

1.  Run interactive configuration:

    ```shell
    $ python3 license_check.py license_check_2017-11-23_14:51:47
    ```
    
2. In console you will get some basics results, for more details please see the created file with DateTime stamp `license_check_%Y-%m-%d_%H:%M:%S`.
      ```
      ### Console output

      - id: 1 (number, required) - The unique identifier for a product
      - name: A green door (string, required) - Name of the product
      - price: 12.50 (number, required)
      - tags: home, green (array[string])
      
      ### File output

      - id: 1 (number, required) - The unique identifier for a product
      - name: A green door (string, required) - Name of the product
      - price: 12.50 (number, required)
      - tags: home, green (array[string])
      ```
      
  3. File `compare_files_%Y-%m-%d_%H:%M:%S` will be created. You can see it forcompare details.
        ```
        ### compare_files_2017-10-21_12:45:56

      - id: 1 (number, required) - The unique identifier for a product
      - name: A green door (string, required) - Name of the product
      - price: 12.50 (number, required)
      - tags: home, green (array[string])
      ```

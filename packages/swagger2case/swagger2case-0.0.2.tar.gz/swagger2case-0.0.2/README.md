# swagger2case

[![LICENSE](https://img.shields.io/github/license/HttpRunner/swagger2case.svg)](https://github.com/HttpRunner/swagger2case/blob/master/LICENSE) [![Build Status](https://travis-ci.org/HttpRunner/swagger2case.svg?branch=master)](https://travis-ci.org/HttpRunner/swagger2case) [![coveralls](https://coveralls.io/repos/github/HttpRunner/swagger2case/badge.svg?branch=master)](https://coveralls.io/github/HttpRunner/swagger2case?branch=master)

Convert swagger data to yaml testcases for HttpRunner.

## usage

To see ``swagger2case`` version:

```shell
$ sw2case -V
0.0.1
```

To see available options, run

```shell
$ sw2case -h
usage: sw2case [-h] [-V] [--log-level LOG_LEVEL]
               [swagger_testset_file] [output_testset_file]

Convert swagger testcases to JSON testcases for HttpRunner.

positional arguments:
  swagger_testset_file  Specify swagger testset file.
  output_testset_file   Optional. Specify converted JSON testset file.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show version
  --log-level LOG_LEVEL
                        Specify logging level, default is INFO.
```

## examples

In most cases, you can run ``swagger2case`` like this:

```shell
$ sw2case test/test.json output.json
INFO:root:Generate JSON testset successfully: output.json
```

As you see, the first parameter is swagger source file path, and the second is converted JSON file path.

The output testset file type is detemined by the suffix of your specified file.

If you only specify swagger source file path, the output testset is in JSON format by default and located in the same folder with source file.

```shell
$ sw2case test/test.json
INFO:root:Generate JSON testset successfully: test/test.output.json
```

## generated testset

generated JSON testset ``output.json`` shows like this:

```json
[
    {
        "test": {
            "name": "/api/v1/Account/Login",
            "request": {
                "method": "POST",
                "url": "https://httprunner.top/api/v1/Account/Login",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {
                    "UserName": "test001",
                    "Pwd": "123",
                    "VerCode": ""
                }
            },
            "validate": []
        }
    }
]
```


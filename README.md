# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory. To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

If we need a local PostgreSQL database, then use the below command to start PostgreSQL locally.

`docker compose up -d`

Some Python modules cannot be located by the lambda function. We need to create a zip of those modules and use them as a layer.

For that use below Docker command that is used to install Python dependencies in a way that is compatible with AWS Lambda.

- `docker run -v "$PWD":/var/task "amazon/aws-sam-cli-build-image-python3.9" /bin/sh -c "pip install -r lambda/requirements.txt -t python/lib/python3.9/site-packages/; exit"`

Then we need to create zip 

- `zip -r layers/pythonlib_layer.zip python`
  

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Testing

- `cdk synth > template.yaml`
  - `sam build`
- `sam local invoke MyLambdaFunction --no-event -t ./cdk.out/AwsCdkPythonPsycopg2Stack.template.json`
- Read : `sam local invoke MyLambdaFunction --event events/read.json -t ./cdk.out/AwsCdkPythonPsycopg2Stack.template.json`
- Write : `sam local invoke MyLambdaFunction --event events/write.json -t ./cdk.out/AwsCdkPythonPsycopg2Stack.template.json`

### Payload

- Write

  ```
  {
      "action": "write",
      "data": {
          "name": "Sample Record",
          "description": "This is a test description."
      }
  }
  ```

- Read

  ```
  {
      "action": "read"
  }
  ```

### Result

- Write

  ```
  (base) ➜  cdk-sam-demo git:(main) ✗ sam local invoke MyLambdaFunction --event events/write.json -t ./cdk.out/CdkSamDemoStack.template.json
  Invoking app.lambda_handler (python3.9)
  Decompressing
  /Users/santosh/Documents/workspace/aws/cdk-sam-demo/cdk.out/asset.b9e5b43dd3a267
  962ccec789725e1117a07177602f17375f57b5d4d009e20ff8.zip
  PyhonLibLayer9012B95C is a local Layer in the template
  Local image is up-to-date
  Building image.....................
  Using local image: samcli/lambda-python:3.9-x86_64-df98eaa0c4be380691b9d0fb2.

  Mounting
  /Users/santosh/Documents/workspace/aws/cdk-sam-demo/cdk.out/asset.5154647dfbc9e4
  d979237033784da0522eab6dd6532eef010dd6829545c8cb85 as /var/task:ro,delegated,
  inside runtime container
  START RequestId: 73cfbe98-e830-44f0-b72e-efb08227af7d Version: $LATEST
  END RequestId: e45b19ca-7ae7-4239-876f-22484bb3062c
  REPORT RequestId: e45b19ca-7ae7-4239-876f-22484bb3062c	Init Duration: 0.46 ms	Duration: 1501.97 ms	Billed Duration: 1502 ms	Memory Size: 256 MB	Max Memory Used: 256 MB
  {"statusCode": 200, "body": "{\"message\": \"Record created\", \"record_id\": 1}"}
  ```

- Read

  ```
  (base) ➜  cdk-sam-demo git:(main) ✗ sam local invoke MyLambdaFunction --event events/read.json -t ./cdk.out/CdkSamDemoStack.template.json
  Invoking app.lambda_handler (python3.9)
  Decompressing
  /Users/santosh/Documents/workspace/aws/cdk-sam-demo/cdk.out/asset.b9e5b43dd3a267
  962ccec789725e1117a07177602f17375f57b5d4d009e20ff8.zip
  PyhonLibLayer9012B95C is a local Layer in the template
  Local image is up-to-date
  Building image.....................
  Using local image: samcli/lambda-python:3.9-x86_64-df98eaa0c4be380691b9d0fb2.

  Mounting
  /Users/santosh/Documents/workspace/aws/cdk-sam-demo/cdk.out/asset.5154647dfbc9e4
  d979237033784da0522eab6dd6532eef010dd6829545c8cb85 as /var/task:ro,delegated,
  inside runtime container
  START RequestId: 7584b657-d6ea-4720-a0ca-5b659efe58a1 Version: $LATEST
  END RequestId: 307c58ab-fade-40ab-b28a-085fe2f6ad2c
  REPORT RequestId: 307c58ab-fade-40ab-b28a-085fe2f6ad2c	Init Duration: 0.47 ms	Duration: 1200.22 ms	Billed Duration: 1201 ms	Memory Size: 256 MB	Max Memory Used: 256 MB
  {"statusCode": 200, "body": "{\"records\": [{\"id\": 1, \"name\": \"Test Record\", \"description\": \"This is a test description.\"}]}"}
  ```

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

Enjoy!

# gcs upload sample - gae python

> simple google cloud storage upload sample (gae python)

install required package

```sh
$ pip install -r requirements.txt -t lib
```

modify your `DEVELOPER_KEY` & `BUCKET`

_app.py_

```python

DEVELOPER_KEY = ''
BUCKET = ''
```

running locally

```sh
$ dev_appserver.py app.yaml
INFO     2016-10-26 04:18:41,993 devappserver2.py:769] Skipping SDK update check.
INFO     2016-10-26 04:18:42,068 api_server.py:205] Starting API server at: http://localhost:49682
INFO     2016-10-26 04:18:42,071 dispatcher.py:197] Starting module "default" running at: http://localhost:8080
INFO     2016-10-26 04:18:42,072 admin_server.py:116] Starting admin server at: http://localhost:8000
```

running locally with service account (debug locally)


Create Service Account

1.	Click **APIs & Auth** > **credential**.
2.	Click **Click new Client ID**.
3.	Choose **Service Account**.
4.	Key type : **P12 Key**
5.	Click **Create Client ID**
6.	**P12.Key** file will be downloaded. You have to convert `p12` to `pem` cause PKCS12 format is not supported by the PyCrypto library.

	```sh
	(openssl pkcs12 -in xxxxx.p12 -nodes -nocerts > privatekey.pem)
	```

```
$ dev_appserver.py app.yaml  --appidentity_email_address=<your-service-account> --appidentity_private_key_path=<your-service-account-pem-key-path> --skip_sdk_update_check=yes --enable_sendmail=yes
```

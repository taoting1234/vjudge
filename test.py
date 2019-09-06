import requests
from threading import Thread


def f():
    headers = {
        'User-Agent': 'zuccacm'
    }
    auth = (
        'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU2NzM1MTM0MywiZXhwIjoxNTY5OTQzMzQzfQ.eyJ1aWQiOiIzMTcwMjQxMSJ9.9Te5hkLBe2ka6jcfHmyQOS5lMIvzMvUF-HyI2ewUU1guoKby7UTn4Wu2AnTPzPIaqUXgUAi0dQ9FoYj9lpwT9A',
        ''
    )
    data = {
        "problem_id": 2,
        "code": "var a,b:longint;\nbegin\nread(a,b);\nwrite(a+b);\nend.",
        "language": "2"
    }
    res = requests.post('http://vj-api.newitd.com/v1/solution', headers=headers, auth=auth, json=data).json()
    print(res)


for i in range(10):
    Thread(target=f).start()

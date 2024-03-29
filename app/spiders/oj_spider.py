from app.spiders.spider_http import SpiderHttp


class OjSpider:
    problem_format = """
**Time Limit: {time_limit}ms**

**Memory Limit: {memory_limit}MB**

### Description

{description}

### Input

{input}

### Output

{output}

### Sample Input

```
{sample_input}
```

### Sample Output

```
{sample_input}
```
"""

    def __init__(self, remote_user):
        self.username = remote_user.username
        self.password = remote_user.password
        self.request = SpiderHttp()
        if remote_user.cookies:
            self.request.sess.cookies.update(remote_user.cookies)

        if not self.check_login_status():
            if not self.login():
                raise Exception('remote user login error')
            assert self.check_login_status()
            remote_user.modify(cookies=self.request.sess.cookies.get_dict())

    def check_login_status(self):
        pass

    def login(self):
        pass

    def get_status(self, remote_id):
        pass

    def submit(self, remote_oj, remote_problem, language, code, **kwargs):
        pass

    def get_problem(self, remote_oj, remote_problem):
        pass

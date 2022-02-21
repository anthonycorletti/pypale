# pypale

(Py)thon (Pa)ssword(le)ss Tokens.

```sh
pip install pypale
```

## Usage

```py
from pypale import Pypale

token_ttl_minutes = 14 * 24 * 60        # 2 weeks
token_issue_ttl_seconds = 2 * 60 * 60   # 2 hours
base_url = "mydomain.com"
secret_key = "loadthisfromyoursecretsmanager"

pypale = Pypale(
    base_url=base_url,
    secret_key=secret_key,
    token_ttl_minutes=token_ttl_minutes,
    token_issue_ttl_seconds=token_issue_ttl_seconds)

email = "jane.doe@example.com"
token = pypale.generate_token(email)
assert pypale.valid_token(token, email)
```

## An example with SendGrid

```py
# send an email with a magic login link to "jane.doe@example.com"
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

email = "jane.doe@example.com"
token = pypale.generate_token(email)
link = f"https://mydomain.com/link_login/?code={token}"
sg = sendgrid.SendGridAPIClient(api_key=your_sendgrid_api_key)
from_email = Email("bob@mydomain.co")
to_email = To(email)
subject = "Hello!"
content = Content(
            "text/html", f"Click this <a href={link}>link</a> to log in.")
mail = Mail(from_email, to_email, subject, content)
response = self.sg.client.mail.send.post(request_body=mail.get())
print (response)

# in your link_login route, mentioned in the link var above,
# make sure to call pypale.validate_token with the token and
# properly handle valid and invalid tokens.
# for example ...

def link_login(code: str):
    if not pypale.valid_token(code):
        raise Exception("Invalid login.")
    access_token = base64.b64decode(code).decode("utf8")
    return {
        "access_token": base64.b64decode(code).decode("utf8"),
        "token_type": "bearer"
    }
```

### Contributions & Suggestions

[Pull requests](https://github.com/anthcor/pypale/compare) and [issues](https://github.com/anthcor/pypale/issues/new) are very welcome!

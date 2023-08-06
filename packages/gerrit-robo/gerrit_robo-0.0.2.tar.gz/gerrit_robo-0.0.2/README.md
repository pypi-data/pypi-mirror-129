gerrit-robo
==========

This is a very thin wrapper around the gerrit api to 
allow robots to add comments to a patchset (and maybe 
more later)

**Please note, that this a work in progress and is not usable, nor tested**


## Usage

```
gerrit = Gerrit('http://review.domain.de', 'projectname').with_auth(
    'your_username', '<<http_password>>')
change_id = 'I09d1b8dc8d9eb072d4bd387f4c75c80cda43ebd5'

review = Review('The bot reviewed')
review.comment('README.md', [1, 3], 'A robot comment')
review.comment('README.md', 4, 'This is a comment, too')
gerrit.send_review(change_id, review)
```

## Generate HTTP Password

You cannot login with your normal password. Rather:
1. Login into Gerrit
2. Click on your profile image > Settings > HTTP Credentials
3. `Generate New Password`
4. Copy it immediatly as it will be lost ast soon as you close this moda
5. Inset it into your source-code under `gerrit.with_auth`


(found [here](https://stackoverflow.com/questions/35361276/gerrit-authentication-required))

# Nested
Coding Challenge

### Installing

```
virtualenv venv
source venv/bin/activate
pip install -r requirements_lock.txt
```

### Dependencies
Modify the `requirements.txt`file to add or update new deps.
After modifying, run:

```
pip install -r requirements.txt --upgrade && pip freeze > requirements_lock.txt
```

That will save everything into the `requirements.txt` file but won't be very
user-readable. Think of this as the difference between Gemfile and Gemfile.lock
for anyone with Ruby experience.

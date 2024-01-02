# Alarmbot Bot

## Project Structure

### When single app

```
src/
    package/
        sub_package/
            __init__.py
            sub_package.py
        __init__.py
        package.py
    __init__.py
    requirements.txt
    setup.py
app.py
Dockerfile
.env
.env.template
```

### When multiple apps

```
src/
    package/
        sub_package/
            __init__.py
            sub_package.py
        __init__.py
        package.py
    __init__.py
    requirements.txt
    setup.py
apps/
    alarm_bot/
        app.py
    ask_bot/
        app.py
dockerfiles/
    alarm_bot/
        Dockerfile
    ask_bot/
        Dockerfile
.env
.env.template
```
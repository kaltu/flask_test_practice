# Prerequisites

```pip install -r requirements.txt```

Download ```chromewebdriver``` from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads)

Add webdriver excutable path to ```PATH``` environment variable or place it at ```<proj_root>/robot```

# Launching main server
At project root:

Windows CMD
```
set FLASK_APP=main
set FLASK_ENV=development
flask run --host 0.0.0.0 --port 80
```

Windows Power Shell
```
$Env:FLASK_APP = "main"
$Env:FLASK_ENV = "development"
flask run --host 0.0.0.0 --port 80
```

Unix Bash (Mac, Linux etc.)
```
export FLASK_APP=main
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 80
```

# Run unit tests
First, make sure another ```flask run``` instance is up and running.

At project root:

Windows CMD
```
set FLASK_APP=main
set FLASK_ENV=development
flask test
```

Windows Power Shell
```
$Env:FLASK_APP = "main"
$Env:FLASK_ENV = "development"
flask test
```

Unix Bash (Mac, Linux etc.)
```
export FLASK_APP=main
export FLASK_ENV=development
flask test
```

# Run robot tests
With ```chromedriver``` excutable installed
At ```<proj_root>/robot```

```
robot ./test_ui.robot
```


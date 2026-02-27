# Building from source

Create a new [python virtual environment](https://docs.python.org/3/library/venv.html) and [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work) (recommended)

```bash
python -m venv venv

# On windows
.\venv\scripts\activate

# On Linux
source <venv>/bin/activate
```

From the root of the repository run

```bash
pip install requirements.txt
```

## Creating the executable

The executable from the release was created with [pyinstaller](https://pyinstaller.org/en/stable/)

From the root of the repository, create the .spec file with the command:

```bash
pyi-makespec ./src/main.py
```

This will create the `main.spec` file, which you can modify freely. However, the app needs the following values inside `Analysis()`.

```spec
datas=[('src/config','config'),('src/data','data'),('src/logs','logs'),('src/screens/html','screens/html'),('src/styles','styles')]
```

Finally, create the executable with the following command:

```bash
pyinstaller ./main.spec
```

This will create the `dist/app` directory with the app.exe and the `_internal` directory which contains the data of the application (config, blacklist, styles, etc.)

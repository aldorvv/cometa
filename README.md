# Install API dependencies
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

# Run tests
```bash
$ pytest -vv
```

# Run API
```bash
$ uvicorn app:app --reload
```

# Install UI dependencies
```bash
$ cd ui/cometa
$ npm install
```

# Run UI
```bash
$ cd ui/cometa
$ npm run serve
```
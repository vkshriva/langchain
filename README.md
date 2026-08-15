# Dockerized Python dev environment

How to build and start:

```bash
docker compose up --build
```

For the interactive chat app, run the container in attached mode so your keyboard input reaches the Python process:

```bash
APP_TARGET=ex_2/main.py docker compose run --rm -it app
```

How to run after editing code without rebuilding:

```bash
docker compose up
```

Run a specific Python file from a subfolder:

```bash
APP_TARGET=services/foo/main.py docker compose up --build
```

You can also run a file from any nested folder inside `app/` by changing the path:

```bash
APP_TARGET=tasks/bar/main.py docker compose up
```

Rebuild only when `requirements.txt` changes:

If you change `requirements.txt`, rebuild the image so dependencies are reinstalled:

```bash
docker compose up --build
```

Notes:

- You can add more `.py` files inside the `app/` folder, including nested subfolders.
- Because the entire `app/` folder is mounted as a volume, new files you create on the host will be immediately available inside the container without changing the Dockerfile or compose file.

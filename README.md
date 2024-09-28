# mtalive

A simple process alive checker w/ webserver support.

The server will listen on `ADDRESS:PORT/mtalive`

### Preinstalled dependencies
You must have the following packets installed:

- `python3` (tested w/ 3.10.x)
- `git` (update script)

### Install/run/update

To install mtalive, clone the repo and run `update.sh`.

To update mtalive, simply run `update.sh` again.

### Run
Params:
1. `minetest_path` (required)
2. `listening_address` (optional, defaults to `127.0.0.1`)
3. `listening_port` (optional, defaults to `3000`)

(The order of params is important)

```bash
./mtalive/env/bin/python3 mtalive.py /home/user/minetest/bin/minetest 127.0.0.1 3000
```

Make sure to activate the Python venv/use the Python binary from the `env` folder.

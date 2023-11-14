# mtalive

A simple process alive checker w/ webserver support.

### Preinstalled dependencies
You must have the following packets installed:

- `python3` (tested w/ 3.10.x)
- `git` (update script)

### Install/run/update

To install mtalive, clone the repo and run `update.sh`.

To update mtalive, simply run `update.sh` again.

#### Run
Params:
- `-e` mtalive_minetest_path (required)
- `-a` mtalive_listening_address (optional, defaults to `127.0.0.1`)
- `-p` mtalive_listening_port (optional, defaults to `3000`)

```bash
./run.sh -e /home/nik/minetest/bin/minetest -a 127.0.0.1 -p 80
```

**You don't have to** set the `source` first, the script will do that for you.
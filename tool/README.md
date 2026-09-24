# The tool

Not vendored here, build it from source at the pinned commit.

- Repo: `git@github.com:b-elamine/S4CLI.git`
- Commit: `9850fbd564c0e9db9504627f53f99ce12268a978`

## Build

```
git clone git@github.com:b-elamine/S4CLI.git
cd S4CLI
git checkout 9850fbd564c0e9db9504627f53f99ce12268a978
mvn -q clean package -DskipTests
```

Produces two files in `target/`. Run `sam4c-cli.jar`, the shaded jar with
everything bundled in. Do not run `sam4c-cli-1.0-SNAPSHOT.jar` -- it is
Maven's plain build output, has no runnable manifest, and will fail with
"no main manifest attribute" if you try.

## Run

```
java -jar target/sam4c-cli.jar --validate <arch.yaml> <rules.secdsl>
```

## Verify the build

```
python3 scripts/reproduce.py /path/to/sam4c-cli.jar
```
from this evaluation folder's root. Expect `15/15 checks passed`.

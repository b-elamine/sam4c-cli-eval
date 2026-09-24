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

Produces `target/sam4c-cli.jar` (the shaded jar, use this one —
`sam4c-cli-1.0-SNAPSHOT.jar` in the same folder has no runnable manifest).

## Run

```
java -jar target/sam4c-cli.jar --validate <arch.yaml> <rules.secdsl>
```

## Verify the build

```
python3 scripts/reproduce.py /path/to/sam4c-cli.jar
```
from this evaluation folder's root. Expect `15/15 checks passed`.

## Two fixes made at this commit

- Authentication now counts a component sharing a credential with the
  authenticator as verifying the token itself, instead of requiring the
  authenticator physically on the path. Removed a false finding on Bank of
  Anthos (shared JWT, verified locally by each service).
- A `via` mediator that's also the source/target of an Isolation rule no
  longer silently disables the search. Found on Sock Shop.

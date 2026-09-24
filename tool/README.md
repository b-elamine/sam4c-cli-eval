# The tool

This evaluation was run against one exact commit of the tool. Nothing in this
folder vendors the tool itself; build it from source at the pinned commit.

## Pinned version

- Repo: `git@github.com:b-elamine/S4CLI.git`
- Commit: `9850fbd564c0e9db9504627f53f99ce12268a978`
- Commit message: `fix authn and via checks`

## Build

```
git clone git@github.com:b-elamine/S4CLI.git
cd S4CLI
git checkout 9850fbd564c0e9db9504627f53f99ce12268a978
mvn -q clean package -DskipTests
```

This produces `target/sam4c-cli.jar` (the shaded jar, with the manifest set;
`target/sam4c-cli-1.0-SNAPSHOT.jar` in the same folder is the unshaded jar
and has no runnable manifest, do not use it).

## Run

```
java -jar target/sam4c-cli.jar --validate <arch.yaml> <rules.secdsl>
```

## Verify this is the right build

```
python3 scripts/reproduce.py /path/to/sam4c-cli.jar
```

from the root of this evaluation folder. Expect `28/28 checks passed`.

## What changed at this commit, relevant to the evaluation

Two fixes were made to the tool while building this evaluation, both tested
by the pilot pairs in `tool-validation-pilot/`:

- Authentication now counts a component that shares a credential with the
  authenticator as verifying the token itself, instead of requiring the
  authenticator to sit physically on the path. This removed a false finding
  on Bank of Anthos (its services verify a shared JWT locally). Tested by
  pair `c9-cwe306-token-at-target`.
- In an Isolation rule with a `via` mediator, a mediator that is also the
  source or target of the rule no longer silently disables the search.
  Found when a `via` rule on Sock Shop returned nothing. Tested by pair
  `c8-multihop-mediator`.

# Ground-truth manifests

Every file under here is copied verbatim from the upstream repo, at the
commit recorded in `../../../FINDINGS.md` section 1 — same bytes, same path
relative to the repo root, same filename. Nothing is renamed, merged, or
edited.

| System | Path here | Real path in the upstream repo | Repo |
|---|---|---|---|
| bank-of-anthos | `bank-of-anthos/kubernetes-manifests/*.yaml` (10 files) | `kubernetes-manifests/*.yaml` | GoogleCloudPlatform/bank-of-anthos |
| online-boutique | `online-boutique/release/kubernetes-manifests.yaml` | `release/kubernetes-manifests.yaml` | GoogleCloudPlatform/microservices-demo |
| sock-shop | `sock-shop/deploy/kubernetes/complete-demo.yaml` | `deploy/kubernetes/complete-demo.yaml` | microservices-demo/microservices-demo |
| teastore | `teastore/examples/kubernetes/teastore-clusterip.yaml` | `examples/kubernetes/teastore-clusterip.yaml` | DescartesResearch/TeaStore |
| opentelemetry-demo | `opentelemetry-demo/compose.yaml` | `compose.yaml` (repo root) | open-telemetry/opentelemetry-demo |
| hotel-reservation | `hotel-reservation/hotelReservation/docker-compose.yml` | `hotelReservation/docker-compose.yml` | delimitrou/DeathStarBench |
| social-network | `social-network/socialNetwork/docker-compose.yml` | `socialNetwork/docker-compose.yml` | delimitrou/DeathStarBench |

hotel-reservation and social-network come from the same upstream repo
(DeathStarBench), each from its own subfolder.

## Why bank-of-anthos is a folder and the rest are one file

bank-of-anthos is the only one of the 7 where the upstream repo itself
splits the deployment into multiple files, one per workload plus a shared
`config.yaml`. The other 6 repos each ship one single manifest file as their
deploy artifact, so one file here is the complete, faithful copy.

An earlier version of this folder had bank-of-anthos rebuilt as one
concatenated file, and the other 6 renamed/flattened to `<system>.yaml`. That
lost the "this is literally what ships in the repo" property. This version
fixes that: what's here is exactly what git tracks upstream, at its real
path.

For the service source code cited as evidence in `FINDINGS.md` (e.g.
`src/frontend/frontend.py`, `UserMentionService.cpp`), the exact repo and
commit for each is also listed in `FINDINGS.md` section 1 — those files
aren't vendored here, since it's whole service source trees, not single
manifests; clone at the pinned commit if you need to check a citation
yourself.

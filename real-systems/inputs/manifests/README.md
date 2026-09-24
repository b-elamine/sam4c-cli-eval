# Ground-truth manifests

Copied verbatim from the upstream repo, real path, real filename, nothing
renamed or merged. Commits: `../../../FINDINGS.md` section 1.

| System | Path here | Real path upstream | Repo |
|---|---|---|---|
| bank-of-anthos | `bank-of-anthos/kubernetes-manifests/*.yaml` (10 files) | `kubernetes-manifests/*.yaml` | GoogleCloudPlatform/bank-of-anthos |
| online-boutique | `online-boutique/release/kubernetes-manifests.yaml` | `release/kubernetes-manifests.yaml` | GoogleCloudPlatform/microservices-demo |
| sock-shop | `sock-shop/deploy/kubernetes/complete-demo.yaml` | `deploy/kubernetes/complete-demo.yaml` | microservices-demo/microservices-demo |
| teastore | `teastore/examples/kubernetes/teastore-clusterip.yaml` | `examples/kubernetes/teastore-clusterip.yaml` | DescartesResearch/TeaStore |
| opentelemetry-demo | `opentelemetry-demo/compose.yaml` | `compose.yaml` | open-telemetry/opentelemetry-demo |
| hotel-reservation | `hotel-reservation/hotelReservation/docker-compose.yml` | `hotelReservation/docker-compose.yml` | delimitrou/DeathStarBench |
| social-network | `social-network/socialNetwork/docker-compose.yml` | `socialNetwork/docker-compose.yml` | delimitrou/DeathStarBench |

bank-of-anthos is the only repo that ships its manifest as multiple files;
the other 6 each ship one single file, so one file here is the full copy.

Source code cited as evidence (not manifests) is in `../evidence/`, not
here.

# Findings explained and verified against the source repos

Written 2026-09-20, tool commit `7ba7166` at the time, re-verified against tool commit `9850fbd564c0e9db9504627f53f99ce12268a978` (the pinned commit for this evaluation, see `tool/README.md`) on 2026-09-24 with no change in results. All 7 real systems were cloned; the 3 repos that moved after the modeling date are checked out at their 2026-07-31 commit, the other 4 have no newer commits and every finding was checked against the repo files. Evidence is `path:line` inside the clone, and every path below is the real path in the repo. From this evaluation folder, reproduce with `python3 scripts/reproduce.py <path-to-jar>`.

Every deployment manifest cited below is vendored verbatim in `real-systems/inputs/manifests/`, and every service source file cited below is vendored verbatim in `real-systems/inputs/evidence/` — both at their real repo path, see each folder's README.

## Tool change made during this check

Authentication now counts a component that shares a credential with the authenticator as verifying the token itself (`SemanticValidator.sharingCredential`). Before, only an authenticator physically on the path counted, which wrongly reported token-based systems such as Bank of Anthos.

A second fix: in an Isolation rule with `via`, a mediator that is also the source or target of the rule no longer disables the search silently (found when a `via` rule on Sock Shop returned nothing).

## 1. Repos checked

| System | Repo | Commit checked out (date) | Ground-truth file | Vendored copy vs that commit |
|---|---|---|---|---|
| bank-of-anthos | GoogleCloudPlatform/bank-of-anthos | 1e40564f 2026-07-13 | `kubernetes-manifests/*.yaml` (10 files: 9 workloads + config.yaml) | identical, all 10 files vendored as-is |
| hotel-reservation | delimitrou/DeathStarBench | 6ecb097 2024-06-27 | `hotelReservation/docker-compose.yml` | identical |
| online-boutique | GoogleCloudPlatform/microservices-demo | 9a4616e7 2026-07-13 | `release/kubernetes-manifests.yaml` | identical at 2026-07-31; HEAD (2026-09-18) differs: same 12 workloads and service types, 11 image tags changed |
| opentelemetry-demo | open-telemetry/opentelemetry-demo | f7408a5 2026-07-31 | `compose.yaml` | identical at 2026-07-31; HEAD (2026-09-18) differs: same 20 services |
| social-network | delimitrou/DeathStarBench | 6ecb097 2024-06-27 | `socialNetwork/docker-compose.yml` | identical |
| sock-shop | microservices-demo/microservices-demo + 8 service repos | 9dff06f 2023-12-05 | `deploy/kubernetes/complete-demo.yaml` | identical |
| teastore | DescartesResearch/TeaStore | 34b37f7 2025-01-08 | `examples/kubernetes/teastore-clusterip.yaml` | identical |

All 7 ground-truth files are vendored verbatim, at their real repo path, under
`real-systems/inputs/manifests/` (see that folder's README for the exact
path mapping). Sock Shop service repos used for source checks (commit): carts f4e8005 catalogue 925e08e front-end 52dee65 orders 546a10c payment 384e334 queue-master 7dc3372 shipping 9c0fbfa user e1a79e7.

## 2. From git to the YAML model

Each system is one `.arch.yaml` (structure) and one `.secdsl` (rules). Steps, applied identically to all 7:

| Step | What is read in git | What goes in the model |
|---|---|---|
| 1 | One ground-truth deployment file (see section 1) | one `Architecture` named after the system |
| 2 | Nothing: manifests do not say which machine runs a pod | one `Worker` host (the cluster or compose host), every deployable `deployedOn` it |
| 3 | Every Kubernetes Deployment/StatefulSet, every Compose service | one `Deployable` each. `Data` if the image is a database, cache or broker (mongo, postgres, mariadb, redis, memcached, rabbitmq), else `App` |
| 4 | k8s `Service.type` (LoadBalancer or NodePort), Compose `ports:` | `exposure: external` only for the intended public entry point. Everything else `internal`. Compose maps host ports to dev UIs (jaeger, consul, flagd-ui); those stay `internal` and the header of each model says so |
| 5 | `containerPort`, Compose `ports`, known protocol of the image | one `Port` per endpoint with number (container port) and protocol: `http`, `grpc`, `tcp` (databases, Thrift), `udp` (jaeger agent) |
| 6 | Env vars and ConfigMaps naming another service (`PAYMENT_SERVICE_ADDR: paymentservice:50051`), Compose `depends_on`, then the service source code where the manifest is silent (`config_json["text-service"]`, `srv-geo`, `Service.PERSISTENCE`, lua scripts) | one `Connector` per directed call, one `out` link on the caller, one `in` link on the callee |
| 7 | `image:` | one `Implementation` per deployable (`runtime: container`, image when the manifest has a literal one) |
| 8 | Volumes | `persistent: true` only if the data volume outlives the pod (PVC, volumeClaimTemplate, hostPath, named Compose volume). `emptyDir`, no volume, or an init-script mount count as not persistent |
| 9 | The author | `Domain` attribute (business role) and `DataClass` on sensitive stores. This is the only step that is a judgment, not a read |
| 10 | The author, one rubric for all 7 | `.secdsl`: isolate the session or account store from the public entry point; `Availability medium` on the user-facing path; `Confidentiality` where the call graph carries payment or ledger data; `Authentication` only where the system has a real auth service |

Example, Online Boutique `frontend`: the Service `frontend-external` is `type: LoadBalancer` (`release/kubernetes-manifests.yaml:588`), so `exposure: external`; the Deployment's `containerPort: 8080` becomes the port `http_in`; its env vars `PRODUCT_CATALOG_SERVICE_ADDR` etc. become one connector each (`FE_to_ProductCatalog`, ...); no `replicas:` field, so the model declares no `scale` and the tool counts one copy.

## 3. Is each model right? Checked against the repos

| System | Units in repo / modeled | External entry points | Data flags checked | Edges in model | Edge sources (manifest / service code / config) |
|---|---|---|---|---|---|
| bank-of-anthos | 9 / 9 | frontend | 2 Data components, flags match the volumes | 12 | 11 / 1 / 0 |
| hotel-reservation | 24 / 24 | frontend (judgment) | 12 Data components, flags match the volumes | 41 | 22 / 9 / 10 |
| online-boutique | 12 / 12 | frontend | 1 Data components, flags match the volumes | 16 | 16 / 0 / 0 |
| opentelemetry-demo | 20 / 20 | frontend-proxy (judgment) | 2 Data components, flags match the volumes | 48 | 48 / 0 / 0 |
| social-network | 27 / 27 | nginx-thrift, media-frontend (judgment) | 13 Data components, flags match the volumes | 46 | 13 / 27 / 6 lua |
| sock-shop | 14 / 14 | front-end | 5 Data components, flags match the volumes | 15 | 2 / 13 / 0 |
| teastore | 7 / 7 | teastore-webui | 1 Data components, flags match the volumes | 13 | 6 / 7 / 0 |

Errors found by this check and fixed in the models (none changed a finding):

- 24 units added: hotel 9, social-network 8, OTel 5, Online Boutique `loadgenerator`, Bank of Anthos `loadgenerator`. 0 manifest units are missing now.
- 14 `persistent` flags were wrong and are now false: Bank of Anthos 2 (`emptyDir`), Sock Shop 4, TeaStore 1 (no volume), OTel `astronomy-db` (init script only), Social-Network 6 (no volumes).
- 6 edges did not exist in the code and were removed: Sock Shop `orders -> queue-master`; Social-Network `compose-post -> social-graph / url-shorten / user-mention`, `media-service -> media-mongodb`, `media-frontend -> media-service`.
- 31 real edges were missing and were added: hotel consul x10; Social-Network 14 (text -> url-shorten and user-mention, home-timeline -> post-storage and social-graph, user <-> social-graph, user-timeline -> post-storage, user-mention -> user stores, nginx-thrift -> 4 services, media-frontend -> media-mongodb); TeaStore 3 (auth, image, recommender -> persistence); Sock Shop 3 (shipping -> rabbitmq, orders -> carts and user); Bank of Anthos `ledgerwriter -> balancereader`.
- 2 port numbers changed to the container-port convention (Online Boutique `emailservice` 5000 -> 8080, Social-Network `media-frontend` 8081 -> 8080). A false header claim was corrected: Social-Network `post-storage-service` also publishes a host port (10002:9090, a debug mapping, kept internal).

Still a judgment, not a read from git (the model is right only if you accept these):

- Which host-port services count as `external` on the 3 Compose systems (compose maps host ports to dev UIs too).
- `Domain` and `DataClass` tags, and the rubric in `.secdsl`.
- Port numbers for `jaeger` (`6831`, from Jaeger's agent default, not published by the compose files).
- Protocol labels of a few OTel edges (`flagd` as `grpc`).

So the honest answer is: units, exposure of the real entry points, persistence, ports and every edge are now checked against the repos. The exposure of dev tooling, the tags and the rubric are author decisions.

## 4. The findings

Verdict key: **Confirmed** = the fact is true in the repo. **Partial** = exposure true, the app has a login on some routes. **Model artifact** = true in the model, not a weakness in the real app. **By design** = real path, intended by the app. Replicas findings are true facts but exist because the rubric asks for at least 2 copies (`Availability medium`).

| # | System | Check | Subject | Why the tool reports it | Evidence in repo | Verdict |
|---|---|---|---|---|---|---|
| 1 | bank-of-anthos | Unauthenticated entry | frontend | exposed component and no `Authentication` rule targets it | bank-of-anthos/kubernetes-manifests/frontend.yaml:35 `type: LoadBalancer`; `bank-of-anthos/src/frontend/frontend.py:92-105`: `verify_token`, redirect to `login_page`. The entry does authenticate users | Model artifact: exposed yes, but login is enforced |
| 2 | bank-of-anthos | Plaintext channel | FE_to_LedgerWriter | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | bank-of-anthos/kubernetes-manifests/config.yaml:28 `TRANSACTIONS_API_ADDR: ledgerwriter:8080`; `bank-of-anthos/src/frontend/frontend.py:662` `'http://{}/transactions'` | Confirmed: plain HTTP |
| 3 | bank-of-anthos | Plaintext channel | FE_to_BalanceReader | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | bank-of-anthos/kubernetes-manifests/config.yaml:29 `BALANCES_API_ADDR: balancereader:8080`; `bank-of-anthos/src/frontend/frontend.py` builds `http://` URIs | Confirmed: plain HTTP |
| 4 | bank-of-anthos | Plaintext channel | FE_to_TransactionHistory | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | bank-of-anthos/kubernetes-manifests/config.yaml:30 `HISTORY_API_ADDR: transactionhistory:8080`; `bank-of-anthos/src/frontend/frontend.py` builds `http://` URIs | Confirmed: plain HTTP |
| 5 | bank-of-anthos | Insufficient replicas | frontend | `Availability` rule targets it and it runs one copy | bank-of-anthos/kubernetes-manifests/frontend.yaml:38 (no `replicas` field, Kubernetes default 1) | Confirmed: single copy |
| 6 | hotel-reservation | Unauthenticated entry | frontend | exposed component and no `Authentication` rule targets it | dsb/hotelReservation/docker-compose.yml:30 `- "5000:5000"`; `hotel-reservation/hotelReservation/services/frontend/server.go:99,104,356,408`: `/user` and `/reservation` use `CheckUser`, search and recommendations are open | Partial: exposed, login on some routes |
| 7 | hotel-reservation | Insufficient replicas | frontend | `Availability` rule targets it and it runs one copy | dsb/hotelReservation/docker-compose.yml:35 `replicas: 1` | Confirmed: single copy |
| 8 | hotel-reservation | Insufficient replicas | reservation | `Availability` rule targets it and it runs one copy | dsb/hotelReservation/docker-compose.yml:217 `replicas: 1` | Confirmed: single copy |
| 9 | hotel-reservation | Insufficient replicas | mongodb-reservation | `Availability` rule targets it and it runs one copy | dsb/hotelReservation/docker-compose.yml:368 `replicas: 1` | Confirmed: single copy |
| 10 | hotel-reservation | Insufficient replicas | memcached-reserve | `Availability` rule targets it and it runs one copy | dsb/hotelReservation/docker-compose.yml:291 `replicas: 1` | Confirmed: single copy |
| 11 | online-boutique | Unauthenticated entry | frontend | exposed component and no `Authentication` rule targets it | online-boutique/release/kubernetes-manifests.yaml:136 `type: LoadBalancer` (Service frontend-external); no login code in `src/frontend` (grep 'login' finds nothing) | Confirmed |
| 12 | online-boutique | Plaintext channel | Checkout_to_Payment | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | online-boutique/release/kubernetes-manifests.yaml:651-652 `PAYMENT_SERVICE_ADDR: paymentservice:50051`; `online-boutique/src/checkoutservice/main.go:215` `insecure.NewCredentials()`; `online-boutique/src/paymentservice/server.js:62` `createInsecure()` | Confirmed: gRPC without TLS |
| 13 | online-boutique | Insufficient replicas | frontend | `Availability` rule targets it and it runs one copy | online-boutique/release/kubernetes-manifests.yaml:22 (no `replicas` field, Kubernetes default 1) | Confirmed: single copy |
| 14 | online-boutique | Insufficient replicas | checkoutservice | `Availability` rule targets it and it runs one copy | online-boutique/release/kubernetes-manifests.yaml:606 (no `replicas` field, Kubernetes default 1) | Confirmed: single copy |
| 15 | opentelemetry-demo | Unauthenticated entry | frontend-proxy | exposed component and no `Authentication` rule targets it | opentelemetry-demo/compose.yaml:328 `${ENVOY_PORT}:${ENVOY_PORT}`; no login or password code in `src/frontend/pages` | Confirmed |
| 16 | opentelemetry-demo | Plaintext channel | Checkout_to_Payment | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | opentelemetry-demo/compose.yaml:136 `PAYMENT_ADDR`; `opentelemetry-demo/src/checkout/main.go:467` `insecure.NewCredentials()` | Confirmed: gRPC without TLS |
| 17 | opentelemetry-demo | Insufficient replicas | frontend-proxy | `Availability` rule targets it and it runs one copy | opentelemetry-demo/compose.yaml:314 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 18 | opentelemetry-demo | Insufficient replicas | frontend | `Availability` rule targets it and it runs one copy | opentelemetry-demo/compose.yaml:247 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 19 | opentelemetry-demo | Insufficient replicas | checkout | `Availability` rule targets it and it runs one copy | opentelemetry-demo/compose.yaml:114 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 20 | social-network | Isolation violated | user-mongodb via user-mention-service | the rule approves only the account services as mediators, but a second service reads the user store and is reachable from the entry | social-network/socialNetwork/src/UserMentionService/UserMentionService.cpp:45 reads `user-mongodb`; `social-network/socialNetwork/src/TextService/TextService.cpp:34` calls `user-mention-service`; `social-network/socialNetwork/src/ComposePostService/ComposePostService.cpp` calls `text-service` | Confirmed: shared user store |
| 21 | social-network | Unauthenticated entry | nginx-thrift | exposed component and no `Authentication` rule targets it | dsb/socialNetwork/docker-compose.yml:253 `- 8080:8080`; `social-network/socialNetwork/nginx-web-server/lua-scripts/api/user/login.lua` exists (login for some APIs, others anonymous) | Partial: exposed, login on some routes |
| 22 | social-network | Unauthenticated entry | media-frontend | exposed component and no `Authentication` rule targets it | dsb/socialNetwork/docker-compose.yml:270 `- 8081:8080`; `media-frontend/lua-scripts/*.lua`: no token, login or auth code | Confirmed |
| 23 | social-network | Insufficient replicas | nginx-thrift | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:249 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 24 | social-network | Insufficient replicas | media-frontend | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:266 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 25 | social-network | Insufficient replicas | compose-post-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:39 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 26 | social-network | Insufficient replicas | text-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:197 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 27 | social-network | Insufficient replicas | unique-id-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:210 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 28 | social-network | Insufficient replicas | user-mention-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:223 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 29 | social-network | Insufficient replicas | url-shorten-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:110 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 30 | social-network | Insufficient replicas | url-shorten-mongodb | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:132 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 31 | social-network | Insufficient replicas | post-storage-service | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:52 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 32 | social-network | Insufficient replicas | post-storage-mongodb | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:74 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 33 | social-network | Insufficient replicas | post-storage-memcached | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:67 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 34 | social-network | Insufficient replicas | url-shorten-memcached | `Availability` rule targets it and it runs one copy | dsb/socialNetwork/docker-compose.yml:125 (service has no `replicas`, compose default 1) | Confirmed: single copy |
| 35 | sock-shop | Isolation violated | session-db -> front-end | the entry point reaches the session store directly, not through the cart service that owns it | sock-shop/deploy/kubernetes/complete-demo.yaml:279-280 `SESSION_REDIS: "true"` on `front-end`; `session-db` Service in the same file | By design: the front-end really talks to its session store |
| 36 | sock-shop | Unauthenticated entry | front-end | exposed component and no `Authentication` rule targets it | sock-shop/deploy/kubernetes/complete-demo.yaml:313 `type: NodePort`; `sock-shop/front-end/api/endpoints.js:25` has `loginUrl` (login exists, catalogue is anonymous) | Partial: exposed, login on some routes |
| 37 | sock-shop | Plaintext channel | Orders_to_Payment | a `Confidentiality` rule covers the path and the connector protocol is `http`/`grpc` | `sock-shop/orders/src/main/java/works/weave/socks/orders/config/OrdersConfigurationProperties.java:12,73` builds `"http://" + host` for `/paymentAuth`; `sock-shop/payment/cmd/paymentsvc/main.go` uses `ListenAndServe` (no TLS) | Confirmed: plain HTTP |
| 38 | sock-shop | Insufficient replicas | front-end | `Availability` rule targets it and it runs one copy | sock-shop/deploy/kubernetes/complete-demo.yaml:257 `replicas: 1` | Confirmed: single copy |
| 39 | sock-shop | Insufficient replicas | orders | `Availability` rule targets it and it runs one copy | sock-shop/deploy/kubernetes/complete-demo.yaml:329 `replicas: 1` | Confirmed: single copy |
| 40 | sock-shop | Insufficient replicas | orders-db | `Availability` rule targets it and it runs one copy | sock-shop/deploy/kubernetes/complete-demo.yaml:397 `replicas: 1` | Confirmed: single copy |
| 41 | sock-shop | Insufficient replicas | queue-master | `Availability` rule targets it and it runs one copy | sock-shop/deploy/kubernetes/complete-demo.yaml:524 `replicas: 1` | Confirmed: single copy |
| 42 | sock-shop | Insufficient replicas | rabbitmq | `Availability` rule targets it and it runs one copy | sock-shop/deploy/kubernetes/complete-demo.yaml:576 `replicas: 1` | Confirmed: single copy |
| 43 | teastore | Authentication bypass | webui -> persistence | a path from webui reaches persistence without crossing `teastore-auth` | `teastore/services/tools.descartes.teastore.webui/src/main/java/tools/descartes/teastore/webui/servlet/CartServlet.java:31` uses `LoadBalancedCRUDOperations` (persistence) directly; `teastore/services/tools.descartes.teastore.webui/src/main/java/tools/descartes/teastore/webui/startup/WebuiStartup.java:55`; no auth code in the persistence service | Confirmed: persistence is reached with no auth hop |
| 44 | teastore | Unauthenticated entry | teastore-webui | exposed component and no `Authentication` rule targets it | teastore/examples/kubernetes/teastore-clusterip.yaml:291 `type: NodePort`; `teastore/services/tools.descartes.teastore.webui/src/main/java/tools/descartes/teastore/webui/servlet/LoginActionServlet.java` exists in webui (login for orders, browsing anonymous) | Partial: exposed, login on some routes |
| 45 | teastore | Insufficient replicas | teastore-webui | `Availability` rule targets it and it runs one copy | teastore/examples/kubernetes/teastore-clusterip.yaml:255 (no `replicas` field, Kubernetes default 1) | Confirmed: single copy |

Totals: 45 findings. By design 1, Confirmed 39, Model artifact 1, Partial 4.

## 5. What the check shows about the tool

- The single-copy findings (28) are true but rubric-driven: the shipped manifests run one replica (the evidence column shows an explicit `replicas: 1` or the absence of the field, which means the default of 1).
- 8 unauthenticated-entry findings: 3 are Confirmed (no login code), 4 are Partial (the app has login on some routes), 1 is a Model artifact (Bank of Anthos: its frontend redirects to /login, the model cannot express a login built into the entry). The check reports exposure without a rule, it cannot see login built into the app.
- Plaintext channel: all 6 are Confirmed in code (insecure gRPC credentials or `http://`).
- Authentication bypass: TeaStore is Confirmed. Bank of Anthos is no longer reported: its backends verify the JWT themselves, which the tool now understands through a shared credential (`jwt-key`, mounted by userservice and the 5 verifiers in the manifests).
- Isolation: every system now states the multi-hop form of the rule (the store is reachable from the entry only through its own domain, `via`). 5 systems hold the design (silent). Sock Shop fires on a direct path the app needs (its session store). Social Network fires because a second service (`user-mention-service`) reads the user store.

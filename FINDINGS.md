# Findings, verified against the source repos

All 7 systems cloned and checked against the repo files. Every path below is
the real repo path. Manifests: `real-systems/inputs/manifests/`. Cited
source files: `real-systems/inputs/evidence/`. Tool version and reproduce
steps: `tool/README.md`.

## 1. Repos checked

| System | Repo | Commit | Ground-truth file |
| --- | --- | --- | --- |
| bank-of-anthos | GoogleCloudPlatform/bank-of-anthos | 1e40564f | `kubernetes-manifests/*.yaml` (10 files) |
| hotel-reservation | delimitrou/DeathStarBench | 6ecb097 | `hotelReservation/docker-compose.yml` |
| online-boutique | GoogleCloudPlatform/microservices-demo | 9a4616e7 | `release/kubernetes-manifests.yaml` |
| opentelemetry-demo | open-telemetry/opentelemetry-demo | f7408a5 | `compose.yaml` |
| social-network | delimitrou/DeathStarBench | 6ecb097 | `socialNetwork/docker-compose.yml` |
| sock-shop | microservices-demo/microservices-demo + 8 service repos | 9dff06f | `deploy/kubernetes/complete-demo.yaml` |
| teastore | DescartesResearch/TeaStore | 34b37f7 | `examples/kubernetes/teastore-clusterip.yaml` |

All 7 ground-truth files vendored verbatim under `real-systems/inputs/manifests/`.
Sock Shop service repos used for source checks (commit): carts f4e8005
catalogue 925e08e front-end 52dee65 orders 546a10c payment 384e334
queue-master 7dc3372 shipping 9c0fbfa user e1a79e7.

How git becomes `.arch.yaml`/`.secdsl`, and the model-vs-repo check counts:
`METHODOLOGY.md`.

## 2. The findings

Verdict key: **Confirmed** = true in the repo. **Partial** = exposure true, app has a login on some routes. **Model artifact** = true in the model, not in the app. **By design** = real path, intended by the app. Replicas findings exist because the rubric asks for >=2 copies (`Availability medium`).

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

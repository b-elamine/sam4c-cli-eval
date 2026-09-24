# Source-code evidence

Every finding that cites a line of service source code (not a deployment
manifest) in `../../../FINDINGS.md` has that exact file vendored here, at its
real path inside the upstream repo. Same bytes, same path, nothing edited.

Manifests (the deployment files) are in `../manifests/`, not here. This
folder is only for the service source code checked when a manifest alone
did not settle a finding.

| File here | Real repo | Cited in FINDINGS.md row |
|---|---|---|
| `bank-of-anthos/src/frontend/frontend.py` | GoogleCloudPlatform/bank-of-anthos | 1, 2, 3, 4 |
| `hotel-reservation/hotelReservation/services/frontend/server.go` | delimitrou/DeathStarBench | 6 |
| `online-boutique/src/checkoutservice/main.go` | GoogleCloudPlatform/microservices-demo | 12 |
| `online-boutique/src/paymentservice/server.js` | GoogleCloudPlatform/microservices-demo | 12 |
| `opentelemetry-demo/src/checkout/main.go` | open-telemetry/opentelemetry-demo | 16 |
| `social-network/socialNetwork/src/UserMentionService/UserMentionService.cpp` | delimitrou/DeathStarBench | 20 |
| `social-network/socialNetwork/src/TextService/TextService.cpp` | delimitrou/DeathStarBench | 20 |
| `social-network/socialNetwork/src/ComposePostService/ComposePostService.cpp` | delimitrou/DeathStarBench | 20 |
| `social-network/socialNetwork/nginx-web-server/lua-scripts/api/user/login.lua` | delimitrou/DeathStarBench | 21 |
| `sock-shop/front-end/api/endpoints.js` | microservices-demo/front-end | 36 |
| `sock-shop/orders/src/main/java/works/weave/socks/orders/config/OrdersConfigurationProperties.java` | microservices-demo/orders | 37 |
| `sock-shop/payment/cmd/paymentsvc/main.go` | microservices-demo/payment | 37 |
| `teastore/.../webui/servlet/CartServlet.java` | DescartesResearch/TeaStore | 43 |
| `teastore/.../webui/startup/WebuiStartup.java` | DescartesResearch/TeaStore | 43 |
| `teastore/.../webui/servlet/LoginActionServlet.java` | DescartesResearch/TeaStore | 44 |

Exact commits are in `FINDINGS.md` section 1 (Sock Shop's constituent
service repos, e.g. `orders`, `payment`, `front-end`, are listed separately
there since Sock Shop is assembled from 8 independent repos, not one).

An earlier version of `FINDINGS.md` cited some of these with a shortened or
bare-filename path (e.g. `webui/.../CartServlet.java`, or `TextService.cpp`
with no path at all). That's fixed: every citation in `FINDINGS.md` now
gives the real path, matching what's vendored here exactly.

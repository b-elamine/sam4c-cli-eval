# Model inventory

Every modeled component. Full per-finding evidence: `findings-explained.md`.

| System | Component | Type | Domain | Exposure | Persistent | Credentials |
|---|---|---|---|---|---|---|
| BoA | K8sCluster | Worker |  |  |  |  |
| BoA | frontend | App | frontend | external |  | jwt-key |
| BoA | userservice | App | accounts | internal |  | jwt-key |
| BoA | contacts | App | accounts | internal |  | jwt-key |
| BoA | accounts-db | Data | accounts | internal | False |  |
| BoA | ledgerwriter | App | ledger | internal |  | jwt-key |
| BoA | balancereader | App | ledger | internal |  | jwt-key |
| BoA | transactionhistory | App | ledger | internal |  | jwt-key |
| BoA | ledger-db | Data | ledger | internal | False |  |
| BoA | loadgenerator | App | observability | internal |  |  |
| HR | K8sCluster | Worker |  |  |  |  |
| HR | consul | App | platform | internal |  |  |
| HR | frontend | App | frontend | external |  |  |
| HR | search | App | search | internal |  |  |
| HR | geo | App | search | internal |  |  |
| HR | mongodb-geo | Data | search | internal | True |  |
| HR | rate | App | search | internal |  |  |
| HR | mongodb-rate | Data | search | internal | True |  |
| HR | profile | App | profile | internal |  |  |
| HR | mongodb-profile | Data | profile | internal | True |  |
| HR | recommendation | App | recommendation | internal |  |  |
| HR | mongodb-recommendation | Data | recommendation | internal | True |  |
| HR | user | App | account | internal |  |  |
| HR | mongodb-user | Data | account | internal | True |  |
| HR | reservation | App | reservation | internal |  |  |
| HR | mongodb-reservation | Data | reservation | internal | True |  |
| HR | attractions | App | attractions | internal |  |  |
| HR | review | App | review | internal |  |  |
| HR | mongodb-attractions | Data | attractions | internal | True |  |
| HR | mongodb-review | Data | review | internal | True |  |
| HR | memcached-profile | Data | profile | internal | False |  |
| HR | memcached-rate | Data | search | internal | False |  |
| HR | memcached-reserve | Data | reservation | internal | False |  |
| HR | memcached-review | Data | review | internal | False |  |
| HR | jaeger | App | observability | internal |  |  |
| OB | K8sCluster | Worker |  |  |  |  |
| OB | frontend | App | frontend | external |  |  |
| OB | adservice | App | ads | internal |  |  |
| OB | currencyservice | App | currency | internal |  |  |
| OB | cartservice | App | cart | internal |  |  |
| OB | redis-cart | Data | cart | internal | False |  |
| OB | recommendationservice | App | recommendation | internal |  |  |
| OB | checkoutservice | App | checkout | internal |  |  |
| OB | emailservice | App | email | internal |  |  |
| OB | paymentservice | App | payment | internal |  |  |
| OB | shippingservice | App | shipping | internal |  |  |
| OB | productcatalogservice | App | catalog | internal |  |  |
| OB | loadgenerator | App | observability | internal |  |  |
| OTel | K8sCluster | Worker |  |  |  |  |
| OTel | frontend-proxy | App | frontend | external |  |  |
| OTel | frontend | App | frontend | internal |  |  |
| OTel | ad | App | ads | internal |  |  |
| OTel | cart | App | cart | internal |  |  |
| OTel | valkey-cart | Data | cart | internal | False |  |
| OTel | checkout | App | checkout | internal |  |  |
| OTel | currency | App | currency | internal |  |  |
| OTel | email | App | email | internal |  |  |
| OTel | payment | App | payment | internal |  |  |
| OTel | product-catalog | App | catalog | internal |  |  |
| OTel | astronomy-db | Data | catalog | internal | False |  |
| OTel | quote | App | shipping | internal |  |  |
| OTel | recommendation | App | catalog | internal |  |  |
| OTel | shipping | App | shipping | internal |  |  |
| OTel | image-provider | App | media | internal |  |  |
| OTel | flagd | App | observability | internal |  |  |
| OTel | flagd-ui | App | observability | internal |  |  |
| OTel | load-generator | App | observability | internal |  |  |
| OTel | otel-collector | App | observability | internal |  |  |
| OTel | telemetry-docs | App | observability | internal |  |  |
| SN | K8sCluster | Worker |  |  |  |  |
| SN | nginx-thrift | App | frontend | external |  |  |
| SN | media-frontend | App | frontend | external |  |  |
| SN | compose-post-service | App | post | internal |  |  |
| SN | text-service | App | post | internal |  |  |
| SN | unique-id-service | App | post | internal |  |  |
| SN | user-mention-service | App | post | internal |  |  |
| SN | media-service | App | media | internal |  |  |
| SN | media-mongodb | Data | media | internal | False |  |
| SN | url-shorten-service | App | post | internal |  |  |
| SN | url-shorten-mongodb | Data | post | internal | False |  |
| SN | post-storage-service | App | post | internal |  |  |
| SN | post-storage-mongodb | Data | post | internal | False |  |
| SN | user-timeline-service | App | timeline | internal |  |  |
| SN | user-timeline-mongodb | Data | timeline | internal | False |  |
| SN | social-graph-service | App | social | internal |  |  |
| SN | social-graph-mongodb | Data | social | internal | False |  |
| SN | user-service | App | account | internal |  |  |
| SN | user-mongodb | Data | account | internal | False |  |
| SN | home-timeline-service | App | timeline | internal |  |  |
| SN | home-timeline-redis | Data | timeline | internal | False |  |
| SN | social-graph-redis | Data | social | internal | False |  |
| SN | user-timeline-redis | Data | timeline | internal | False |  |
| SN | media-memcached | Data | media | internal | False |  |
| SN | post-storage-memcached | Data | post | internal | False |  |
| SN | url-shorten-memcached | Data | post | internal | False |  |
| SN | user-memcached | Data | account | internal | False |  |
| SN | jaeger-agent | App | observability | internal |  |  |
| SS | K8sCluster | Worker |  |  |  |  |
| SS | front-end | App | frontend | external |  |  |
| SS | catalogue | App | catalog | internal |  |  |
| SS | catalogue-db | Data | catalog | internal | False |  |
| SS | carts | App | cart | internal |  |  |
| SS | carts-db | Data | cart | internal | False |  |
| SS | orders | App | orders | internal |  |  |
| SS | orders-db | Data | orders | internal | False |  |
| SS | payment | App | payment | internal |  |  |
| SS | shipping | App | shipping | internal |  |  |
| SS | queue-master | App | orders | internal |  |  |
| SS | rabbitmq | App | orders | internal |  |  |
| SS | session-db | Data | cart | internal | False |  |
| SS | user | App | user | internal |  |  |
| SS | user-db | Data | user | internal | False |  |
| TS | K8sCluster | Worker |  |  |  |  |
| TS | teastore-registry | App | platform | internal |  |  |
| TS | teastore-db | Data | catalog | internal | False |  |
| TS | teastore-persistence | App | data | internal |  |  |
| TS | teastore-auth | App | auth | internal |  |  |
| TS | teastore-image | App | catalog | internal |  |  |
| TS | teastore-recommender | App | catalog | internal |  |  |
| TS | teastore-webui | App | frontend | external |  |  |
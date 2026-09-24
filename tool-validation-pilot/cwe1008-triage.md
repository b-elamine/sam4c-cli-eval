# CWE-1008 (Architectural Concepts) - full triage

Fetched from MITRE CWE-1008 (12 categories, all member weaknesses). Each weakness classified:

- **Scope**: IN = representable in the architecture model and fixable by changing the deployment
  design/config (not code); OUT = code / app / runtime (fixable only by changing a component).
- **Verdict**: `covered c#` (a check addresses it), `covered~ c#` (partial), `gap(area)` (IN, no
  check yet), `out(why)`.
- `(review)` = borderline; verify against the CWE's "Modes of Introduction" field before trusting.

This is my first-pass classification (knowledge + the fix-test). YOU verify, especially the
`(review)` rows and any gap/out call you disagree with. Counts at the bottom.

Our checks: c1 Availability, c2 Isolation, c3 missing-auth, c4 exposed-data, c5 accidental-exposure,
c6 authz-without-authn, c7 isolation-vs-communication.

---

## CWE-1009 Audit  (logging/audit - not represented in our model)
| CWE | Name                                      | Scope | Verdict                                          |
| --- | ----------------------------------------- | ----- | ------------------------------------------------ |
| 117 | Improper Output Neutralization for Logs   | OUT   | out(log injection, code)                         |
| 223 | Omission of Security-relevant Information | OUT   | out(audit not modeled) (review)                  |
| 224 | Obscured Security-relevant Information    | OUT   | out(audit not modeled)                           |
| 532 | Sensitive Information into Log File       | OUT   | out(code/logging)                                |
| 778 | Insufficient Logging                      | OUT   | out(audit not modeled; future modeling) (review) |
| 779 | Logging of Excessive Data                 | OUT   | out(logging)                                     |

## CWE-1010 Authenticate Actors
| CWE | Name                                         | Scope | Verdict                                      |
| --- | -------------------------------------------- | ----- | -------------------------------------------- |
| 258 | Empty Password in Configuration File         | IN    | gap(secrets)                                 |
| 259 | Use of Hard-coded Password                   | IN    | gap(secrets)                                 |
| 262 | Not Using Password Aging                     | OUT   | out(app policy)                              |
| 263 | Password Aging Long Expiration               | OUT   | out(app policy)                              |
| 287 | Improper Authentication                      | IN    | covered~ c3 (review: broader than "missing") |
| 288 | Auth Bypass Alternate Path/Channel           | IN    | gap(unprotected channel) (review)            |
| 289 | Auth Bypass by Alternate Name                | OUT   | out(auth logic)                              |
| 290 | Auth Bypass by Spoofing                      | OUT   | out(auth logic)                              |
| 291 | Reliance on IP Address for Auth              | OUT   | out(auth mechanism) (review)                 |
| 293 | Using Referer for Auth                       | OUT   | out(code)                                    |
| 294 | Auth Bypass Capture-replay                   | OUT   | out(protocol/code)                           |
| 301 | Reflection Attack in Auth                    | OUT   | out(protocol)                                |
| 302 | Bypass by Assumed-Immutable Data             | OUT   | out(code)                                    |
| 303 | Incorrect Impl of Auth Algorithm             | OUT   | out(code)                                    |
| 304 | Missing Critical Step in Auth                | OUT   | out(code)                                    |
| 305 | Bypass by Primary Weakness                   | OUT   | out(code)                                    |
| 306 | Missing Authentication for Critical Function | IN    | covered c3                                   |
| 307 | Excessive Authentication Attempts            | OUT   | out(app)                                     |
| 308 | Use of Single-factor Authentication          | OUT   | out(auth strength) (review)                  |
| 322 | Key Exchange without Entity Auth             | OUT   | out(crypto/protocol)                         |
| 521 | Weak Password Requirements                   | OUT   | out(app policy)                              |
| 593 | OpenSSL CTX Modified                         | OUT   | out(code)                                    |
| 603 | Use of Client-Side Authentication            | IN    | gap(enforcement location) (review)           |
| 620 | Unverified Password Change                   | OUT   | out(app)                                     |
| 640 | Weak Password Recovery                       | OUT   | out(app)                                     |
| 798 | Use of Hard-coded Credentials                | IN    | gap(secrets)                                 |
| 836 | Password Hash Instead of Password            | OUT   | out(code)                                    |
| 916 | Password Hash Insufficient Effort            | OUT   | out(crypto/code)                             |

## CWE-1011 Authorize Actors  (the richest category for us)
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 114 | Process Control | OUT | out(code) |
| 15 | External Control of Config Setting | OUT | out(code) (review) |
| 219 | Sensitive File Under Web Root | IN | gap(exposure) |
| 220 | Sensitive File Under FTP Root | IN | gap(exposure) |
| 266 | Incorrect Privilege Assignment | IN | gap(least-privilege) |
| 267 | Privilege With Unsafe Actions | IN | gap(least-privilege) |
| 268 | Privilege Chaining | IN | gap(least-privilege) (review) |
| 269 | Improper Privilege Management | IN | gap(least-privilege) |
| 270 | Privilege Context Switching Error | OUT | out(code) |
| 271 | Privilege Dropping Errors | OUT | out(code) |
| 272 | Least Privilege Violation | IN | gap(least-privilege) |
| 273 | Improper Check for Dropped Privileges | OUT | out(code) |
| 274 | Improper Handling Insufficient Privileges | OUT | out(code) |
| 276 | Incorrect Default Permissions | IN | gap(permissions/least-priv) |
| 277 | Insecure Inherited Permissions | IN | gap(permissions) |
| 279 | Incorrect Execution-Assigned Permissions | OUT | out(runtime) (review) |
| 280 | Improper Handling Insufficient Permissions | OUT | out(code) |
| 281 | Improper Preservation of Permissions | OUT | out(code) |
| 282 | Improper Ownership Management | OUT | out(code) (review) |
| 283 | Unverified Ownership | OUT | out(code) |
| 284 | Improper Access Control | IN | covered~ c2/c6 (broad parent) (review) |
| 285 | Improper Authorization | IN | covered~ c6 (review) |
| 286 | Incorrect User Management | OUT | out(app) |
| 300 | Channel Accessible by Non-Endpoint (MITM) | IN | gap(channel confidentiality) |
| 341 | Predictable from Observable State | OUT | out(code) |
| 359 | Exposure of Private Personal Info | IN | gap(exposure/privacy) |
| 403 | Exposure of File Descriptor | OUT | out(runtime) |
| 419 | Unprotected Primary Channel | IN | covered~ c5 (review) |
| 420 | Unprotected Alternate Channel | IN | gap(exposure) |
| 425 | Direct Request (Forced Browsing) | OUT | out(app) |
| 426 | Untrusted Search Path | OUT | out(code/runtime) |
| 434 | Unrestricted Upload of Dangerous Type | OUT | out(app) |
| 527 | Exposure of Version-Control Repo | IN | gap(exposure) |
| 528 | Exposure of Core Dump File | IN | gap(exposure) |
| 529 | Exposure of ACL Files | IN | gap(exposure) |
| 530 | Exposure of Backup File | IN | gap(exposure) |
| 538 | Sensitive Info in Externally-Accessible File | IN | gap(exposure) |
| 551 | Authorization Before Parsing/Canonicalization | OUT | out(code) |
| 552 | Files/Directories Accessible to External Parties | IN | covered~ c4 |
| 566 | Authz Bypass User-Controlled SQL Key | OUT | out(code) |
| 639 | Authz Bypass User-Controlled Key | OUT | out(code) |
| 642 | External Control of Critical State Data | OUT | out(code) |
| 647 | Non-Canonical URL for Authz | OUT | out(code) |
| 653 | Improper Isolation or Compartmentalization | IN | covered c2 |
| 656 | Reliance on Security Through Obscurity | OUT | out(design principle, not modelable) (review) |
| 668 | Exposure of Resource to Wrong Sphere | IN | covered c2/c4/c5 |
| 669 | Incorrect Resource Transfer Between Spheres | IN | gap(exposure/isolation) |
| 671 | Lack of Admin Control over Security | OUT | out(design) (review) |
| 673 | External Influence of Sphere Definition | OUT | out(code) |
| 708 | Incorrect Ownership Assignment | OUT | out(code) |
| 732 | Incorrect Permission for Critical Resource | IN | gap(permissions/least-priv) |
| 770 | Allocation of Resources Without Limits/Throttling | IN | covered~ c1 (resource limits) |
| 782 | Exposed IOCTL with Insufficient Access Control | OUT | out(runtime) |
| 827 | Improper Control of DTD | OUT | out(code) |
| 862 | Missing Authorization | IN | covered c6 |
| 863 | Incorrect Authorization | IN | gap(finer-grained authz) |
| 921 | Storage of Sensitive Data without Access Control | IN | covered~ c4 |
| 923 | Improper Restriction of Comm Channel to Endpoints | IN | covered~ c2/c5 |
| 939 | Improper Authz in Custom URL Scheme Handler | OUT | out(app) |
| 942 | Permissive Cross-domain Policy | IN | gap(exposure/access config) |

## CWE-1012 Cross Cutting  (mostly code)
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 208 | Observable Timing Discrepancy | OUT | out(side-channel/code) |
| 392 | Missing Report of Error Condition | OUT | out(code) |
| 460 | Improper Cleanup on Thrown Exception | OUT | out(code) |
| 544 | Missing Standardized Error Handling | OUT | out(code) |
| 602 | Client-Side Enforcement of Server-Side Security | IN | gap(enforcement location) (review) |
| 703 | Improper Check/Handling of Exceptional Conditions | OUT | out(code) |
| 754 | Improper Check for Unusual Conditions | OUT | out(code) |
| 784 | Reliance on Cookies without Integrity (security decision) | OUT | out(code) |
| 807 | Reliance on Untrusted Inputs in Security Decision | OUT | out(code) |

## CWE-1013 Encrypt Data
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 256 | Plaintext Storage of a Password | IN | gap(secrets/encryption-at-rest) |
| 257 | Storing Passwords in Recoverable Format | IN | gap(secrets) |
| 260 | Password in Configuration File | IN | gap(secrets) |
| 261 | Weak Encoding for Password | OUT | out(code) |
| 311 | Missing Encryption of Sensitive Data | IN | gap(Confidentiality) |
| 312 | Cleartext Storage of Sensitive Information | IN | gap(encryption-at-rest) |
| 313 | Cleartext Storage in File/Disk | IN | gap(encryption-at-rest) |
| 314 | Cleartext Storage in Registry | IN | gap(encryption-at-rest) (review) |
| 315 | Cleartext Storage in a Cookie | OUT | out(app) |
| 316 | Cleartext Storage in Memory | OUT | out(runtime) |
| 317 | Cleartext Storage in GUI | OUT | out(app) |
| 318 | Cleartext Storage in Executable | OUT | out(code) |
| 319 | Cleartext Transmission of Sensitive Information | IN | gap(Confidentiality channel) |
| 321 | Use of Hard-coded Cryptographic Key | IN | gap(secrets) |
| 323 | Reusing a Nonce / Key Pair | OUT | out(crypto/code) |
| 324 | Use of Key Past Expiration | OUT | out(crypto/ops) (review) |
| 325 | Missing Cryptographic Step | OUT | out(code) |
| 326 | Inadequate Encryption Strength | OUT | out(crypto strength) (review) |
| 327 | Broken or Risky Crypto Algorithm | OUT | out(crypto) |
| 328 | Use of Weak Hash | OUT | out(crypto) |
| 330 | Use of Insufficiently Random Values | OUT | out(code) |
| 331 | Insufficient Entropy | OUT | out(code) |
| 332 | Insufficient Entropy in PRNG | OUT | out(code) |

## CWE-1014 Identify Actors  (certificate / channel-source validation - mostly code)
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 295 | Improper Certificate Validation | OUT | out(TLS code) (review: could be config) |
| 296 | Improper Following of Cert Chain | OUT | out(code) |
| 297 | Cert with Host Mismatch | OUT | out(code) |
| 298 | Cert Expiration | OUT | out(code/ops) |
| 299 | Cert Revocation Check | OUT | out(code) |
| 345 | Insufficient Verification of Data Authenticity | OUT | out(Integrity, code) |
| 346 | Origin Validation Error | OUT | out(code) |
| 370 | Missing Cert Revocation after Initial Check | OUT | out(code) |
| 441 | Unintended Proxy/Intermediary (Confused Deputy) | OUT | out(code/design) (review) |
| 599 | Missing OpenSSL Cert Validation | OUT | out(code) |
| 940 | Improper Verification of Source of Channel | IN | gap(channel auth) (review) |
| 941 | Incorrectly Specified Destination in Channel | IN | gap(channel) (review) |

## CWE-1015 Limit Access
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 73 | External Control of File Name or Path | OUT | out(code) |
| 201 | Insertion of Sensitive Information Into Sent Data | IN | gap(exposure) (review) |
| 209 | Error Message Containing Sensitive Information | OUT | out(app) |
| 212 | Improper Removal of Sensitive Information | OUT | out(code) |
| 243 | chroot Jail Without Changing Working Dir | OUT | out(runtime) |
| 250 | Execution with Unnecessary Privileges | IN | gap(least-privilege) |
| 610 | Externally Controlled Reference to Resource in Another Sphere | IN | gap(exposure) (review: SSRF-ish) |
| 611 | Improper Restriction of XXE | OUT | out(code) |

## CWE-1016 Limit Exposure  (mostly error-message/code in CWE's grouping)
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 210 | Self-generated Error Message Sensitive Info | OUT | out(app) |
| 211 | Externally-Generated Error Message Sensitive | OUT | out(app) |
| 214 | Invocation of Process Using Visible Sensitive Info | IN | gap(secrets/exposure) (review) |
| 550 | Server-generated Error Message Sensitive | OUT | out(app) |
| 829 | Inclusion of Functionality from Untrusted Sphere | OUT | out(supply chain/code) |
| 830 | Inclusion of Web Functionality from Untrusted Source | OUT | out(code) |

## CWE-1017 Lock Computer
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 645 | Overly Restrictive Account Lockout | OUT | out(app) |

## CWE-1018 Manage User Sessions  (all app-level)
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 6 | J2EE Insufficient Session-ID Length | OUT | out(app) |
| 384 | Session Fixation | OUT | out(app) |
| 488 | Exposure of Data to Wrong Session | OUT | out(app) |
| 579 | J2EE Non-serializable in Session | OUT | out(code) |
| 613 | Insufficient Session Expiration | OUT | out(app) |
| 841 | Improper Enforcement of Behavioral Workflow | OUT | out(app) |

## CWE-1019 Validate Inputs  (ALL injection/input validation = code -> all OUT)
CWE-20, 59, 74, 75, 76, 77, 78, 79, 88, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 138, 150, 349, 352,
472, 473, 502, 601, 641, 643, 652, 790, 791, 792, 793, 794, 795, 796, 797, 943 -> all **OUT (code)**.
(38 weaknesses, none representable in the design model.)

## CWE-1020 Verify Message Integrity
| CWE | Name | Scope | Verdict |
|-----|------|-------|---------|
| 353 | Missing Support for Integrity Check | IN | gap(Integrity) |
| 354 | Improper Validation of Integrity Check Value | OUT | out(code) |
| 390 | Detection of Error Without Action | OUT | out(code) |
| 391 | Unchecked Error Condition | OUT | out(code) |
| 494 | Download of Code Without Integrity Check | IN | gap(supply chain / image integrity) |
| 565 | Reliance on Cookies without Integrity | OUT | out(code) |
| 649 | Reliance on Obfuscation without Integrity | OUT | out(code) |
| 707 | Improper Neutralization | OUT | out(code) |
| 755 | Improper Handling of Exceptional Conditions | OUT | out(code) |
| 924 | Improper Enforcement of Message Integrity in Transmission | IN | gap(Integrity channel) |

---

## Summary (first pass - verify)

- Total member weaknesses across CWE-1008: ~160.
- **IN-scope (design/config representable): ~45.** OUT-of-scope (code/app/runtime): ~115.
- Of the IN-scope:
  - **covered (a check addresses it): CWE-306, 862, 668, 653 (full); 287, 284, 285, 419, 552, 770,
    921, 923 (partial)** -> ~4 full + ~8 partial.
  - **gap (IN, no check yet):** clusters as -
    - secrets in config (258, 259, 260, 798, 321, 256, 257, 214) -> a Secrets property,
    - encryption at rest / transit (311, 312, 313, 314, 319) -> Confidentiality,
    - message integrity (353, 924, 494) -> Integrity,
    - least privilege / permissions (266, 267, 268, 269, 272, 276, 277, 732, 250) -> least-privilege authz,
    - finer-grained authorization (863) -> authz scope,
    - resource/file exposure (219, 220, 527, 528, 529, 530, 538, 359, 420, 669, 942, 201) -> exposure (some may be covered~ by exposed-data),
    - channel (300, 940, 941) -> channel confidentiality/auth.

### Two honest framings of the number
- **By in-scope coverage:** of ~45 design-level weaknesses, our 7 checks address ~12 (fully or
  partially); the rest are gaps in identified property areas (secrets, encryption, integrity,
  least-privilege, finer authz, more exposure).
- **By design-tactic:** of the 12 CWE-1008 tactics, we touch Authenticate Actors, Authorize Actors
  (the big one), and partially Limit Access/Exposure; we do not yet touch Encrypt Data, Verify
  Message Integrity, Identify Actors, Audit, Sessions, Validate Inputs, Lock Computer, Cross Cutting.

### To verify (your pass)
- Every `(review)` row (check the CWE's "Modes of Introduction" field: Architecture/Design or
  Operation -> likely IN; Implementation -> likely OUT).
- The covered~ (partial) calls: decide if our check really addresses it or it's a gap.
- Whether to count "covered~" as covered or gap in the headline number (be consistent).
- The exposure cluster (219/220/527-538/552/921): several are arguably covered by exposed-data;
  decide covered vs gap per row.

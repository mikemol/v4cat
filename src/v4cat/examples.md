# Examples — domain templates for the catalogue framework

This file sketches starter templates for several domains the
framework applies to — enough to begin cataloguing each, not
exhaustive coverage. The framework itself is domain-agnostic;
processors are one of several worked examples below, alongside
programming languages, cryptography, databases, file systems,
network protocols, mathematical structures, OS designs, and ML
architectures.

For each template:

- **What's catalogued** — the *objects* (specs in framework
  vocabulary).
- **Initial breaks to consider** — candidate Q-numbered or letter-
  labelled breaks. These are starting points; real cataloguing
  will surface more.
- **Lineage/descent structure** — how objects relate.
- **What the temporal axis is** — the privileged advancement
  coordinate (year of release, version number, paper-publication-
  year).
- **Likely tensions** — implementation-alignment concerns the
  domain forces.

## Contents

1. [Processor architectures](#1-processor-architectures)
2. [Programming languages](#2-programming-languages)
3. [Cryptographic primitives](#3-cryptographic-primitives)
4. [Database systems](#4-database-systems)
5. [File systems](#5-file-systems)
6. [Network protocols](#6-network-protocols)
7. [Mathematical structures](#7-mathematical-structures)
8. [Operating system designs](#8-operating-system-designs)
9. [Machine-learning architectures](#9-machine-learning-architectures)
10. [Cataloguing your own database schema](#10-cataloguing-your-own-database-schema)
11. [The shape that recurs](#11-the-shape-that-recurs)

---

## 1. Processor architectures

A well-developed application domain for the framework.

**Objects**: classic and modern processor specs. Examples include
8-bit micros (6502, 6800, 4004, 8080, 8051), 16/32-bit families
(68000-68030, 80186-80386, 80287-80387, 8087), embedded
controllers (AVR, MSP430), mainframes (System/360, System/360/67,
System/370, System/370/XA, IBM z16). Plus non-processor formal
systems used as foils: Brainfuck, lambda calculus.

**Initial breaks to consider**: paging model, interrupt
precedence, vector facility, modal specs (FPU rounding /
precision modes), agent-level versus spec-level distinctions
(coprocessor agents, multi-CPU shared memory), instruction
classification (JMP/BRANCH/JSR/RTS/HALT), cache substrate
state, privilege rings.

**Temporal axis**: year of release (with the chronological-vs-
catalogue-exposition split that the framework's `year` and
`catalogue_order` columns track).

**Primary lineage chains**: Motorola 68k family, Intel x86 family,
Intel x87 coprocessor family, IBM mainframe family, embedded
families (8051-derived, AVR-derived).

**Convergence signal**: late additions in a family (e.g., the
80287 against an already-developed x87 base, or 68030 against a
68k base, or System/370/XA against a System/370 base) tend to
contribute *zero new breaks* — only refinements of existing ones.
This is the convergence signal described in
[theory.md § 11](theory.md).

---

## 2. Programming languages

A natural domain for the framework, full of accumulating structural
distinctions and clean lineage.

### Initial breaks to consider

- **PL-Type-System**: static / dynamic / gradual / dependent.
  Refinements: Hindley-Milner inference, row polymorphism,
  higher-rank polymorphism, refinement types, dependent types.
  *Axis*: equivalential.
- **PL-Memory-Management**: manual / refcount / tracing GC /
  region-based / linear-types-managed.
  *Axis*: spatial + temporal.
- **PL-Concurrency**: threads + locks / actors / fibers / async-
  await / CSP / STM / data-parallel.
  *Axis*: parallel.
- **PL-Effects**: exceptions / monads / algebraic-effects /
  effect-types / capability-effects.
  *Axis*: temporal + equivalential.
- **PL-Evaluation-Strategy**: strict / lazy / call-by-need /
  call-by-name / call-by-push-value.
  *Axis*: temporal.
- **PL-Module-System**: modules-as-records / functor-based /
  trait-based / typeclass-based / namespace-based.
  *Axis*: spatial.
- **PL-Macro-System**: textual / hygienic / typed-syntactic /
  none.
  *Axis*: spatial.
- **PL-Object-Model**: class-based / prototype-based / structural /
  algebraic-records-only.
  *Axis*: spatial.

### Lineage / descent

Programming languages have rich lineage:

- ALGOL 60 → ALGOL 68 → Pascal → Modula → Ada → Eiffel
- LISP → Scheme → Common Lisp → Clojure
- ML → SML → Caml → OCaml → ReasonML
- ML → Haskell (via lazy ML)
- C → C++ → Rust (with breaks)
- C → Objective-C → Swift
- JavaScript → TypeScript

Lineage edges admit `descended-from` for explicit ancestry,
`influenced-by` for less-direct kinship.

### Temporal axis

Year of first stable release (or first major paper).

### Worked examples

```python
cat.introduce_object('algol-60', 'ALGOL 60', year=1960,
                     attrs={'family': 'algol-lineage'})
cat.introduce_object('pascal',   'Pascal',   year=1970,
                     attrs={'family': 'algol-lineage'},
                     lineage=[('algol-60', 'descended-from')])
cat.introduce_object('haskell',  'Haskell',  year=1990,
                     attrs={'family': 'ml-lineage'})

cat.introduce_break('PL-Type-System', 'Static type system',
                    axes=['equivalential'])
cat.witness('algol-60', 'PL-Type-System', 'origin')
cat.witness('haskell', 'PL-Type-System', 'refines')
cat.refine('PL-Type-System', 'haskell', 'hindley-milner-inference')
cat.refine('PL-Type-System', 'haskell', 'higher-rank-polymorphism')
```

### Likely tensions

- **T-evaluation-strategy-vs-effects**: lazy languages have
  semantic interactions with effects (exception ordering, IO
  ordering) that strict languages don't. The PL-Effects break
  may need refinements per evaluation strategy.
- **T-memory-vs-concurrency**: GC-based memory management
  interacts with thread-based concurrency (stop-the-world);
  refcount with data races. The two breaks aren't independent.

### Convergence

Programming language design has been somewhat convergent since
the late-1990s standards (ML / Haskell / Java / Python all
roughly stable in their structural choices). Modern languages
(Rust, Swift, Kotlin) refine existing breaks; few introduce
genuinely new structural primitives.

---

## 3. Cryptographic primitives

A domain with clean structural distinctions and active research,
suitable for cataloguing as new primitives are proposed.

### Initial breaks to consider

- **CR-Hardness-Assumption**: factoring / discrete-log / lattice /
  isogeny / hash-function-collision / random-oracle.
  *Axis*: equivalential (the assumption underwrites the
  equivalence between cryptographic and computational hardness).
- **CR-Security-Notion**: IND-CPA / IND-CCA1 / IND-CCA2 / EUF-CMA /
  forward-secrecy.
  *Axis*: equivalential.
- **CR-Quantum-Security**: pre-quantum / post-quantum / hybrid.
  *Axis*: equivalential.
- **CR-Side-Channel-Resistance**: vulnerable / constant-time /
  leakage-resistant / black-box.
  *Axis*: temporal (timing attacks happen along execution-time).
- **CR-Composability**: black-box / UC-secure / ROM / standard-
  model.
  *Axis*: meta.
- **CR-Atomicity**: synchronous / asynchronous / fair-exchange.
  *Axis*: temporal.

### Lineage / descent

- RSA → RSA-OAEP → RSA-PSS
- Diffie-Hellman → ECDH → X25519
- AES (Rijndael) → AES-NI / AES-GCM
- Lattice basis: NTRU → Kyber / ML-KEM
- Hash: MD5 → SHA-1 → SHA-2 → SHA-3 (Keccak)

### Temporal axis

Year of first publication (paper or RFC).

### Likely tensions

- **T-quantum-transition**: post-quantum candidates have larger
  key sizes; protocols designed for pre-quantum primitives may
  not accommodate. Many CR-Quantum-Security refinements
  needed.
- **T-side-channel-vs-performance**: constant-time
  implementations are often slower; performance-critical paths
  pressure for non-constant-time. Q-class breaks for performance
  might emerge.

### Worked examples

```python
cat.introduce_object('rsa', 'RSA',  year=1977,
                     attrs={'authors': 'Rivest-Shamir-Adleman',
                            'family': 'factoring-based'})
cat.introduce_object('aes', 'AES',  year=2001,
                     attrs={'family': 'block-cipher'})
cat.introduce_object('mlkem', 'ML-KEM (Kyber)', year=2024,
                     attrs={'family': 'lattice-based'})

cat.introduce_break('CR-Quantum-Security',
                    'Quantum-resistance class',
                    axes=['equivalential'])
cat.witness('rsa',    'CR-Quantum-Security', 'first-witness',
            notes='pre-quantum: vulnerable to Shor algorithm')
cat.witness('mlkem',  'CR-Quantum-Security', 'first-witness',
            notes='post-quantum: lattice-based')
```

---

## 4. Database systems

A domain with rich structural choices and ongoing innovation.

### Initial breaks to consider

- **DB-Consistency-Model**: serializable / strict-serializable /
  snapshot-isolation / read-committed / eventual / causal.
  *Axis*: temporal + equivalential.
- **DB-Partitioning**: hash / range / consistent-hash /
  geo-partitioning.
  *Axis*: spatial + parallel.
- **DB-Replication**: synchronous / asynchronous / quorum-based.
  *Axis*: temporal.
- **DB-Storage-Engine**: B-tree / LSM / row-store / column-store /
  hybrid.
  *Axis*: spatial.
- **DB-Transaction-Model**: ACID / BASE / 2PL / OCC / MVCC.
  *Axis*: temporal.
- **DB-Query-Language**: SQL / SPARQL / Cypher / KV / document.
  *Axis*: spatial.
- **DB-Scaling-Model**: scale-up / scale-out / serverless.
  *Axis*: parallel.

### Lineage / descent

- Codd RDM → Ingres / System R → Oracle / DB2 → PostgreSQL
- BigTable → Cassandra / HBase
- Dynamo → Riak / DynamoDB
- Spanner → CockroachDB / YugabyteDB
- LevelDB → RocksDB → many LSM-based stores
- MongoDB / CouchDB (document)

### Temporal axis

Year of first public release.

### Likely tensions

- **T-CAP-tradeoffs**: each consistency model + partitioning
  combination occupies a CAP-theorem position. The break
  combinations aren't independent.
- **T-storage-vs-query-pattern**: column-stores favour analytic
  queries; row-stores favour OLTP. Storage engine + query
  pattern co-vary.

### Worked examples

```python
cat.introduce_object('postgres', 'PostgreSQL', year=1996,
                     attrs={'family': 'postgres-lineage'})
cat.introduce_object('cassandra','Cassandra',  year=2008,
                     attrs={'family': 'dynamo-lineage'})
cat.introduce_object('cockroach','CockroachDB',year=2017,
                     attrs={'family': 'spanner-lineage'})

cat.introduce_break('DB-Consistency-Model', 'Consistency level',
                    axes=['temporal', 'equivalential'])
cat.witness('postgres',  'DB-Consistency-Model', 'first-witness',
            notes='snapshot-isolation by default; serializable optional')
cat.witness('cassandra', 'DB-Consistency-Model', 'first-witness',
            notes='eventual; tunable per-query')
cat.witness('cockroach', 'DB-Consistency-Model', 'first-witness',
            notes='strict-serializable via Paxos')
```

---

## 5. File systems

A relatively-bounded domain with clean structural distinctions.

### Initial breaks to consider

- **FS-Journaling**: none / metadata-only / full / log-structured.
  *Axis*: temporal.
- **FS-Snapshots**: none / copy-on-write / log-structured.
  *Axis*: temporal + spatial.
- **FS-Checksums**: none / metadata-only / data-and-metadata.
  *Axis*: equivalential.
- **FS-Allocation**: extent-based / block-based / inline.
  *Axis*: spatial.
- **FS-Concurrency-Model**: single-writer / multi-writer-via-lock /
  cluster-coherent.
  *Axis*: parallel.
- **FS-Compression**: per-file / per-block / transparent / none.
  *Axis*: spatial.
- **FS-Deduplication**: none / per-block / content-addressed.
  *Axis*: spatial.

### Lineage / descent

- ext2 → ext3 → ext4 (Linux)
- FAT → FAT32 → exFAT (Microsoft)
- HFS → HFS+ → APFS (Apple)
- NTFS → ReFS (Microsoft)
- ZFS (Sun)
- btrfs (Linux)

### Worked example

ZFS as a witness of multiple breaks at first arrival:

```python
cat.introduce_object('zfs', 'ZFS', year=2005,
                     attrs={'vendor': 'Sun', 'family': 'zfs'})
cat.introduce_break('FS-Snapshots', 'COW snapshots',
                    axes=['temporal', 'spatial'])
cat.witness('zfs', 'FS-Snapshots', 'origin')
cat.refine('FS-Snapshots', 'zfs', 'cow-trees',
           description='Copy-on-write at the block-pointer level')

cat.introduce_break('FS-Checksums', 'End-to-end checksums',
                    axes=['equivalential'])
cat.witness('zfs', 'FS-Checksums', 'origin')
```

---

## 6. Network protocols

A protocol-stack-shaped domain with clean composition.

### Initial breaks to consider

- **NP-Reliability**: best-effort / acked / persistent.
  *Axis*: temporal.
- **NP-Ordering**: arbitrary / per-stream / total.
  *Axis*: temporal.
- **NP-Encryption**: none / opportunistic / required.
  *Axis*: equivalential.
- **NP-Multiplexing**: single-stream / multiple-streams /
  bidirectional / out-of-band.
  *Axis*: parallel.
- **NP-Flow-Control**: none / per-stream / per-connection.
  *Axis*: temporal.
- **NP-Congestion-Control**: none / Reno / CUBIC / BBR / DCTCP.
  *Axis*: temporal.

### Lineage / descent

- IP → TCP / UDP
- TCP → TLS / SCTP
- HTTP/1.1 → HTTP/2 → HTTP/3 (over QUIC)
- TLS 1.0 → 1.2 → 1.3
- WireGuard, Noise

### Temporal axis

Year of first RFC / first deployment.

### Worked example

```python
cat.introduce_object('tcp',  'TCP',  year=1981, attrs={'family': 'ietf'})
cat.introduce_object('quic', 'QUIC', year=2021, attrs={'family': 'ietf'})

cat.introduce_break('NP-Multiplexing', 'Stream multiplexing',
                    axes=['parallel'])
cat.witness('tcp',  'NP-Multiplexing', 'first-witness',
            notes='single-stream per connection')
cat.witness('quic', 'NP-Multiplexing', 'refines',
            notes='multiple streams per connection; head-of-line-blocking-free')
```

---

## 7. Mathematical structures

The framework's lineage actually draws from this domain (see
`theory.md` § 5 on magma theory). It's worth cataloguing
explicitly, both as a witness to the framework's foundations and
as a clean structural domain.

### Initial breaks to consider

The classical refinement chain *is* the catalogue:

- **MS-Operation-Closure**: closed-binary-op (the magma seed)
- **MS-Associativity**: (semigroup adds)
- **MS-Identity**: (monoid adds)
- **MS-Inverses**: (group adds)
- **MS-Commutativity**: (abelian-group adds)
- **MS-Distributivity**: (ring requires two compatible operations)
- **MS-Multiplicative-Inverses-Excluding-Zero**: (field adds)
- **MS-Order**: (ordered structure adds)
- **MS-Topology**: (topological structure adds)

### Lineage / descent

The refinement chain *is* the descent structure:

```text
magma → semigroup → monoid → group → abelian-group →
                                        ring → integral-domain →
                                          field → ordered-field →
                                            real-closed-field
```

Each step `descended-from` the previous *and* adds new axioms.

### Temporal axis

Year of first articulation (sometimes ancient — groups go back to
Galois 1830s; magma is a 20th-century formalisation; topological
groups Pontryagin 1930s).

### Worked example

```python
cat.introduce_object('magma', 'Magma', year=1934)
cat.introduce_object('semigroup', 'Semigroup', year=1904,
                     lineage=[('magma', 'descended-from')])
cat.introduce_object('group', 'Group', year=1830,
                     lineage=[('semigroup', 'descended-from')])

cat.introduce_break('MS-Associativity', 'Operation is associative',
                    axes=['equivalential'])
cat.witness('semigroup', 'MS-Associativity', 'origin')

cat.introduce_break('MS-Inverses', 'Operation has inverses',
                    axes=['equivalential'])
cat.witness('group', 'MS-Inverses', 'origin')
```

The mathematical structures domain is the *cleanest possible*
example of the framework: each break adds an axiom; refinement
chains are descent edges; convergence is the moment when
mathematicians stop introducing new structure-classes.

---

## 8. Operating system designs

A domain with rich kernel-architecture distinctions.

### Initial breaks to consider

- **OS-Kernel-Architecture**: monolithic / micro / hybrid /
  exokernel / unikernel.
  *Axis*: spatial.
- **OS-Process-Model**: heavyweight / lightweight (threads) /
  fibers / actors / coroutines.
  *Axis*: parallel.
- **OS-IPC-Model**: shared-memory / message-passing / pipes /
  capabilities.
  *Axis*: spatial + temporal.
- **OS-Scheduling**: cooperative / preemptive / real-time /
  fair-share.
  *Axis*: temporal.
- **OS-Security-Model**: discretionary / mandatory / capability /
  sandbox.
  *Axis*: spatial.
- **OS-Filesystem-Abstraction**: VFS / object-based / direct.
  *Axis*: spatial.

### Lineage / descent

- Multics → Unix → BSD → Linux / macOS-XNU
- VMS → Windows NT
- L3 → L4 → seL4
- Plan 9 → Inferno
- QNX, MINIX (microkernel lineage)

### Temporal axis

Year of first stable release.

---

## 9. Machine-learning architectures

A rapidly-evolving domain with clean structural distinctions.

### Initial breaks to consider

- **ML-Loss-Function**: MSE / cross-entropy / contrastive /
  reinforcement / self-supervised.
  *Axis*: equivalential.
- **ML-Optimizer**: SGD / Adam / AdamW / LAMB / Lion.
  *Axis*: temporal.
- **ML-Architecture**: feedforward / convolutional / recurrent /
  attention / state-space / mixture-of-experts.
  *Axis*: spatial.
- **ML-Training-Paradigm**: supervised / self-supervised /
  reinforcement / few-shot / zero-shot.
  *Axis*: temporal.
- **ML-Scaling-Law**: Chinchilla / dense vs sparse / scaling-with-
  data vs scaling-with-compute.
  *Axis*: meta.
- **ML-Inference-Pattern**: greedy / beam-search / sampling /
  speculative-decoding / early-exit.
  *Axis*: temporal.

### Lineage / descent

- Perceptron → MLP → CNN (LeNet → AlexNet → ResNet → ConvNeXt)
- RNN → LSTM → GRU → Transformer (attention)
- Transformer → BERT → GPT → Claude / Llama / Mistral
- VAE → diffusion / flow-matching → stable-diffusion / DALL-E
- AlphaGo → MuZero → Gato / Gemini Robotics

### Temporal axis

Year of first public paper / first public release.

### Likely tensions

- **T-scaling-vs-architecture**: scaling laws change which
  architectural choices matter; many MoEs and SSM papers are
  refinements relative to scaling.
- **T-training-paradigm-vs-loss**: SSL paradigm forces specific
  loss functions; reinforcement forces RL-class losses.

---

## 10. Cataloguing your own database schema

A self-referential application: use the framework on a CRUD
database's schema. This is the structural dual sketched in
`theory.md` § 10 — every relational schema is implicitly a
catalogue of structural decisions; the framework makes the
implicit explicit.

### What's catalogued

The objects (specs) are *schema versions* — each migration
produces a new version. So `v001-initial`, `v002-add-users`,
`v003-add-orders`, etc. Each migration is a witness object whose
year is the date it was deployed.

Alternatively, the objects are *tables*: each table is a witness
of various structural-decision breaks. This view is more
fine-grained but loses the migration-time-ordering. Most catalogues
benefit from both kinds of object — schema versions AND tables —
with each entity-table being an "object" of catalogue-order
introduced at the version that created it.

### Initial breaks to consider

These are the structural-decision categories most relational
schemas surface. Each is a `(partition, preservation-theorem)`
pair that real DBs frequently embody:

- **DB-Identity**: how each row is uniquely identified.
  *(partition: by primary-key strategy)*. Variants: surrogate
  (auto-increment / UUID), natural (composite of business
  attributes), hybrid.
  *Axis*: spatial.
- **DB-Cardinality**: which relationships can be 1-to-many,
  many-to-many, etc. *(partition: by cardinality predicate)*.
  Witnessed by FK presence + uniqueness constraints.
  *Axis*: spatial.
- **DB-Lifecycle**: hard-delete vs soft-delete vs append-only.
  *(partition: by row-end-of-life policy)*. Soft-delete via
  `deleted_at`/`is_deleted`; hard-delete via `DELETE FROM`;
  append-only via insert-only with a "current" flag.
  *Axis*: temporal.
- **DB-Versioning**: how table-row history is preserved.
  Variants: none, separate audit table, valid-time columns
  (`valid_from`/`valid_to`), bitemporal.
  *Axis*: temporal.
- **DB-Polymorphism**: how heterogeneous data types are stored.
  Variants: single-table-inheritance (all subtypes in one wide
  table); class-table-inheritance (one table per subtype); JSON
  columns; tagged-union columns with discriminator + nullable
  fields.
  *Axis*: spatial.
- **DB-Soft-Constraints**: validation that lives at the application
  level rather than as a CHECK constraint. *(partition: by
  enforcement layer)*. App-level (more flexible, more error-prone);
  DB-level (more rigid, more reliable).
  *Axis*: equivalential.
- **DB-Referential-Integrity**: how FK violations are handled.
  Variants: CASCADE / RESTRICT / SET NULL / SET DEFAULT / no FK
  enforced at all (eventual consistency).
  *Axis*: temporal + equivalential.
- **DB-Audit-Pattern**: how mutations are tracked. Variants:
  no audit; `created_at`/`updated_at` columns; separate audit log;
  trigger-based audit.
  *Axis*: temporal + meta.
- **DB-Multi-Tenancy**: how tenants are isolated. Variants:
  tenant-id column on every table; schema-per-tenant;
  database-per-tenant.
  *Axis*: spatial + parallel.
- **DB-Data-Locality**: how data is geographically distributed.
  Variants: single region; multi-region active-passive;
  multi-region active-active; geo-partitioned by tenant or row
  attribute.
  *Axis*: spatial + parallel.

### Lineage / descent

Schema versions form a strict chain:

```text
v001-initial → v002-add-users → v003-add-orders → ... → vNNN-current
```

Each version `descended-from` the prior. Branching is rare in
production schemas (though feature branches in development
introduce parallel chains that get merged via squash-and-rebase).

### Temporal axis

The migration deployment date. Each schema version's `year`
attribute is when it landed in production. This makes the
originator-emerges-from-MIN-year pattern work directly: if a
constraint is added at v005 and an earlier-version-of-the-same-
break is later discovered (e.g., "we had this constraint informally
since v002 via app-level validation"), an `origin` witness from
v002 supersedes the v005 attribution automatically.

### Worked example

```python
cat = SymmetryCatalogue('/var/db/schema-history.db')

# Schema versions as objects
cat.introduce_object('v001-initial', 'Initial schema (Mar 2018)',
                     year=2018, attrs={'family': 'production-db'})
cat.introduce_object('v002-add-users', 'Add users table (Apr 2018)',
                     year=2018, attrs={'family': 'production-db'},
                     lineage=[('v001-initial', 'descended-from')])
cat.introduce_object('v007-soft-delete', 'Add deleted_at (Sep 2019)',
                     year=2019, attrs={'family': 'production-db'},
                     lineage=[('v006-prior', 'descended-from')])

# Structural-decision breaks
cat.introduce_break('DB-Identity', 'Row identification strategy',
                    axes=['spatial'])
cat.introduce_break('DB-Lifecycle', 'Row end-of-life policy',
                    axes=['temporal'])
cat.introduce_break('DB-Audit-Pattern', 'Mutation tracking',
                    axes=['temporal', 'meta'])

# Witness which migration introduced each
cat.witness('v002-add-users', 'DB-Identity', 'origin')
cat.witness('v002-add-users', 'DB-Identity', 'catalogue-introduces')
cat.refine('DB-Identity', 'v002-add-users', 'surrogate-auto-increment',
           description='users.id is BIGSERIAL; chosen for sortability')

cat.witness('v007-soft-delete', 'DB-Lifecycle', 'origin')
cat.witness('v007-soft-delete', 'DB-Lifecycle', 'catalogue-introduces')
cat.refine('DB-Lifecycle', 'v007-soft-delete', 'soft-delete-via-deleted-at',
           description='Required by GDPR soft-delete-then-purge workflow')

# A tension: the DB-Audit-Pattern is implemented inconsistently
cat.introduce_tension('T-audit-inconsistent',
    'Mixed audit patterns across tables',
    description='Some tables have created_at/updated_at; others have'
                ' separate audit log; new tables tend to use both.',
    breaks_involved=['DB-Audit-Pattern'])
```

### Likely tensions

Almost every long-lived schema has these:

- **T-soft-vs-hard-delete**: parts of the schema use soft delete,
  others hard delete. Often grandfathered from earlier conventions.
- **T-id-strategy-mixed**: surrogate keys in core tables;
  natural keys in lookup tables; UUID adopted later. Requires
  conversion functions across joins.
- **T-audit-inconsistent**: as in the worked example.
- **T-denormalisation-creep**: read-model denormalisations
  added for performance, not always reverted when use cases
  change.
- **T-deprecated-column**: column added for a feature that was
  later removed; column still in schema "in case it comes back."

The framework's tensions table is exactly the right place to
record these. The status field (`open`, `partially-addressed`,
`addressed`) tracks resolution.

### Practical applications

Once you have a catalogue of your schema's structural decisions:

#### Migration code review

Each migration PR can include a small catalogue update — which
break the migration witnesses, refines, or introduces. The PR
reviewer checks that the catalogue update matches the DDL.

#### Onboarding

A new engineer reads `catalogue://breaks` to see all structural
decisions and `catalogue://objects/{table-name}` to see which
breaks each table witnesses. Both are far more compact than reading
years of migrations.

#### Refactoring

When deciding whether a column or constraint can be removed,
query: "what break does this witness, and is the break still
load-bearing?" If the break has been promoted, deferred, or made
sibling-boundary, the refactor is informed.

#### Audit / compliance

When a regulator asks "do you have soft-delete?", the answer is:
"`SELECT * FROM refinements WHERE name = 'soft-delete-via-deleted-at'`"
— and you get back the migration, the rationale, the introducing
date, and the tables it applies to. Compliance-friendly by
construction.

### Why this case is special

This isn't just "another domain." It's the methodology applied
to the structure-of-structure of a CRUD database, which is exactly
the case `theory.md` § 10 describes as the *dual* relationship.
The catalogue framework's own implementation in `schema.sql` is
itself a (very small) catalogue of its own structural decisions
(S0-S11). Cataloguing your application's database is the same
move at production scale.

You don't have to retrofit existing schemas all at once. Start
small: catalogue the next migration. Over time, the catalogue
fills in. The framework is *additive*; the schema's history
isn't lost in the process.

---

## 11. The shape that recurs

Across all these domains, a few patterns recur:

### (a) The temporal axis is always something

In every domain, there's a *year* (or version, or paper-publication-
date, or release-date). The temporal axis is the universal anchor
for tropical-MIN attribution.

### (b) Lineage is always richer than vendors

Vendors / families / lineages are commonly multi-axis. A
language descended-from another *and* influenced-by a third *and*
in a family with siblings. Multiple `descended-from` edges work;
so do `influenced-by` and `family-member` edge kinds.

### (c) Convergence shows up

Mature domains (file systems, programming languages, mathematical
structures) have converged metamodels — most modern instances
refine existing breaks rather than introducing new ones. Active
domains (ML, post-quantum crypto, distributed databases) keep
introducing new breaks; those are where the framework's
cataloguing is most informative.

### (d) Tensions are universal

Every domain has implementation-alignment concerns — places where
the structural decomposition the framework names doesn't cleanly
match the data layout people use. Recording these as `tension`
rows (rather than forcing them into ill-fitting break/witness
shape) keeps the catalogue honest. Each domain accumulates its
own T1-Tn list.

### (e) Cross-domain wedge audits are informative

KQUERY between two domains' break sets surfaces cross-domain
structural patterns. The 11 cell shows shared primitives (e.g.,
both processors and operating systems have privilege models, and
the corresponding breaks in the two domains are structurally
related); the 10/01 cells show domain-specific specialisations;
the 00 cell shows what neither domain catalogues but might be
relevant to a meta-domain.

This is the *open question 1* in `methodology.md`: schema
interoperability across instances. As more domains are catalogued
in the framework, cross-domain wedge audits will become possible
and likely productive.

---

## What this file isn't

These templates are *starting points*, not finished catalogues.
Real cataloguing of any of these domains will:

- Surface breaks the templates didn't name.
- Force schema breaks (new tables, new columns) the templates
  didn't anticipate.
- Reveal tensions specific to the domain.
- Eventually converge — or surface that the metamodel needs
  extension.

The templates are *enough to begin*; the framework is what makes
them sustainable as cataloguing accumulates.

---

*See also: `methodology.md` (operational design),
`theory.md` (foundations), `tutorial.md` (walk-through),
`README.md` (quick-start).*

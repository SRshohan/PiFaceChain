# Intro

# Tools

- Deepface
# Diagram

## face model

```bash
flowchart TB
    subgraph FaceIDModel["🧠 Face ID Model Architecture"]
        Z["Sensor"]
        A["fa:fa-user-circle Canonical Face Model(468 Landmarks)"]
        B["fa:fa-pen Face Alignment"]
        C["fa:fa-code-branch Feature Extraction (Embeddings)"]
        D["fa:fa-project-diagram Neural Network (FaceNet512)"]
        E["fa:fa-check-circle Cosine Similarity Matching"]
        F["fa:fa-clipboard Decision Threshold"]
    end
    Z --> A
    A --> B
    B --> D
    D --> C
    B --> C
    C --> E
    E --> F

    style FaceIDModel fill:#D4EFDF,stroke:#27AE60,color:#000,font-weight:bold

```

## Blockchain

```bash

flowchart TB
    subgraph Org1["🏢 Organization 1"]
        Peer1["fa:fa-server Peer 1"]
        Chaincode1["fa:fa-file-contract Smart Contract (Chaincode)"]
        Ledger1["Ledger1(CouchDB)"]
    end

    subgraph Org2["🏢 Organization 2"]
        Peer2["fa:fa-server Peer 2"]
        Chaincode2["fa:fa-file-contract Smart Contract (Chaincode)"]
        Ledger2["Ledger2(CouchDB)"]
    end

    subgraph Ledger["🗂️ CouchDB Distributed Ledger"]
        WriteLedger["fa:fa-database Write to CouchDB"]
        EndorsePolicy["fa:fa-gavel Endorsement Policy"]
    end

    subgraph Blockchain["🔗 Blockchain Network"]
        Proposal["fa:fa-envelope User Transaction Request"]
        Org1
        Org2
        Ledger
        channel["Channel"]
    end


    Proposal --> Org1
    Proposal --> Org2
    Org1 --> EndorsePolicy
    Org2 --> EndorsePolicy
    Org1 <--> channel
    Org2 <--> channel
    EndorsePolicy --> WriteLedger

    style Blockchain fill:#D6EAF8,stroke:#5DADE2,color:#000,font-weight:bold
    style Org1 fill:#EBDEF0,stroke:#AF7AC5,color:#000,font-weight:bold
    style Org2 fill:#EBDEF0,stroke:#AF7AC5,color:#000,font-weight:bold
    style Ledger fill:#A9DFBF,stroke:#27AE60,color:#000,font-weight:bold


```


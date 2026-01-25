```mermaid
graph TD
    A[Start: User performs an Action] --> B{Action Type?};

    subgraph User Actions
        B --> C1{Login};
        B --> C2{Play Audio};
        B --> C3{Other Actions: Create, Update, Delete};
    end

    C1 --> D(Determine Status: Success/Failed);
    C2 --> D;
    C3 --> D;

    D --> E(Gather Log Data);

    subgraph Data Collected
        E --> E1[Username/Full Name];
        E --> E2[Action/Status];
        E --> E3[Operation Time (Timestamp)];
        E --> E4[Description (e.g., File Path, Error Message)];
        E --> E5[Operation Address (IP)];
        E --> E6[Client Type (OS/Browser)];
    end

    E --> F(Format Log Entry);
    F --> G(Store Log in Database/Storage);

    subgraph Audit Log System Backend
        G --> H{Query/Request Report};
        H --> I(Retrieve Filtered/Sorted Data);
    end

    I --> J(Display Log Entries on Audit Log Page);
    J --> K[End: Log Available for Review];

    style A fill:#A5D6A7,stroke:#388E3C,stroke-width:2px
    style K fill:#A5D6A7,stroke:#388E3C,stroke-width:2px
    style G fill:#E1BEE7,stroke:#8E24AA,stroke-width:2px
    style J fill:#BBDEFB,stroke:#1E88E5,stroke-width:2px
```
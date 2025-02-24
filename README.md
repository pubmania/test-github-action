graph TD
    A[GitHub Action] --> B[Build Temp Site]
    B --> C{Run Python Script}
    C --> D[Check Frontmatter for Bluesky URL]
    D -->|Exists| E[Skip Posting]
    D -->|Missing| F[Create Bluesky Post]
    F --> G[Update Frontmatter Metadata]
    G --> H[Rebuild Site with Updated Metadata]
    H --> I[Deploy to GitHub Pages]

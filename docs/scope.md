# Scope

This Audit & Accountability Policy applies to all systems, applications, and personnel handling Criminal Justice Information (CJI) within the eAgent® suite. It covers:

- **Data Capture**
  - Logging of every access, query, modification, or export of CJI.
- **Data Storage**
  - Secure retention of audit logs in our centralized logging infrastructure (e.g., ELK stack).
- **Data Transmission**
  - Encrypted transport of audit events between microservices, databases, and external systems.
- **Retention & Disposal**
  - Logs are retained for a minimum of 12 months and purged thereafter according to CJIS retention guidelines.
- **Access Control**
  - Only authorized roles may view or extract audit logs; all access is itself logged.
- **Reporting & Analysis**
  - Generation of scheduled and ad-hoc audit reports to detect anomalies or policy violations.

# Review Cycle

This section defines how and when the Audit & Accountability Policy is reviewed and updated.

## 1. Annual Review

- **When**: Every January 15th
- **Initiation**: A scheduled GitHub Action opens a “Policy Review” issue
- **Attendees**: Security Lead, Compliance Officer, IT Ops, Data Analyst
- **Output**: Approved updates merged via Pull Request and tagged with a new semantic version (e.g., `v1.1.0`)

## 2. Post-Incident Review

- **Trigger**: Detection of an `UNAUTHORIZED_ACCESS` event by ElastAlert
- **Action**: ElastAlert opens an immediate GitHub issue titled “Post-Incident Policy Review”
- **Timeline**: Stakeholders meet within 72 hours to assess root cause and update procedures

## 3. Ad-Hoc Updates

- **Scope**: Minor edits (e.g., contact changes, typo fixes)
- **Process**:
  1. Create a branch; update the relevant `.md` file.
  2. Open a Pull Request for peer review.
  3. Merge and update `CHANGELOG.md`.

---

**Versioning & Changelog**

- We use [semantic versioning](https://semver.org/): `v<major>.<minor>.<patch>`
- All releases and noteworthy changes are recorded in `CHANGELOG.md`.

# gcp-label-based-vm-cleanup

# GCP Label-Based VM Cleanup Tool

A serverless, event-driven solution to automatically manage Google Cloud Compute Engine instances based on their labels. This tool helps enforce cost-control policies by automatically stopping or deleting VMs that are marked for cleanup, such as temporary "lab" or "test" environments.

## 🏗️ Architecture Overview

This solution leverages Google Cloud's serverless ecosystem to create a responsive and scalable system:

1.  **Trigger:** A user adds a specific label (e.g., `auto-cleanup: true`) to a VM instance. This action emits an event log to Google Cloud's audit logs.
2.  **Event Capture:** **Eventarc** listens for the specific Compute Engine `insertLabel` event in the audit log.
3.  **Logic:** Eventarc triggers a **Cloud Run** service or a **Cloud Function** (2nd Gen).
4.  **Action:** The serverless function:
    *   Reads the label data from the triggering event.
    *   Uses the Compute Engine API to perform the defined action (e.g., `stop` or `delete`) on the VM.
5.  **Result:** VMs are automatically managed moments after they are tagged, without any manual intervention.


## ✨ Features

*   **Event-Driven:** Resources are managed in real-time based on label changes, not a fixed schedule.
*   **Serverless:** No servers to provision or manage. Built with Cloud Run, Eventarc, and Cloud Functions.
*   **Flexible Policy Engine:** Easily modify the code to react to different labels (e.g., `ttl: 2023-12-31`) or different actions (stop vs. delete).
*   **Cost Effective:** Only runs when a labelling event occurs; incurs no cost when idle.

## 🚀 Quick Start

### Prerequisites

- A Google Cloud Project with billing enabled.
- The `gcloud` CLI installed and authenticated on your machine.
- Basic knowledge of GCP services (IAM, Compute Engine).

### 1. Enable Required APIs

Enable the necessary Google Cloud APIs:

```bash
gcloud services enable \
  run.googleapis.com \
  eventarc.googleapis.com \
  cloudfunctions.googleapis.com \
  compute.googleapis.com \
  logging.googleapis.com


# Create the service account
gcloud iam service-accounts create vm-cleanup-tool \
    --description="SA for the label-based VM cleanup function" \
    --display-name="VM Cleanup Tool"

# Grant the necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:vm-cleanup-tool@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/compute.instanceAdmin.v1"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:vm-cleanup-tool@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/eventarc.eventReceiver"

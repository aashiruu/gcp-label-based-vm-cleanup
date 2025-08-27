import functions_framework
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import logging

# Initialize the Compute Engine client
compute = discovery.build('compute', 'v1')

@functions_framework.cloud_event
def stop_vm_on_label(cloud_event):
    """Triggered by a label insertion event. Stops the VM."""
    data = cloud_event.data

    # Extract resource information from the event payload
    resource_name = data['resourceName']
    project_id = data['resource']['labels']['project_id']
    zone = data['resource']['labels']['zone']
    instance_id = resource_name.split('/')[-1]

    # Check if the added label is our target label
    added_labels = data['protoPayload']['response']['labels']
    if 'auto-cleanup' in added_labels and added_labels['auto-cleanup'].lower() == 'true':
        logging.info(f"Label 'auto-cleanup:true' detected. Stopping instance {instance_id} in zone {zone}.")

        try:
            # Stop the instance
            stop_request = compute.instances().stop(project=project_id, zone=zone, instance=instance_id)
            stop_request.execute()
            logging.info(f"Successfully stopped instance: {instance_id}")

        except HttpError as e:
            logging.error(f"An API error occurred: {e}")
    else:
        logging.info("Triggering label was not 'auto-cleanup:true'. No action taken.")

def get_message_status(resp_message):
    statuses = ["rejected", "caution", "approved"]
    
    # Loop through the statuses in reverse order and check if they appear in the resp_message
    for status in reversed(statuses):
        if status.lower() in resp_message.lower():
            print(f"status: {status}")
            return status
    
    # Default to "caution" if none of the statuses appear
    return "caution"
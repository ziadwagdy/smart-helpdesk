import pandas as pd

# List of VIP support ticket names and descriptions
tickets = [
    {"name": "VIP Account Access Issue", "description": "Hi VIP Support,\nI am unable to access my VIP account. The system keeps logging me out every time I try to log in. Can you please resolve this urgently?\nBest,\nVIP User"},
    {"name": "VIP Data Sync Problem", "description": "Dear VIP Support,\nThere seems to be a problem with syncing data across my devices. The updates I make on one device are not reflecting on the other. Please look into this.\nBest,\nVIP User"},
    {"name": "VIP Custom Report Request", "description": "Hello,\nI need a custom report generated for my VIP account activity over the last quarter. Can you assist with this request?\nRegards,\nVIP User"},
    {"name": "VIP Priority Support Needed", "description": "Hi,\nI am facing an issue with my account settings, and I need priority support to resolve it as soon as possible. Please expedite this request.\nThanks,\nVIP User"},
    {"name": "VIP Feature Access Problem", "description": "Dear VIP Support Team,\nI am unable to access some of the VIP features on my account. The options are greyed out. Can you enable these features?\nSincerely,\nVIP User"},
    {"name": "VIP Data Migration", "description": "Hello,\nI need help migrating my data from my old account to my new VIP account. Can you provide assistance with this process?\nThanks,\nVIP User"},
    {"name": "VIP Subscription Renewal", "description": "Hi Support,\nMy VIP subscription is due for renewal, but I am facing issues with the payment process. Can you help renew my subscription?\nBest,\nVIP User"},
    {"name": "VIP Account Security", "description": "Hi,\nI have concerns about the security of my VIP account. Can you review the security settings and suggest any improvements?\nThanks,\nVIP User"},
    {"name": "VIP Customization Request", "description": "Dear Support,\nI would like to request some customizations for my VIP account dashboard. Can you assist with implementing these changes?\nRegards,\nVIP User"},
    {"name": "VIP Account Upgrade", "description": "Hello,\nI am interested in upgrading my VIP account to a higher tier. Can you provide details on the available options and assist with the upgrade?\nThanks,\nVIP User"},
    {"name": "VIP Performance Issue", "description": "Hi Team,\nMy VIP account is experiencing performance issues, and it is running slower than usual. Can you investigate and resolve this?\nBest,\nVIP User"},
    {"name": "VIP Transaction History", "description": "Dear Support,\nI need a detailed history of all transactions made through my VIP account. Can you provide this information?\nRegards,\nVIP User"},
    {"name": "VIP Feature Request", "description": "Hello,\nI have a suggestion for a new feature that would be beneficial for VIP users. Can you forward this request to the development team?\nThanks,\nVIP User"},
    {"name": "VIP Service Outage", "description": "Hi,\nI experienced a service outage on my VIP account yesterday. Can you provide an explanation and ensure this does not happen again?\nThanks,\nVIP User"},
    {"name": "VIP Billing Issue", "description": "Dear VIP Support,\nThere is an error in my latest VIP billing statement. The charges do not match my usage. Can you review and correct this?\nBest,\nVIP User"},
    {"name": "VIP Account Recovery", "description": "Hello,\nI have lost access to my VIP account and need help recovering it. Can you assist with the recovery process?\nRegards,\nVIP User"},
    {"name": "VIP Service Feedback", "description": "Hi Team,\nI would like to provide feedback on the VIP services I have been using. Can you provide a channel for submitting my feedback?\nBest,\nVIP User"},
    {"name": "VIP Data Backup", "description": "Dear Support,\nI need assistance with setting up regular data backups for my VIP account. Can you help configure this?\nRegards,\nVIP User"},
    {"name": "VIP Account Verification", "description": "Hello,\nI received a notification that my VIP account needs verification. Can you guide me through the verification process?\nThanks,\nVIP User"},
    {"name": "VIP Support Ticket Escalation", "description": "Hi,\nI submitted a support ticket two days ago, but have not received a response. Can you escalate this ticket for faster resolution?\nThanks,\nVIP User"},
    {"name": "VIP User Training", "description": "Dear Support,\nI am new to the VIP services and would like to schedule a training session to learn about all the features available. Can you arrange this?\nBest,\nVIP User"},
    {"name": "VIP Access Issue", "description": "Hello,\nI am unable to access the VIP section of the website. It shows an error message every time I try to log in. Can you help resolve this?\nRegards,\nVIP User"},
    {"name": "VIP Notification Settings", "description": "Hi,\nI would like to customize the notification settings for my VIP account. Can you assist with configuring these settings?\nThanks,\nVIP User"},
    {"name": "VIP Service Request", "description": "Dear VIP Support Team,\nI have a special service request related to my VIP account. Can you provide details on how to proceed with this request?\nSincerely,\nVIP User"},
    {"name": "VIP Account Deactivation", "description": "Hello,\nI need to temporarily deactivate my VIP account. Can you provide instructions on how to do this?\nThanks,\nVIP User"}
]

# Generate the data
data = [{"Name": ticket["name"], "Description": ticket["description"]} for ticket in tickets]

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("vip_tickets.xlsx", index=False)
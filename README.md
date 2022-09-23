# universal-reminder-tool
Easy to integrate reminder tool for alerts well before expiry


### Why?
Well, it started with exploration to find a tool that provide simple alerting well in-advance before expiry of any secrets 
And more importantly integrate very smoothly with any type of secret inc. Cloud Secrets such as Azure Service Principal or Vault secrets with limited expiry etc.

To my surprise there was no proper Open Source Tool that I found for doing this. So here is my contribution, a very simple reminder-tool who capabilities include
- Adding reminders
- Evaluate reminders to provide alerting from X days in advance (X being configurable)
[No fancy stuff yet]. 

Hope this tool would help people who have faced similar problem.

##### Example
```Shell
    curl --request POST 'https://<ingress-url>/add-reminders' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title": "<Title>",
        "reminder_type": "<REMINDER_TYPE>",
        "reminder_message": "<Reminder Message>",
        "duration": "<Duration: 10s|365d"
    }'
```



### Developer's Note
Any and all contributions to improve this tool are welcome and encouraged, looking forward to it


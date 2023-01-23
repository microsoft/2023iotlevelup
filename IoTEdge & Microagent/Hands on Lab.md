# IoT Edge & Defender for IoT Micro Agent Lab

## Lab 1: Configure Defender for IoT in IoT Hub


## Lab 2: Setup IoT Edge & Micro Agent in VM


## Lab 3: Analytics

1. Configure loganalytics setting with Defender for IoT
    ```
    az security workspace-setting create -n default --target-workspace /subscriptions/$subscriptionId/resourcegroups/$resourceGroup/providers/Microsoft.OperationalInsights/workspaces/$loganalyticsws
    
    az security iot-solution show --solution-name $iotHubName --resource-group $resourceGroup

    ```

## Clean Up
az group delete --name $resourceGroup





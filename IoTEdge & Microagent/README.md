# IoT Edge & Defender for IoT Micro Agent Lab

## Pre-requisites

### In Cloud
#### Using Portal
1. Open Azure Subscription here - [Azure](https://portal.azure.com)
2. Create Resource Group
3. Create IoT Hub
4. Create IoT Edge device in IoT Hub 
5. Create Log Analytics Workspace
6. Create VM (to configure IoT Edge)

#### Using CLI
1. Open Cloud Shell here - [Azure CLI](https://shell.azure.com)
    >First time you will required to create Storage account for CLI
2. Install & Update IoT Extension using commands at CLI prompt
    ``` 
    az extension add --name azure-iot
    az extension update --name azure-iot 
    ```
3. Store parameters to create unique resource names
    ```
    randomNumber=$RANDOM
    randomIdentifier=$USER$randomNumber

    subscriptionId=$(az account show --query id -o tsv)
    location="East US" 
    resourceGroup="IoT-LevelUp-$randomIdentifier" 
    iotHubName="IoT-LevelUp-Hub-$randomIdentifier"
    edgedeviceName="edgedevice"$randomNumber
    loganalyticsws="$randomIdentifier-logws"

    echo "export subscriptionId="$subscriptionId > myconfig.log
    echo "export randomIdentifier="$randomIdentifier >> myconfig.log
    echo "export location="\"$location\" >> myconfig.log
    echo "export resourceGroup="$resourceGroup >> myconfig.log
    echo "export iotHubName="$iotHubName >> myconfig.log
    echo "export edgedeviceName="$edgedeviceName >> myconfig.log
    echo "export loganalyticsws="$loganalyticsws >> myconfig.log

    source myconfig.log
    

4. Create Resource Group for resources
    ```
    az group create --name $resourceGroup --location "$location" 
    ```
5. Create IoT Hub S1 SKU x 1  and save connection string in notepad for future use
    ```
    az iot hub create --name $iotHubName --resource-group $resourceGroup --sku S1  

    HUBCONNECTIONSTRING=$(az iot hub connection-string show -n $iotHubName --policy-name iothubowner --key-type primary --query "connectionString") 

    echo "IoT Hub Connection String ="
    echo $HUBCONNECTIONSTRING

    ```
6. Create IoT Edge device in IoT Hub and save device connection string in notepad 
    ```
    az iot hub device-identity create -n $iotHubName -d $edgedeviceName --ee

    DEVICECONNECTIONSTRING=$(az iot hub device-identity connection-string show --device-id $edgedeviceName  --hub-name $iotHubName --key-type primary -o tsv)

    echo "Device Connection String ="
    echo $DEVICECONNECTIONSTRING

    ```

7. Create Log Analytics Workspace
    ```
    az monitor log-analytics workspace create -g $resourceGroup -n $loganalyticsws
    az monitor log-analytics workspace show --resource-group $resourceGroup --workspace-name $loganalyticsws

    ```
8. Create VM 
    ```
    az vm create --resource-group $resourceGroup --name vm$randomIdentifier --image Canonical:0001-com-ubuntu-server-focal:20_04-lts:latest --admin-username $USER --admin-password "IoTLevelUp2023#" --size Standard_DS2_v2 --public-ip-address-dns-name dns$randomIdentifier --public-ip-sku Standard --nsg-rule SSH --no-wait


    ```

### On PC
1. Install Visual Studio Code
2. Install IoT Hub & IoT Edge Extensions
3. Install Git


# Hands on Lab

## Lab 1: Configure Defender for IoT in IoT Hub
    ```
    az security iot-solution create --solution-name $iotHubName --resource-group $resourceGroup --iot-hubs /subscriptions/$subscriptionId/resourcegroups/$resourceGroup/providers/Microsoft.Devices/IotHubs/$iotHubName --display-name $iotHubName --location "eastus" --workspace $loganalyticsws

    ```

## Lab 2: Setup IoT Edge & Micro Agent in VM
    ```

    ```

## Lab 3: Analytics
1. Enable Defender for IoT with IoT Hub
    ```

    ```

2. Configure loganalytics setting with Defender for IoT
    ```
    az security workspace-setting create -n default --target-workspace /subscriptions/$subscriptionId/resourcegroups/$resourceGroup/providers/Microsoft.OperationalInsights/workspaces/$loganalyticsws
    
    az security iot-solution show --solution-name $iotHubName --resource-group $resourceGroup

    ```

## Clean Up
az group delete --name $resourceGroup






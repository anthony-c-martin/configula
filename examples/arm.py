resources = []
location = "[resourceGroup().location]"

def storageAccount(name, location, properties):
  return <
    type: 'Microsoft.Storage/storageAccounts'
    apiVersion: '2015-06-15'
    name: !~ name
    location: !~ location
    properties: !~ properties
  >

def networkInterface(name, location, properties):
  return <
    type: 'Microsoft.Network/networkInterfaces'
    apiVersion: '2015-06-15'
    name: !~ name
    location: !~ location
    properties: !~ properties
  >

def virtualMachine(name, location, properties):
  return <
    type: 'Microsoft.Compute/virtualMachines'
    apiVersion: '2019-07-01'
    name: !~ name
    location: !~ location
    properties: !~ properties
  >

resources.append(storageAccount('testsa', location, <
  accountType: Standard_LRS
>))

resources.append(networkInterface('test-nic', location, <
  ipConfigurations:
  - name: myConfig
    properties:
      subnet:
        id: '[parameters(''subnetResourceId'')]'
      privateIPAllocationMethod: Dynamic
>))

resources.append(virtualMachine('test-vm', location, <
  osProfile:
    computerName: myVm
    adminUsername: "[concat(parameters('namePrefix'), 'admin')]"
    adminPassword: myS3cretP@ssw0rd
    windowsConfiguration:
      provisionVMAgent: true
  hardwareProfile:
    vmSize: Standard_A1_v2
  storageProfile:
    imageReference:
      publisher: MicrosoftWindowsServer
      offer: WindowsServer
      sku: 2016-Datacenter
      version: latest
    osDisk:
      createOption: FromImage
    dataDisks: []
  networkProfile:
    networkInterfaces:
    - properties:
      primary: true
      id: "[resourceId('Microsoft.Network/networkInterfaces', concat(parameters('namePrefix'),'-nic'))]"
  diagnosticsProfile:
    bootDiagnostics:
      enabled: true
      storageUri: "[variables('bootDiagsUri')]"
>))

render(resources)
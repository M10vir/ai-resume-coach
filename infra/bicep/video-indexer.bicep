param location string
param mediaServiceName string = 'coachmedia${uniqueString(resourceGroup().id)}'
param storageAccountName string

resource mediaStorage 'Microsoft.Storage/storageAccounts@2022-09-01' existing = {
  name: storageAccountName
}

resource mediaServices 'Microsoft.Media/mediaservices@2021-11-01' = {
  name: mediaServiceName
  location: location
  properties: {
    storageAccounts: [
      {
        id: mediaStorage.id
        type: 'Primary'
      }
    ]
  }
}

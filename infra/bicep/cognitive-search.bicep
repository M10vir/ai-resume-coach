param location string
param searchServiceName string = 'coachsearch${uniqueString(resourceGroup().id)}'

resource search 'Microsoft.Search/searchServices@2020-08-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: 'basic' // or use 'standard' if needed
  }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
  }
}

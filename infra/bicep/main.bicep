targetScope = 'subscription'

param location string = 'eastus'
param resourceGroupName string = 'rg-ai-resume-coach'
@secure()
param adminPassword string

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}

module openai 'openai.bicep' = {
  name: 'openaiModule'
  scope: rg
  params: {
    location: location
  }
}

module postgres 'postgres.bicep' = {
  name: 'postgresModule'
  scope: rg
  params: {
    location: location
    adminPassword: adminPassword  // Replace this with a secure one
  }
}

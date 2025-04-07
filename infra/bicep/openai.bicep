param location string

resource openai 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'openai-coach'
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
    tier: 'Standard'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

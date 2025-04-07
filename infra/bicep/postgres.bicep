param location string

@secure()
param adminPassword string

param adminUsername string = 'postgresadmin'
param dbName string = 'resume_analysis'
param postgresServerName string = 'pg-resume-coach'

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
  }
  properties: {
    administratorLogin: adminUsername
    administratorLoginPassword: adminPassword
    version: '13'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

resource db 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: postgres
  name: dbName
  properties: {}
}

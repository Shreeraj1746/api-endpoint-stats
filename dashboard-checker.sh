#!/bin/bash

# This script checks if a dashboard with a specific name exists in Grafana
# If not, it creates the dashboard using the Grafana API

# Set the Grafana credentials and URL
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin"
DASHBOARD_UID="endpoint-stats"

echo "Checking connection to Grafana..."
# Test if we can connect to Grafana
response=$(curl -s -o /dev/null -w "%{http_code}" $GRAFANA_URL/api/health)
if [ $response -ne 200 ]; then
  echo "Error: Cannot connect to Grafana at $GRAFANA_URL (HTTP $response)"
  exit 1
fi
echo "Successfully connected to Grafana."

echo "Authenticating with Grafana..."
# Get auth token (in newer Grafana versions)
auth_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name":"dashboard-checker", "role": "Admin"}' $GRAFANA_URL/api/auth/keys -u "$GRAFANA_USER:$GRAFANA_PASSWORD")
token=$(echo $auth_response | grep -o '"key":"[^"]*' | grep -o '[^"]*$')

if [ -z "$token" ]; then
  echo "Using basic authentication instead of token..."
  AUTH="-u $GRAFANA_USER:$GRAFANA_PASSWORD"
else
  echo "Using token authentication..."
  AUTH="-H 'Authorization: Bearer $token'"
fi

echo "Checking if dashboard exists..."
# Directly check if the dashboard exists by UID
dashboard_response=$(eval "curl -s -o /dev/null -w '%{http_code}' $AUTH $GRAFANA_URL/api/dashboards/uid/$DASHBOARD_UID")

if [ "$dashboard_response" == "200" ]; then
  echo "Dashboard 'Endpoint Statistics Dashboard' already exists!"
  # Get the dashboard info
  dashboard_info=$(eval "curl -s $AUTH $GRAFANA_URL/api/dashboards/uid/$DASHBOARD_UID")
  echo "Dashboard info successfully retrieved."
else
  echo "Dashboard not found (HTTP $dashboard_response). Creating dashboard..."

  # Check for the local create-dashboard.json file
  if [ -f "create-dashboard.json" ]; then
    echo "Using local dashboard JSON file..."
    dashboard_file="create-dashboard.json"
  else
    echo "Error: Dashboard JSON file not found!"
    exit 1
  fi

  # Create the dashboard using the local file
  dashboard_create=$(eval "curl -s -X POST $AUTH -H 'Content-Type: application/json' -d @$dashboard_file $GRAFANA_URL/api/dashboards/db")

  if echo "$dashboard_create" | grep -q "success"; then
    echo "Dashboard created successfully!"
    dashboard_uid=$(echo "$dashboard_create" | grep -o '"uid":"[^"]*' | grep -o '[^"]*$')
    dashboard_url=$(echo "$dashboard_create" | grep -o '"url":"[^"]*' | grep -o '[^"]*$')
    echo "Dashboard UID: $dashboard_uid"
    echo "Dashboard URL: $dashboard_url"
  else
    echo "Failed to create dashboard:"
    echo "$dashboard_create"
  fi
fi

# Revoke the API key if we created one
if [ ! -z "$token" ]; then
  echo "Revoking temporary API key..."
  key_id=$(echo $auth_response | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
  revoke_response=$(eval "curl -s -X DELETE $AUTH $GRAFANA_URL/api/auth/keys/$key_id")
fi

echo "Done."

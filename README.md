# eWaste Recycling Project
Team 01 – COM6103

## Requests API (Collection Requests)

Base URL: `http://127.0.0.1:5050`

### Auth: register/login tokens

> If login fails and token is empty, run register first (fresh DB).

```bash
# Register a consumer (only needed once per database)
curl -i -X POST http://127.0.0.1:5050/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"consumer@test.com","password":"123456"}'

# Login consumer -> token
CONSUMER_TOKEN=$(curl -s -X POST http://127.0.0.1:5050/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"consumer@test.com","password":"123456"}' \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token',''))")

echo "CONSUMER_TOKEN=$CONSUMER_TOKEN"



# Create a collection request
curl -i -X POST http://127.0.0.1:5050/api/requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CONSUMER_TOKEN" \
  -d '{"item_name":"Old iPhone X","category":"phone","condition":"broken","preferred_method":"dropoff"}'

# List my requests
curl -i http://127.0.0.1:5050/api/requests/mine \
  -H "Authorization: Bearer $CONSUMER_TOKEN"

# Get one request by id (replace 1)
curl -i http://127.0.0.1:5050/api/requests/1 \
  -H "Authorization: Bearer $CONSUMER_TOKEN"



# Make admin (if you have the script)
python backend/scripts/make_admin.py admin@test.com

# Login admin -> token
ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:5050/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"123456"}' \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token',''))")

echo "ADMIN_TOKEN=$ADMIN_TOKEN"

# List all requests
curl -i http://127.0.0.1:5050/api/requests \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Filter by status
curl -i "http://127.0.0.1:5050/api/requests?status=submitted" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Update status (replace 1)
curl -i -X PATCH http://127.0.0.1:5050/api/requests/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"status":"approved"}'
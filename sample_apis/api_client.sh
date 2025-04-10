
API_ENDPOINT="http://127.0.0.1:8000"
OPENAIAPI_SPEC_FILE="fake_openapi.json"

SLEEP_TIME=0.1

echo "Posting to the API"
curl -X POST "$API_ENDPOINT/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "High-end device", "price": 1500.0, "tax": 150.0}'

sleep $SLEEP_TIME


echo -e "\n\nGetting one item from the API"
curl "$API_ENDPOINT/items/123"

sleep $SLEEP_TIME

echo -e "\n\nGetting the openapi schema from the API"
curl -s "$API_ENDPOINT/openapi.json"  > $OPENAIAPI_SPEC_FILE
echo ""

jq "." $OPENAIAPI_SPEC_FILE > /dev/null
if [ $? -eq 0 ]; then
    echo "OpenAPI schema is valid."
else
    echo "OpenAPI schema is invalid."
fi
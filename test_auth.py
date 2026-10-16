from azure.identity import AzureCliCredential

credential = AzureCliCredential()

token = credential.get_token(
    "https://ai.azure.com/.default"
)

print("Authentication successful")
print("Token acquired")
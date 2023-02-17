import requests

# Retrieve the input file from GitHub
input_url = "https://raw.githubusercontent.com/CTH-JC-CC/APT28-IOC/main/additional_URLs"
response = requests.get(input_url)
urls = response.text.splitlines()

# Generate the KQL query
kql = "search *\n| where " + " or ".join(["Url == '" + url + "'" for url in urls])

# Write the KQL query to the output file
output_file = input_url.split("/")[-1].replace(".txt", "_output.txt")
with open(output_file, "w") as f:
    f.write(kql)

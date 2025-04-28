from apify_client import ApifyClient

# Initialize the ApifyClient with your Apify API token
# Replace '<YOUR_API_TOKEN>' with your token.
client = ApifyClient("apify_api_J0NOcRQl64HWS74ZRdzIUYa24OW9Jb3mPJIV")

# Prepare the Actor input
run_input = {
    "startUrls": [{ "url": "https://docs.apify.com/academy/web-scraping-for-beginners" }],
    "useSitemaps": False,
    "respectRobotsTxtFile": True,
    "crawlerType": "playwright:adaptive",
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "initialCookies": [],
    "proxyConfiguration": { "useApifyProxy": True },
    "keepElementsCssSelector": "",
    "removeElementsCssSelector": """nav, footer, script, style, noscript, svg, img[src^='data:'],
[role=\"alert\"],
[role=\"banner\"],
[role=\"dialog\"],
[role=\"alertdialog\"],
[role=\"region\"][aria-label*=\"skip\" i],
[aria-modal=\"true\"]""",
    "clickElementsCssSelector": "[aria-expanded=\"false\"]",
}

# Run the Actor and wait for it to finish
run = client.actor("apify/website-content-crawler").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)

# 📚 Want to learn more 📖? Go to → https://docs.apify.com/api/client/python/docs/quick-start
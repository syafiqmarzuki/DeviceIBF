import tweepy

auth = tweepy.OAuthHandler("8ZttJWOCRWYFc98DDBtK2K1xA", "f3z8UiSpqRklN2BkXubOd5yg6qZqZXC0zRugRALb8IWXEMpMrq")
auth.set_access_token("1253167579650158593-6c7cZ1o0bfIILvblMwy8rpR38O0UFK", "0fHrd7ILuK5iJWIMApr0NkFi4Rzkn6w7vpnmi27xI4YBz")

# Create API object
api = tweepy.API(auth)

data = 30
f = 'ketinggain hahahhahah'
g = 'cm harap lunga'
print(f,data,g)
api.update_status(s)




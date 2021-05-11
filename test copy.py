import requests

paramDict = {"email":"test@gmail.com","coupon_code":"GETUR1SUGARGNOME",'recaptcha_token': "03AGdBq26bBpzl2KOupZVN7eQyaquCi2J4phl9YVqYRQdUswpZgdqkS_aPpWqbgaKZ5quRxC3gE3RoPm5aceGQclYmKTyqz0Owb06EezdMcTQZ4CRHZ5sau7UHt_uPqZM4FpwdP8vpQkWVaEzhc2a8GlTCb84Uz_Mt2HNZOQhxRh5sL_4dpQAYBC016luiXlL_zo0OHpSs9OaaAjqer2piKuGKHmVfbkBiy02ItKY-MAMOdaQe8gqNeFG5ZIp6kwsj5h1p2uRToUAgiXtxBcMFFp1-7BnSpvSiZRE7U2t8tukwdN2aGoJAN4G_ZxHoKxPI8XXrp49J79wcg1_b2eLLzQTs5f8qbj8Hj53vBC1NonEk70bCwUsd92dYbz2-3yeOpJKbg3iNd5Yuu5gwuxSUAM3wuHkBuyHR-JUpEfYrGRV4rISn_lEx5KcEu6MTD5-3RO0Gy7pN4dF5"}

url = "https://account.devplay.com/v2/coupon/ck"
#response = requests.get(url, params=paramDict)
response = requests.post(url, data=paramDict)

print("status status_code :", response.status_code)
print("status text :", response.text)
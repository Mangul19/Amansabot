import requests, json

couponCode = "XYOKSPZLLUJYFKJN"

data = {
  "email": "test@gmail.com",
  "coupon_code": couponCode,
  "recaptcha_token": "---------"
}

url = "https://account.devplay.com/v2/coupon/ck"
#response = requests.get(url, params=paramDict)

response = requests.post(url, data=json.dumps(data))

code = response.text.split(":")[1][:-2]

print("status status_code :", response.status_code)
print("status text :", code)

def switch(code):
  return {"20000":"상품이 정상적으로 지급되었습니다. 게임에 접속해서 확인해주세요.",
    "40006":"DevPlay 계정을 다시 한번 확인해주세요.",
    "42501":"사용 기간이 만료된 쿠폰입니다.",
    "42502":"쿠폰번호를 다시 한번 확인해주세요.",
    "42503":"해당 계정으로 이미 같은 종류의 쿠폰을 등록하셨습니다.",
    "42504":"해당 계정으로 이미 같은 종류의 쿠폰을 등록하셨습니다."}.get(code,"서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.")
    
  print(switch(code))
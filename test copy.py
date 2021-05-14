import requests, json

couponCode = "XYOKSPZLLUJYFKJN"

data = {
  "email": "test@gmail.com",
  "coupon_code": couponCode,
  "recaptcha_token": "03AGdBq27yCQSdWQiP0pwYBVVyL6aqJ5RGBgA3GzHx2eRcNpdkolspZibdhYMV4xMuI-9U6xuPQTs_A3Fa670MTErhtmp9TwS-5k97EXwowT9K-m-ZiGo2L7B1VxH0WVuGOJDrnL0t6m3iJv6L68k8r8_oz0rQV-5jWqa_vjaW15ldLxdT3qYGqedV0YYCH7zp_s_nik8Cs0RFyXxbwTj4uOu62WH8_OSJkPn-X9pd3niyF7r0sUEm5b23fOf9fBahKEL-3MFuxiMPSiyAGCyNF_II-xRBzt3SgLtfyWX8fkP6jsyEfQ2xPrpFfg-uP8HxgVQTxzExSESzsQn4ql0Tmk_P1HrWlq0-OhiAsbqI-4NJgKWA03S7pD4n2zvSIrk-DzdFzbcJcRw9mc0V_oC6UzBvn9KvOSFib8uJKU-bmYgnMhzof33Jj5ziosmvbWJdvaG75JkoH31T"
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
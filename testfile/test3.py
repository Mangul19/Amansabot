import requests, json

data = {
  "0": "https://www.coupon.lordofheroes.com/",
  "1": "D6P337D1DJ1GHXMQ",
  "2": "LOHFRONTIER"
}

url = "https://www.coupon.lordofheroes.com/_api/wix-code-public-dispatcher/siteview/backend/aModule.jsw/useCoupon.ajax?gridAppId=04ff3e18-525e-42cb-b8c6-a7e7198d0860&instance=wixcode-pub.2fd497917a98f4b500d1eec2f0a4bb8b04bd33de.eyJpbnN0YW5jZUlkIjoiMDQ0ZDZiNzUtZjM4MC00M2ZmLThkMmItMjVhNGQwZjU3MzYzIiwiaHRtbFNpdGVJZCI6IjQ5NmZlM2VjLTFlMDktNDYzZC05MDM2LWQ3NTRiYzA5YzIzOSIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTYyMTIxNTE3ODI4MSwiYWlkIjoiZmQxNGMyOGQtMWU2NC00ZGFjLTgyYmQtNTEwMjk5YTUwMjc4IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6IjI1N2Q0NjhlLTdjNjUtNDg4Ni04Mzk5LTAwYWQ0YmVlYmYxZCIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6IkFkc0ZyZWUsU2hvd1dpeFdoaWxlTG9hZGluZyxIYXNEb21haW4iLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiOGZkOWZhMTEtODhmYy00YWM5LTg5MzItYTFjMGM4MTcyZTllIiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsfQ==&viewMode=site"
#response = requests.get(url, params=paramDict)

response = requests.post(url, data=json.dumps(data))

code = response.text

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
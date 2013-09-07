require 'sinatra'
require 'oj'
require 'httparty'

CLIENT_ID = "kaj9cycumsukkw37cwrn67v9del0iieg"
CLIENT_SECRET = "tXvUvg1NjiSkPt8JPJZ4Awn71as5eUvn"

@@access = []

def request_auth(url,data)
  response = HTTParty.post(url, body: data)
  hash = Oj.load(response.body)
  if hash["error"]
    status 404
    #nice error handling
  else
    hash["expires_in"] = (Time.now + hash["expires_in"] * 60).to_f
  end
  hash
end

def add_new_account(code)
  url = "https://www.box.com/api/oauth2/token"
  data = "grant_type=authorization_code&code=#{code}&client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}"
  @@access << request_auth(url,data)
end

def refresh_account(acc)
  url = "https://www.box.com/api/oauth2/token"
  refresh_token = acc["refresh_token"]
  data = "grant_type=refresh_token&refresh_token=#{refresh_token}&client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}"
  acc = request_auth(url,data)
end

def do_search(query, acc)
  while true
    response = HTTParty.get("https://api.box.com/2.0/search?query=#{query}&offset=0",
                            headers: {"Authorization" => "Bearer #{acc["access_token"]}"}
                           )
    if response.headers["www-authenticate"] &&
       response.headers["www-authenticate"]["error"]
      refresh_account(acc)
    else
      return Oj.load(response.body)
    end
  end
end

get '/' do
  "Hello World"
end

get '/register' do
  redirect "https://www.box.com/api/oauth2/authorize?response_type=code&client_id=#{CLIENT_ID}&redirect_uri=http://127.0.0.1:4567/add_access"
end

get '/search/:value' do |value|
  hash = {}
  @@access.each_with_index do |acc,idx|
    hash["#{idx}"] = do_search(value,acc)
  end
  Oj.dump(hash)
end

get '/add_access' do
  status 404 unless params[:code]
  add_new_account(params[:code])
  "success"
end

post '/sendsms' do
  system("python python_sms_sender/send_sms.py #{params[:phone_number]} #{params[:sms_text]}")
end

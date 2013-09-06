require 'sinatra'
require 'oj'
require 'httparty'

CLIENT_ID = "kaj9cycumsukkw37cwrn67v9del0iieg"
CLIENT_SECRET = "tXvUvg1NjiSkPt8JPJZ4Awn71as5eUvn"

@@access = []


get '/' do
  "Hello World"
end

get '/register' do
  redirect "https://www.box.com/api/oauth2/authorize?response_type=code&client_id=#{CLIENT_ID}&redirect_uri=http://127.0.0.1:4567/add_access"
end

get '/add_access' do
  status 404 unless params[:code]
  url = "https://www.box.com/api/oauth2/token"
  data = "grant_type=authorization_code&code=#{params[:code]}&client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}"
  response = HTTParty.post(url, body: data)
  @@access << Oj.load(response.body)
  "LUAUFT"
end



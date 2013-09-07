require 'sinatra'
require 'oj'
require 'httparty'
require 'haml'
require './access.rb'

CLIENT_ID = "kaj9cycumsukkw37cwrn67v9del0iieg"
CLIENT_SECRET = "tXvUvg1NjiSkPt8JPJZ4Awn71as5eUvn"

module Helper
  def self.url_for(text, obj = nil)
    if obj.nil?
      "#{server}/ui"
    elsif obj.is_a?(Symbol) || obj.is_a?(String)
      "#{server}/ui/#{obj}"
    else
      name = obj.class.name.demodulize.tableize
      "#{server}/ui/#{name}/#{obj.id}"
    end
  end

  def self.link(text, obj = nil)
    %{<a href="">#{text}</a>}
  end

  def self.nav_link(text, obj = nil)
    url = ""
    cls = ""

    #if request.path =~ /ui$/
    #  cls = "active" if obj.nil?
    #elsif url =~ %r{#{request.path}}
      cls = "active"
    #end

    %{<li class="#{cls}"><a href="#{url}">#{text}</a></li>}
  end
end

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
  Access.instance.add_account(request_auth(url,data))
end

def refresh_account(account)
  url = "https://www.box.com/api/oauth2/token"
  refresh_token = account.refresh_token
  data = "grant_type=refresh_token&refresh_token=#{refresh_token}&client_id=#{CLIENT_ID}&client_secret=#{CLIENT_SECRET}"
  account = request_auth(url,data)
end

def do_search(query, account)
  while true
    response = HTTParty.get("https://api.box.com/2.0/search?query=#{query}&offset=0",
                            headers: {"Authorization" => "Bearer #{account.access_token}"}
                           )
    if response.headers["www-authenticate"] &&
       response.headers["www-authenticate"]["error"]
      refresh_account(account)
    else
      return Oj.load(response.body)
    end
  end
end

def create_shared_link(user_id, file_id)
  access_token = Access.instance.get_account(user_id).access_token
  response = HTTParty.put("https://api.box.com/2.0/files/#{file_id}",
                            headers: {"Authorization" => "Bearer #{access_token}"},
                            body: '{"shared_link": {"access":  "open"}}')
  return Oj.load(response.body)["shared_link"]["url"]
end

def send_sms(phone_number, message)
  system("python python_sms_sender/send_sms.py #{phone_number} #{message}")
end

get '/' do
  haml :index
end

get '/register' do
  redirect "https://www.box.com/api/oauth2/authorize?response_type=code&client_id=#{CLIENT_ID}&redirect_uri=http://127.0.0.1:4567/add_access"
end

#get '/search/:value' do |value|
#  data = []
#  Access.instance.accounts.each_with_index do |account,idx|
#    search_result = do_search(value,account)
#    search_result['user_id'] = account.user_id
#    data << search_result
#  end
#  haml :results, locals: {data: data}
#end

get '/search/:value' do |value|
  data = {}
  Access.instance.accounts.each do |account|
    search_result = do_search(value,account)
    data[account.user_id.to_s] = search_result["entries"]
  end
  haml :results, layout: false, locals: {data: data}
end

get '/add_access' do
  status 404 unless params[:code]
  add_new_account(params[:code])
  haml :index
end

get '/registered_users' do
  accounts = Access.instance.accounts
  haml :registered_users, locals: {accounts: accounts}
end

get '/request_access/:user_id/:file_id' do | user_id, file_id |
  redirect create_shared_link(user_id, file_id)
end

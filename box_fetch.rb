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
  Access.instance.update_account(account,request_auth(url,data))
end

def do_search(query, account)
  while true
    response = HTTParty.get("https://api.box.com/2.0/search?query=#{query}&limit=5&offset=0",
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
  threads = []
  Access.instance.accounts.each do |account|
    t = Thread.new{
      user = {}
      user["user_id"] = account.user_id
      user["name"] = account.name
      user["phone_number"] = account.phone_number
      user["avatar_url"] = account.avatar_url
      user["results"] = do_search(value,account)["entries"]
      if user["results"].empty?
        Thread.current["data"] = {}
        Thread.current["user_id"] = account.user_id.to_s
      else
        Thread.current["data"] = user
        Thread.current["user_id"] = account.user_id.to_s
      end
    }
    threads << t
  end
  data = {}
  threads.each do |thread|
    thread.join
    data[thread["user_id"]] = thread["data"]
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

get '/request_access/:user_id/:file_id/:file_name' do | user_id, file_id, file_name |
  # TODO: fox bug: this endpoint is some how called 2 times.
  account = Access.instance.get_account(params[:user_id])
  send_sms(account.phone_number, "Hi #{account.name}! Your file #{file_name} has been shared.")
  redirect create_shared_link(user_id, file_id)
end

# post '/send_sms' do
#   account = Access.instance.get_account(params[:user_id])
#   send_sms(account.phone_number, params[:message])
#   return true
# end

get '/download_file/:user_id/:file_id/:file_name' do | user_id, file_id, file_name |
  file_path = "public/img/box/#{file_id}_#{file_name}"
  account = Access.instance.get_account(params[:user_id])

  if not File.exists?(file_path)
    response =  HTTParty.get("https://api.box.com/2.0/files/#{file_id}/content",
                              headers: {"Authorization" => "Bearer #{account.access_token}"})
    open(file_path ,"wb") { |file|
              file.write(response.body)
          }
  end

  send_sms(account.phone_number, "Hi #{account.name}! Your file #{file_name} has been downloaded.")
  send_file file_path
end

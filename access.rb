require 'httparty'
require 'singleton'

class Access
  include Singleton

  attr_accessor :accounts

  def initialize
    @accounts = []
  end

  def add_account(request_auth_info)
    user_info = self.get_user_info(request_auth_info["access_token"])
    accounts << Account.new(user_info["id"],
                            user_info["name"],
                            user_info["phone"],
                            request_auth_info["access_token"],
                            request_auth_info["expires_in"],
                            request_auth_info["refresh_token"])
  end

  def get_user_info(access_token)
    return HTTParty.get("https://api.box.com/2.0/users/me",
                            headers: {"Authorization" => "Bearer #{access_token}"}
                           )
  end
end

class Account
  attr_accessor :user_id
  attr_accessor :name
  attr_accessor :phone_number

  attr_accessor :access_token
  attr_accessor :expires_in
  attr_accessor :refresh_token

  def initialize(user_id, name, phone_number, access_token, expires_in, refresh_token)
    @user_id = user_id
    @name = name
    @phone_number = phone_number
    @access_token = access_token
    @expires_in = expires_in
    @refresh_token = refresh_token
  end
end
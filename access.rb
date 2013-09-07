require 'httparty'
require 'singleton'

class Access
  include Singleton

  ACCOUNTS_FILE = 'accounts.marshal'

  attr_accessor :accounts

  def initialize
    self.accounts = []
    self.load_from_file
  end

  def add_account(request_auth_info)
    user_info = self.get_user_info(request_auth_info["access_token"])
    if account = self.get_account(user_info["id"])
      account.update(request_auth_info["access_token"],
                            request_auth_info["expires_in"],
                            request_auth_info["refresh_token"])
    else
      self.accounts << Account.new(user_info,
                            request_auth_info["access_token"],
                            request_auth_info["expires_in"],
                            request_auth_info["refresh_token"])
    end
    self.dump_to_file
  end

  def get_user_info(access_token)
    return HTTParty.get("https://api.box.com/2.0/users/me",
                            headers: {"Authorization" => "Bearer #{access_token}"}
                           )
  end

  def get_account(user_id)
    self.accounts.each do |account|
      if account.user_id == user_id
        return account
      end
    end
    return nil
  end

  def load_from_file
    if File.exists?(ACCOUNTS_FILE)
      File.open(ACCOUNTS_FILE) do |file|
        self.accounts = Marshal.load(file)
      end
    else
      return false
    end
  end

  def dump_to_file
    File.open(ACCOUNTS_FILE,'w') do |file|
      Marshal.dump(self.accounts, file)
    end
  end
end

class Account
  attr_accessor :user_id
  attr_accessor :name
  attr_accessor :phone_number
  attr_accessor :avatar_url

  attr_accessor :access_token
  attr_accessor :expires_in
  attr_accessor :refresh_token

  def initialize(user_info, access_token, expires_in, refresh_token)
    self.user_id = user_info["id"]
    self.name = user_info["name"]
    self.phone_number = user_info["phone"]
    self.avatar_url = user_info["avatar_url"]
    self.access_token = access_token
    self.expires_in = expires_in
    self.refresh_token = refresh_token
  end

  def update(access_token, expires_in, refresh_token)
    self.access_token = access_token
    self.expires_in = expires_in
    self.refresh_token = refresh_token
  end
end
##
# From https://github.com/meskyanichi/backup/wiki/Generator 
# Backup
# Generated Template
#
# For more information:
#
# View the Git repository at https://github.com/meskyanichi/backup
# View the Wiki/Documentation at https://github.com/meskyanichi/backup/wiki
# View the issue log at https://github.com/meskyanichi/backup/issues
#
# When you're finished configuring this configuration file,
# you can run it from the command line by issuing the following command:
#
# $ backup -t my_backup [-c <path_to_configuration_file>]

Backup::Model.new(:mycelium, 'Mycelium Backup') do

  database MySQL do |db|
    db.name               = "mycelium"
    db.username           = "root"
    db.password           = "Q3lg8Af81tj6vr5PdcIs"
    db.host               = "int-mysql-master.agoodcloud.com"
    db.port               = 3306
    db.socket             = "/tmp/mysql.sock"
   end

  store_with S3 do |s3|
    s3.access_key_id      = 'AKIAJTNZWCZDOIDWFR4A'
    s3.secret_access_key  = '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'
    s3.region             = 'us-east-1'
    s3.bucket             = 'goodcloud-backups'
    s3.path               = '/backups'
    s3.keep               = 10
  end

  store_with CloudFiles do |cf|
    cf.api_key   = '9eea905ac00dfecb2d65ca81281b76f3'
    cf.username  = 'skoczen'
    cf.container = 'GoodCloud'
    cf.path      = '/backups'
    cf.keep      = 5
  end

  compress_with Gzip do |compression|
    compression.best = true
    compression.fast = false
  end

end

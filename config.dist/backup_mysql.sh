#!/bin/bash

. /etc/aws/farmconfig
. /etc/aws/authconfig
. /etc/aws/host.conf

. /usr/local/aws/lib/lib.sh
. /usr/local/aws/lib/mysqllib.sh
. /usr/local/aws/lib/s3lib.sh

log "Performing MySQL data backup."

BUCKET_NAME_MYSQL="$BUCKET_NAME/farm-mysql"
BCK_FILENAME=`mysql_data_backup`

if [ "$?" != 0 ] || [ -z "$BCK_FILENAME" ] || [ ! -f "$BCK_FILENAME" ]; then
    loga "Error occured while performing MySQL data backup."

    exit 1
fi

BCK_FILE_BASE=`basename "$BCK_FILENAME"`

CHTO=`$S3CMD put --force $BCK_FILENAME s3://$BUCKET_NAME_MYSQL/$BCK_FILE_BASE 2>&1` || {
     loga "Error occured while uploading MySQL backup to S3 bucket: $CHTO"

     exit 1
}

CHTORACK=`/root/upcs.sh -c GoodCloud -q $BCK_FILENAME 2>&1` || {
     loga "Error occured while uploading MySQL backup to Rackspace Cloud: $CHTO"
     exit 1
}


log "MySQL data backup completed. Data is now at: s3://$BUCKET_NAME_MYSQL/$BCK_FILE_BASE"

rm "$BCK_FILENAME"

import cStringIO
from celery.task import task
from django.core.files.base import ContentFile


@task
def generate_spreadsheet(account_id, useraccount_id, spreadsheet_id, file_type):
    print "starting.."
    from spreadsheets.models import Spreadsheet, DownloadedSpreadsheet
    from spreadsheets.spreadsheet import SpreadsheetAbstraction
    from accounts.models import Account, UserAccount

    account = Account.objects.get(pk=account_id)
    useraccount = UserAccount.objects.get(pk=useraccount_id, account=account)
    spreadsheet = Spreadsheet.objects.get(pk=spreadsheet_id, account=account)

    f_write = cStringIO.StringIO()
    SpreadsheetAbstraction.create_spreadsheet(spreadsheet.members, spreadsheet.template_obj, file_type, file_handler=f_write)

    extension = SpreadsheetAbstraction.extension_from_file_type(file_type)

    downloaded_spreadsheet = DownloadedSpreadsheet.objects.create(
                                account=spreadsheet.account, 
                                name=spreadsheet.full_name, 
                                num_records = spreadsheet.num_rows,
                                file_type = spreadsheet.default_filetype,
                                spreadsheet=spreadsheet,
                                )
    downloaded_spreadsheet.downloaded_file.save("%s.%s" % (spreadsheet.full_name, extension), ContentFile(f_write.getvalue()), save=False)
    downloaded_spreadsheet.finished = True
    downloaded_spreadsheet.save()
    
    from activities.tasks import save_action
    save_action.delay(account, useraccount, "generated a spreadsheet", spreadsheet=spreadsheet,)
    print "done"